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


def namespace_exists(namespace: str):
    """Check if the namespace exist"""
    try:
        if run(subprocess_parser(f"sudo ip netns list | grep {namespace}")):
            return
        else:
            run(subprocess_parser(f"sudo ip netns add {namespace}"))
    except Error as e:
        print(e)


def veth_pair_exists(veth: str, namespace: str):
    """Function to check if a VETH pair exists in a specific namespace"""
    run(subprocess_parser(f"ip netns exec {namespace} ip link show {veth} up"))


def switches(veth: str, namespace: str):
    """Bring vETHs up"""
    run(subprocess_parser(f"ip netns exec {namespace} link show {veth} up"))

def net_creation(dictionary: dict):
    print(f"Setting up the network namespaces")
    for key,value in dictionary.items():
        print("Your hosts are:", v['hosts'])
        print("Your subnet is:", v['subnet'])
        # Namespace
        namespace_exists(key)
        for host in hosts:
            namespace_exists(host)
        # Ethernet bridges
        print(f"Setting Ethernet Bridges")
        run(subprocess_parser(f"sudo ip link add name {key}-br type bridge"))
        run(subprocess_parser(f"sudo ip link set dev {key}-br up"))
        # run(subprocess_parser(f"sudo ip netns exec {namespace} ip a add {ip} dev vEth"))



def yaml_dict(file: str)-> dict:
    with open(file, "r") as yml:
       return safe_load(yml)  # pass back to the caller python data


def main():
    """Main Function"""
    # Lists
    # namespaces = ["dmz", "core", "corp", "nat"]    
    # bridges = [f"{namespace}-br" for namespace in namespaces]
    # routers = [f"{namespace}-router" for namespace in namespaces]
    Networks = yaml_dict("./Final/topology.yml")
    net_creation(Networks)
    



    run(subprocess_parser("brctl show"))


if __name__ == "__main__":
    main()