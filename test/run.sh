#!/bin/bash
echo "test container : Displaying content of variable PS_HOST_PUBLIC_IP_ADDRESS ...."
echo $PS_HOST_PUBLIC_IP_ADDRESS
echo "Inside the container .... Trying to access storage "
ls 
cd /storage
cat test.txt
echo "Starting sshd server"
/usr/sbin/sshd -D
