#!/bin/bash

echo -e "These are the namespaces:\n"
namespaces=$(ip netns list)

for namespace in ${namespaces[@]}
do
   sudo ip netsn delete $namespace
done

echo -e "These are the bridges:\m"
bridges=$(brctl show | cut -d' ' -f1)

for bridge in ${bridges[@]}
if $bridge != "docker0" or $bridge!= "lo":
do
    sudo ip link delete $bridge
done
fi