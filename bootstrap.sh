#!/bin/bash

echo "This script will set you up to use Ansible and Python"

echo "Updating the OS"
sudo apt update -y && sudo apt upgrade -y;

echo "Installing python3, pip, ansible and openssh"
sudp apt install python3 python3-pip ansible openssh
python3 --version
ansible --version
python3 -m pip install --upgrade pip

echo "Creating Python venv"
mkdir ~/NAP
python3 -m venv ~/NAP
source ~/NAP/bin/activate
python3 -m pip install paramiko jinja2


echo "Run the Playbook"
ansible-playbook bookname.yml