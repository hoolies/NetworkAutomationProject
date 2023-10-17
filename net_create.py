#!/bin/env python3
"""Network Automation Project, Howard's and Chrysanthos' take"""
from subprocess import run

grn = "\033[32m"
wht = "\033[0m"


def namespace_exists(namespace):
    """Check if the namespace exist"""
    try:
        if run(["sudo", "ip", "netns", "list", "| grep", namespace]):
            return
        else:
            run(["sudo", "ip", "netns", "add", namespace])
    except Error as e:
        print(e)

# Namespace
print(f"{grn}Setting up the network namespaces{wht}")
namespaces = ["ohost", "phost", "whost", "yhost", "prouter", "yrouter", "wrouter", "orouter", "crouter"]
for namespace in namespaces:
    namespace_exists(namespace)

# Ethernet bridges
print(f"{grn}Setting Ethernet Bridges{wht}")
bridges = ["pbridge", "obridge", "ybridge", "wbridge"]
for bridge in bridges:
    run(["sudo", "ip", "link", "add", "name", bridge, "type", bridge])
    run(["sudo", "ip", "link", "set", "dev", bridge, "up"])

run(["brctl", "show"])

# Function to check if a VETH pair exists in a specific namespace
def veth_pair_exists(veth, namespace):
    run("ip", "netns", "exec", namespace, "ip", "link", "show", veth, "up")

# Create VETH pairs
#print(f"{grn}Install VETHs{wht}")
#veth_connections = [
#    ("phost2pbrg", "pbridge", "phost"),
#    ("prout2pbrg", "pbridge", "prouter"),
#    ("yhost2ybrg", "ybridge", "yhost"),
#    ("yrout2ybrg", "ybridge", "yrouter"),
#    ("whost2wbrg", "wbridge", "whost"),
#    ("wrout2wbrg", "wbridge", "wrouter"),
#    ("ohost2obrg", "obridge", "ohost"),
#    ("orout2obrg", "obridge", "orouter"),
#    ("crout2prout", "pbridge", "crouter"),
#    ("crout2yrout", "ybridge", "crouter"),
#    ("crout2wrout", "wbridge", "crouter"),
#    ("crout2orout", "obridge", "crouter"),
#    ("crout2nat", "nat", "crouter"),
#]

#for veth1, veth2, ns1 in veth_connections:
#    if not veth_pair_exists(veth1, ns1):
#        run_command(f"sudo ip link add {veth1} type veth peer name {veth2}")
#        run_command(f"sudo ip link set {veth1} netns {ns1}")
#        run_command(f"sudo ip netns :wqexec {ns1} ip link set dev {veth1} up")
#        run_command(f"sudo ip link set dev {veth2} up")
#    else:
#        print(f"VETH pair {veth1} already exists in namespace {ns1}.")