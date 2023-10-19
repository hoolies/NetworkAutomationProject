# NetworkAutomationProject
Network Automation Project

This is Howard's and Chrysanthos's take.

## Table of Contents

- [Project Description](#project-description)
- [Prerequisites](#prerequisites)
- [Usage](#usage)
- [Configuration](#configuration)


## Project Description

This project provides a set of Python scripts to automate the creation and management of network namespaces and Ethernet bridges. It is designed to streamline the setup of network environments, making it easier to work with isolated network segments and bridges.

The project includes the following key functions:

- Creating and managing network namespaces.
- Checking the existence of network namespaces.
- Creating and managing VETH pairs within namespaces.
- Setting up Ethernet bridges within namespaces.
- Loading network configurations from YAML files.

## Prerequisites

Before using this project, you need to have the following dependencies installed:

- Python 3
- The `yaml` module
- Network namespace tools (e.g., `ip netns` and `brctl`)

You can install the Python dependencies using the following command:

```bash
pip install PyYAML
```
## Usage

Clone this repository to your local machine.

```bash

git clone https://github.com/your-username/network-automation-project.git
```

Navigate to the project directory.

```bash

cd network-automation-project
```

Run the script to set up your network environment.

```bash

python script.py
```

Follow the prompts to create and manage network namespaces, VETH pairs, and Ethernet bridges.

## Configuration

The network configuration is loaded from a YAML file (topology.yml) that defines the namespaces and their associated hosts. You can customize this file to match your specific network requirements.

Example topology.yml file:
```
---
networks:
  dmz:
    hosts:
      - host1
      - host2
    subnet: 192.168.1.0/24
  core:
    hosts:
      - host3
    subnet: 192.168.2.0/24
  corp:
    hosts:
      - host4
      - host5
    subnet: 192.168.3.0/24
  nat:
    hosts:
      - host6
    subnet: 192.168.4.0/24
```
