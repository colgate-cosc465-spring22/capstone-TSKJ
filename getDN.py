#!/usr/bin/python3

import dns.resolver
import ipaddress
import dns

import dns.name
import dns.message
import dns.query
import dns.flags

import concurrent.futures

import threading

import socket
def main():
    inf = open("data.txt",'r')
    f = open("data2.txt","w")
    for line in inf:
        IP = line.strip()
        f.write(str(socket.gethostbyaddr(IP)[0]))
        f.write('\n')
    inf.close()
    f.close()
    
main()