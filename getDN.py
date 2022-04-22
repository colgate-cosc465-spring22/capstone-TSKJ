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


'''
Gets Domain Names for IP addresses from input file inf (opened in main())
'''
def main():
    inf = open("data1.txt",'r')
    outf = open("data2.txt",'w')
    url_lst = []
    for line in inf:
        IP = line.strip()
        try:
            url = str(socket.gethostbyaddr(IP)[0]).split('.')
            finalURL = url[-2::]
            finalURL = (".").join(finalURL)
            #print(finalURL)
            #print(finalURL not in url_lst)
            if finalURL not in url_lst:
                outf.write(finalURL)
                outf.write('\n')
                url_lst.append(finalURL)
                #print(url_lst)
        except:
            pass
    inf.close()
    outf.close()
    
if __name__=="__main__":
    main()