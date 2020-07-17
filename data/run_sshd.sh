#!/bin/bash
echo "Displaying content of variable PS_HOST_PUBLIC_IP_ADDRESS ...."
echo $PS_HOST_PUBLIC_IP_ADDRESS
echo "Starting sshd server...."
/usr/sbin/sshd -D