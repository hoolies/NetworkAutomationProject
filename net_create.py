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

def create_core(dictionary: dict):
    [ns_create(f"core-{i}") for i in ["rt","h"]]
    
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

def net_creation(dictionary: dict):
    print(f"Setting up the network")
    for key,value in dictionary.items():
        # print("Your hosts are:", v['hosts'])
        # print("Your subnet is:", v['subnet'])
        print("Creating Namespaces for the network, router, bridge and host")
        # Router
        ns_create(f"{key}-rt")
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
        network_connector(key,"rt","br")
    
        # Connect to need to connect to Core and provide IP




def yaml_dict(file: str)-> dict:
    with open(file, "r") as yml:
       return safe_load(yml)  # pass back to the caller python data


def main():
    """Main Function"""
    # Import the file as dictionary
    Networks = yaml_dict("./Final/topology.yml")
    # Use the dictionary 
    net_creation(Networks)
    # Print the output
    run(subprocess_parser("brctl show"))


if __name__ == "__main__":
    main()