#!/bin/env python3
"""Network Automation Project, Howard's and Chrysanthos' take"""
from subprocess import run
from yaml import safe_load


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


def net_creation(dictionary: dict):
    """Use other functions to create the network"""
    print(f"Setting up the network")
    # Create Core namespaces
    [ns_create(f"core-{i}") for i in ["r","h"]]
    # Remove the key networks
    networks_list = dictionary['networks']
    # Iterate through the nested dictionaries, network is a dictionary
    for network in networks_list:
        for key, vaulue in network.items():
            print(f"Creating Namespaces for:\n\t- Network: {key}\n\t- Router: {key}-r\n\t- Host: {key}-h")
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
            # Create connection to core
            create_core(network)


def yaml_dict(file: str)-> dict:
    """Takes a string for the YAML file path and returns a dictionary"""
    with open(file, "r") as yml:
       return safe_load(yml)  # pass back to the caller python data


def main():
    """Main Function"""
    # Import the file as dictionary
    Networks = yaml_dict("./Final/topology.yml")
    # Use the dictionary 
    net_creation(Networks)
    # Connect Core to NAT
    nat_connections()


if __name__ == "__main__":
    main()