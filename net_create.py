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
    run(subprocess_parser(f"sudo ip netns add {namespace}"))


def net_creation(dictionary: dict):
    print(f"Setting up the network")
    for key,value in dictionary.items():
        # print("Your hosts are:", v['hosts'])
        # print("Your subnet is:", v['subnet'])
        print("Creating Namespaces for the network, router, bridge and host")
        # Network
        namespace_exists(key)
        # Bridge
        namespace_exists(f"{key}br")
        # Router
        namespace_exists(f"{key}rt")
        # Host
        namespace_exists(f"{key}h")
        # Ethernet bridges
        print(f"Setting Ethernet Bridges")
        run(subprocess_parser(f"sudo ip link add name {key}br type bridge"))
        run(subprocess_parser(f"sudo ip link set dev {key}br up"))
        # vETHs
        print(f"Create vETHs for {key}")
        # Bridge
        run(subprocess_parser(f"sudo ip link add {key}h2br type veth peer name br2{key}h"))
        run(subprocess_parser(f"sudo ip link set {key}h2br netns {key}h"))
        run(subprocess_parser(f"sudo ip link set dev br2{key}h master {key}br"))
        run(subprocess_parser(f"sudo ip link set dev br2{key}h up"))
        # Router
        run(subprocess_parser(f"sudo ip link add {key}rt2br type veth peer name br2{key}rt"))
        run(subprocess_parser(f"sudo ip link set {key}rt2br netns {key}rt"))
        run(subprocess_parser(f"sudo ip link set dev {key}br2rt master {key}br"))
        run(subprocess_parser(f"sudo ip link set dev {key}br2rt up"))


def yaml_dict(file: str)-> dict:
    with open(file, "r") as yml:
       return safe_load(yml)  # pass back to the caller python data


def main():
    """Main Function"""
    # Lists
    # namespaces = ["dmz", "core", "corp", "nat"]    
    # bridges = [f"{namespace}br" for namespace in namespaces]
    # routers = [f"{namespace}router" for namespace in namespaces]
    Networks = yaml_dict("./Final/topology.yml")
    net_creation(Networks)
    
    run(subprocess_parser("brctl show"))


if __name__ == "__main__":
    main()