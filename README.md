# NetworkAutomationProject
Network Automation Project

This is Howard's and Chrysanthos's take.

# Network Automation Project with Python and Ansible

## About

This project aims to demonstrate how to use Python, Ansible and Bash to create a scalable network infrastructure that might includes virtual machines (VMs) and containers.

## Prerequisites

Before you begin, ensure you have installed the following:

* Python: You'll need Python installed on your machine.
* Ansible: Install Ansible, a powerful automation tool, on your system.
* Virtualization Platform: Depending on your choice, set up a virtualization platform such as VirtualBox, VMware, or others.
* Container Platform: Install a container platform like Docker or Kubernetes, as per your requirements.

## Project Requirements
### Primary
1. Design a data structure input file
   * Name
   * Network
   * Hosts
   * Other
2. Hub and spoke network design
3. Python script or Ansible playbook to process the input file
4. Deploy the network:
   * Namespaces
   * vEths
   * IPtables
   * Bridges
   * IP2 commands
5. Update documentation and README.md
### Seconday
1. Write a python script that tests end to end connectivity
1. Write a python script that deploys 2 VMs:
   * Each machine is in a different network
   * VMs must launch using KVM hypervisor via QEMU primitives
1. Write an Ansible playbook to:
   * Install iperf on each VM
   * Test network performance
   * Submit the results
1. Deploy SD-WAN using python script:
   * Deploy a VM
   * Install iperf
   * Test SD-WAN connectivity
   * Use bravo and charlie clouds
### Tertiary
1. Run a simple Python Flask service inside one of the network namespaces
   * It should respond to HTTP requests
   * Service need to be deployed by Python script or Ansible playbook
1. Write an Ansible plug module:
   * Publish it in acollection
   * Demonstrate downloading it
   * Use it to automate some aspect of NFV

### Our Project

![](https://raw.githubusercontent.com/hoolies/NetworkAutomationProject/main/Diagram.png)