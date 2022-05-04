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

#returns IP to check DN for
# and updates frequency of flow for each colgate IP
def getIP(t, sfrDict):
    subnetList = ['faculty', 'staff','guest','student','other']
    srcIP, dstIP, b = t

    s = srcIP[1:-1].split('.')
    d = dstIP[1:-1].split('.')


    isSrcColgate = isColgate(s)
    isDstColgate = isColgate(d)

    subnet = 'external'  #if neither IP falls in the colgate subnet, that gets recorded in this
    IP = ''

    if isSrcColgate:
        s_subnet = findSubnet(int(s[2]))
        if (isDstColgate):
           d_subnet = findSubnet(int(d[2]))
           if s_subnet == 4:
               subnet = subnetList[d_subnet]
               IP = srcIP
           subnet = subnetList[s_subnet]
        IP = dstIP 
    else:
        IP = srcIP
        if (isDstColgate):
           d_subnet = findSubnet(int(d[2]))
           subnet = subnetList[d_subnet]

    sfrDict[subnet][0] += 1
    sfrDict[subnet][1] += int(b)

    return IP    

def isColgate(ipLst):
    return ipLst[0]=='149' and ipLst[1]=='43'

def findSubnet(third8):
    if third8 in [56, 57, 58, 59]:
        return 0
    elif third8 in [68, 69, 70, 71]:
        return 1
    elif third8 in [92, 93, 94, 95]:
        return 2
    elif third8 in [96, 97, 98, 99, 192, 193, 194, 195]:
        return 3
    return 4 #not one of the specified /22 subnets but still colgate IP


'''
Gets Domain Names for IP addresses from input file inf (opened in main())
'''
def main():

    sfrDict = {} #dictionary of key = subnet and value = [sflow record, bytes of data exchanged]
    for key in ['faculty', 'staff','guest','student', 'other', 'external']:
      sfrDict[key] = [0, 0] #index 0 is number of flow records, index 1 is number of bytes exchanged

    DNs_not_found = []

    for n in ['22','23', '24', '25', '26', '27', '28', '29', '51', '52']:
        inf = open(n+".txt", 'r')
        outf = open(n + "DNs.txt", 'w')  #return list of unique destination DNs from input file of (srcIP, dstIP) files

        url_lst = []

        for line in inf:
            t = tuple(line.strip()[1:-1].split())
            IP = getIP(t, sfrDict)[1:-2]
            try:
                url = str(socket.gethostbyaddr(IP)[0]).split('.')
                finalURL = url[1:3]
                finalURL = (".").join(finalURL)
                if finalURL not in url_lst:
                    outf.write(finalURL)
                    outf.write('\n')
                    url_lst.append(finalURL)
            except:
                DNs_not_found.append(IP)

        inf.close()
        outf.close()

    getAllDNs()

    f = open('sflow_by_subnet.txt', 'w')
    for key in sfrDict:
        f.write(key + ": " + str(sfrDict[key]))
        f.write('\n')
    f.close()

    f = open('DNs_not_found.txt', 'w')
    for IP in DNs_not_found:
        f.write(IP)
        f.write('\n')
    f.close()

# def main():

#     # testing isColgate
#     f= open("22.txt",'r')

#     sfrDict = {} #dictionary of subnet and sflow record frequency pairs
#     for key in ['faculty', 'staff','guest','student', 'other','external']:
#         sfrDict[key] = [0, 0] #index 0 is number of flow records, index 1 is number of bytes exchanged

#     for line in f:
#       t = tuple(line.strip()[1:-1].split())
#       srcIP, dstIP, b = t
#       #print(dstIP, isColgate((dstIP)[1:-1].split('.')))

#       IP = getIP(t, sfrDict)
#       print(IP)
#     print(sfrDict)
#     f.close


    
if __name__=="__main__":
    main()