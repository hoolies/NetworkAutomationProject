#!/bin/env python3
"""Network Automation Project, Howard's and Chrysanthos' take"""
from subprocess import run


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




# for veth1, veth2, ns1 in veth_connections:
#     if not veth_pair_exists(veth1, ns1):
#          run(subprocess_parser(f"sudo ip link add {veth1} type veth peer name {veth2}"))
#          run(subprocess_parser(f"sudo ip link set {veth1} netns {ns1}"))
#          run(subprocess_parser(f"sudo ip netns  {ns1} ip link set dev {veth1} up"))
#          run(subprocess_parser(f"sudo ip link set dev {veth2} up"))
#     else:
#         print(f"VETH pair {veth1} already exists in namespace {ns1}.")


def main():
    """Main Function"""
    # Lists
    namespaces = ["dmz", "core", "corp", "nat"]    
    bridges = [f"{namespace}-br" for namespace in namespaces]
    routers = [f"{namespace}-router" for namespace in namespaces]
    switches = [f"{namespace}-sw" for namespace in namespaces]
    
    print(f"Setting up the network namespaces")
    for namespace in namespaces:
        # Namespace
        namespace_exists(namespace)
        # Ethernet bridges
        print(f"Setting Ethernet Bridges")
        run(subprocess_parser(f"sudo ip link add name {namespace}-br type bridge"))
        run(subprocess_parser(f"sudo ip link set dev {namespace}-br up"))


    run(subprocess_parser("brctl show"))


if __name__ == "__main__":
    main()