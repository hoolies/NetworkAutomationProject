#!/bin/env python3
"""Network Automation Project, Howard's and Chrysanthos' take"""
from subprocess import run
from yaml import safe_load
from ipaddress import IPv4Network


def subprocess_parser(command: str) -> list:
    """Function that takes a sting and transforms it to list for subprocess run"""
    if command:
        listout = command.split()
    else:
        print("You need to enter a string")
    return listout


def ns_create(namespace: str):
    """Check if the namespace exist"""
    run(subprocess_parser(f"sudo ip netns add {namespace}"))


def bridger(network: str):
    """Function to create the bridge and bring it up"""
    run(subprocess_parser(f"sudo ip link add name {network}-br type bridge"))
    run(subprocess_parser(f"sudo ip link set dev {network}-br up"))


def network_connector(network: str, source: str, destination: str):
    """Function to cconnect the network componenets"""
    run(subprocess_parser(f"sudo ip link add {network}-{source}2{destination} type veth peer name {network}-{destination}2{source}"))
    run(subprocess_parser(f"sudo ip link set {network}-{source}2{destination} netns {network}-{source}"))
    run(subprocess_parser(f"sudo ip link set dev {network}-{destination}2{source} master {network}-{destination}"))
    run(subprocess_parser(f"sudo ip link set dev {network}-{destination}2{source} up"))


def create_core(network: str):
    """Create the core and NAT"""
    run(subprocess_parser(f"sudo ip link add core2{network} type veth peer name {network}2core"))
    run(subprocess_parser(f"sudo ip link set core2{network} netns core-r"))
    run(subprocess_parser(f"sudo ip link set {network}2core netns {network}-r"))


def nat_connections():
    """Create the NAT connection to the core"""
    run(subprocess_parser(f"sudo ip link add core2nat type veth peer nat2core"))
    run(subprocess_parser(f"sudo ip link set core2nat netns core"))
    run(subprocess_parser(f"sudo ip netns exec core-r ip addr add 10.225.255.17/30 dev core-r2nat"))
    run(subprocess_parser(f"sudo ip netns exec core-r ip link set dev core-r2nat up"))
    run(subprocess_parser(f"sudo ip addr add 10.225.255.18/30 dev nat2core-r"))



def veth_creation(key: str):
    print(f"Creating Namespaces for:\n\t- Network: \t{key}\n\t- Router: \t{key}-r\n\t- Host: \t{key}-h")
    # Namespace
    ns_create(key)
    # Router
    ns_create(f"{key}-r")
    # Host
    ns_create(f"{key}-h")
    # Ethernet bridges
    print(f"Setting Ethernet Bridges")
    bridger(key)
    # vETHs
    print(f"Create vETHs for {key}")
    # Host to bridge connection
    network_connector(key,"h","br")
    # Router to bridge
    network_connector(key,"r","br")


def net_creation(dictionary: dict):
    """Use other functions to create the network"""
    print(f"Setting up the network")
    # Create Core namespaces
    [ns_create(f"core-{i}") for i in ["r","h"]]
    # Remove the key networks
    networks_list = dictionary['networks']
    # Iterate through the nested dictionaries, network is a dictionary
    for network in networks_list:
        for key, value in network.items():
            veth_creation(key)
            # Create connection to core
            create_core(key)
            # IP forwarding for the network:
            ip_forwarding_per_subnet(key)
            # Assign IPs
            # assiging_ip(key)
            # subnet = value['subnet']
            # list_of_ips = [str(ip) for ip in IPv4Network(subnet)]


def yaml_dict(file: str)-> dict:
    """Takes a string for the YAML file path and returns a dictionary"""
    with open(file, "r") as yml:
       return safe_load(yml)  # pass back to the caller python data
        


def ip_forwarding_activate():
    run(subprocess_parser(f"sudo sysctl net.bridge.bridge-nf-call-iptables=0"))
    run(subprocess_parser(f"echo 'net.ipv4.ip_forward = 1"))
    # run(subprocess_parser(f"net.ipv6.conf.default.forwarding = 1"))
    # run(subprocess_parser(f"net.ipv6.conf.all.forwarding = 1' | sudo tee /etc/sysctl.d/10-ip-forwarding.conf"))
    run(subprocess_parser(f"sudo ip netns exec core-r sysctl -p /etc/sysctl.d/10-ip-forwarding.conf"))


def ip_forwarding_per_subnet(network: str):
    run(subprocess_parser(f"sudo ip netns exec {network}-r sysctl -p /etc/sysctl.d/10-ip-forwarding.conf"))


def assiging_ip(network: str, subnet: str):
    """Assign IPs"""
    run(subprocess_parser(f"sudo ip netns exec {network} ip addr add {subnet} dev {network}-h2br"))
    run(subprocess_parser(f"sudo ip netns exec {network} ip link set dev {network}-h2br up"))
    run(subprocess_parser(f"sudo ip netns exec {network} ip link set dev lo up"))


def assiging_ip(network: str, subnet: str):
    # phost LAN link
    run(subprocess_parser(f"sudo ip netns exec {network} ip addr add {subnet} dev {network}-h2br"))
    run(subprocess_parser(f"sudo ip netns exec {network} ip link set dev {network}-h2br up"))
    run(subprocess_parser(f"sudo ip netns exec {network} ip link set dev lo up"))


def assign_static_routes(network: str, subnet: str):
    """Create static routes"""
    # Configure routes on the core router
    run(subprocess_parser(f"sudo ip netns exec {network} ip route add {subnet} via 10.255.5.2"))
    run(subprocess_parser(f"sudo ip netns exec {network} ip route add default via 10.225.255.18"))
    #Configure default routes on the hosts
    run(subprocess_parser(f"sudo ip netns exec {network} ip route add default via 10.225.255.18"))
    #Configure the default routes on the edge routers
    run(subprocess_parser(f"sudo ip netns exec {network} ip route add default via 10.225.255.18"))


# def prevent_DHCP(network: str):
#     """Prevent DHCP"""
#     run(subprocess_parser(f"sudo ip addr add 192.168.90.3/24 dev {network}-br2r"))
#     run(subprocess_parser(f"sudo ip addr add 192.168.90.4/24 dev {network}-br"))


def enable_nat(subnet: str):
    # enabling NAT
    run(subprocess_parser(f"sudo iptables -t nat -F"))
    run(subprocess_parser(f"sudo iptables -t nat    -A POSTROUTING -s {subnet} -o ens3 -j MASQUERADE"))
    run(subprocess_parser(f"sudo iptables -t filter -A FORWARD -i ens3 -o nat2crout -j ACCEPT"))
    run(subprocess_parser(f"sudo iptables -t filter -A FORWARD -o ens3 -i nat2crout -j ACCEPT"))
    run(subprocess_parser(f"sudo ip route add {subnet} via 10.225.255.17"))


def main():
    """Main Function"""
    # Import the file as dictionary
    Networks = yaml_dict("/home/student/Final/topology.yml")
    # Create core namespace
    ns_create("core")
    # Use the dictionary 
    net_creation(Networks)
    # Activate IP Forwarding
    ip_forwarding_activate()
    # Connect Core to NAT
    nat_connections()

if __name__ == "__main__":
    main()
