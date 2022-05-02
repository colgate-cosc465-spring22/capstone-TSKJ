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

def getAllDNs():
    outf = open("allDNs.txt",'w')
    DNlst = []
    for n in ['22','23', '24', '25', '26', '27', '28', '29', '51', '52']:
        f = open(n+"DNs.txt", 'r')
        for line in f:
            DN = line.strip()
            if DN not in DNlst:
                outf.write(DN + '\n')
                DNlst.append(DN)


'''
Gets Domain Names for IP addresses from input file inf (opened in main())
'''
def main():
    for n in ['22','23', '24', '25', '26', '27', '28', '29', '51', '52']:
        inf = open(n+".txt", 'r')
        #inf = open("data1.txt",'r')
        outf = open(n + "DNs.txt", 'w')  #return list of unique destination DNs from input file of (srcIP, dstIP) files
        #outf = open("data2.txt",'w')
        url_lst = []
        for line in inf:
            #IP = line.strip()
            srcIP, dstIP = tuple(line.strip()[1:-1].split())
            IP = dstIP[1:-1]
            try:
                url = str(socket.gethostbyaddr(IP)[0]).split('.')
                finalURL = url[1:3]
                finalURL = (".").join(finalURL)
                #print(finalURL)
                if finalURL not in url_lst:
                    outf.write(finalURL)
                    outf.write('\n')
                    url_lst.append(finalURL)
                    #print(url_lst)
            except:
                pass
        inf.close()
        outf.close()

        getAllDNs()
    
if __name__=="__main__":
    main()