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

#for testing/debugging
smalldata_lst = ['sdata1.csv', 'sdata2.csv', 'sdata3.csv', 'sdata4.csv', 'sdata5.csv','sdata6.csv', 'sdata7.csv', 'sdata8.csv', 'sdata9.csv', 'sdata10.csv']

#using the actual data
data_lst = ['data1.csv', 'data2.csv', 'data3.csv', 'data4.csv', 'data5.csv','data6.csv', 'data7.csv', 'data8.csv', 'data9.csv', 'data10.csv']

#list of ECS-enabled domains from each thread
output_lst = ['output1.txt', 'output2.txt', 'output3.txt', 'output4.txt', 'output5.txt','output6.txt', 'output7.txt', 'output8.txt', 'output9.txt', 'output10.txt']

#number of domains that resulted in errors for each thread
error_count_lst = [0,0,0,0,0,0,0,0,0,0]

#moved to global scope from main
RECURSIVE_RESOLVER_IP = '127.0.0.1'
RECURSIVE_RESOLVER_PORT = 8053

def print_record(record):
    # IPv4 address
    if (record.rdtype == dns.rdatatype.A):
        ipv4_address = record.address
        print('\t\tA {}'.format(ipv4_address))
    # Name server domain name
    elif (record.rdtype == dns.rdatatype.NS):
        name_server_domain_name = record.target
        print('\t\tNS {}'.format(name_server_domain_name))
    # Canonical name (i.e., alias)
    elif (record.rdtype == dns.rdatatype.CNAME):
        canonical_domain_name = record.target
        print('\t\tCNAME {}'.format(canonical_domain_name))
    # Other type of record
    else:
        print('\t\t{}'.format(record))

def print_record_set(record_set):
    domain_name = record_set.name
    print('\t{}'.format(domain_name))
    for record in record_set:
        print_record(record)

def print_response(response):
    # Response code
    response_code = response.rcode()
    response_description = dns.rcode.to_text(response_code)
    print('Response code: %d %s' % (response_code, response_description))

    # Options
    print('Options:')
    for option in response.options:
        if (option.otype == dns.edns.ECS):
            print('\tECS %s/%d' % (option.address, option.scopelen))
        else:
            print(opt)

    # Answer
    print('Answers:')
    for record_set in response.answer:
        print_record_set(record_set)

    # Authority
    print('Authority:')
    for record_set in response.authority:
        print_record_set(record_set)

    # Additional
    print('Additional:')
    for record_set in response.additional:
        print_record_set(record_set)

    # Blank line
    print('')

def construct_query(domain, record_type, client_network=None):
    if client_network is None:
        query = dns.message.make_query(domain, record_type)
    else:
        network_address = str(client_network.network_address)
        network_prefixlen = client_network.prefixlen
        ecs = dns.edns.ECSOption(network_address, network_prefixlen)
        query = dns.message.make_query(domain, record_type, use_edns=True, 
                options=[ecs])
    return query

def issue_query(domain, ns_ip, client_network=None, ns_port=53):
    # Create query
    record_type = 'A' # Type of record to request
    #print('Query name server {} on port {} for {} record for {} for client {}'.format(ns_ip, ns_port, record_type, domain, client_network)) 
    #original code commented out
    query = construct_query(domain, record_type, client_network)
    #print(query) #original code commented out

    # Issue query
    tout = 3 # Timeout in seconds
    try:
        response = dns.query.udp(query, ns_ip, timeout=tout, port=ns_port)
    except dns.exception.Timeout:
        #print('Query timed out')
        return

    # Print response
    #print_response(response)  #original code commented out
    return response
    
'''Checks whether domain is a CNAME (alias).'''
def check_cname(answer):
    # print("Checking cname.")
    cname_flag = dns.rrset.RRset.__str__(answer[0]).split()[3]
    if cname_flag == "CNAME":
        # print("CNAME found.")
        return True
    return False

def is_ECS_Enabled(domain, NS_IP):    
    networks = ['149.43.80.0/20', '149.43.80.0/25', '149.43.80.0/30']

    #re-send query with three different prefix sizes and check scope
    for net in networks:
        client_net = ipaddress.ip_network(net)
        resp = issue_query(domain, NS_IP, client_net)

        if resp is not None:
                        
            code = resp.rcode() #0 if there is no error
                            
            if code == 0:

                resp_opt = resp.options #get options section
                resp_opt_len = len(resp_opt)

                if resp_opt_len > 0:   
                    options = dns.rrset.RRset.__str__(resp.options[0]) #convert to str
                    
                    scope = (options.split()[2]).split('/')[1]
                    #print("scope: " + scope)
                    
                    if int(scope) != 0: #need 1 non-zero scope to be ECS-enabled
                        return True
    
    return False #none of the responses replies have non-zero scope 

def check_threads(inputfname, outputfname, index):
    #print("checking thread " + str(index))
    error_count = 0
    f = open(inputfname, 'r')  #got a 10-line long file to test things on
    outputf = open(outputfname, 'w') #function will pass in fname
    for line in f:
        # Added a try except block to catch exceptions thrown when formatting issues are raised
        try:
            # print("Index: " + str(index) + ". Errors: " + str(error_count))
            # Strip domain name
            domain = line.strip().split(',')[1]  #tested this, it works
            #print("domain:", domain)

            # Issue query for authoritative NS
            resp = issue_query(domain, RECURSIVE_RESOLVER_IP, ns_port=RECURSIVE_RESOLVER_PORT)
            #print(type(resp))
            if resp is not None:
                code = resp.rcode() #0 if there is no error
                # ECS Check if NOERROR
                if code == 0:
                    resp_add = resp.additional      # Get "Additional" field from query
                    resp_add_len = len(resp_add)
                    resp_auth = resp.authority      # Get "Authority" field from query
                    auth_len = len(resp_auth)
                    resp_answ = resp.answer         # Get "Answer" field from query
                    answ_len = len(resp_answ)
                    #print("============<DNS RESPONSE>============")
                    #print_response(resp)            # DEBUG: Response print
                    #print("======================================")
                    # Check whether a CNAME record is present
                    is_cname = False
                    if answ_len > 0:
                        is_cname = check_cname(resp_answ)   # helper: Check for CNAME record

                    # ECS Check if it is not a CNAME record
                    if not is_cname:
                        # <Option 1>. If there is an IP address in the "Additional" section
                        # if code==0 and resp_add_len>0:
                        if resp_add_len > 0:
                            #print("ADDTIONAL LEN != 0")
                            resp_add_1 = str(resp.additional[0])
                            #print("resp_add_1: " + resp_add_1)
                            IP = resp_add_1.split()[4]  # IP Address
                            #print("✅ NS IP: " + IP)
                            if not is_IPv6(IP):
                                
                                # ============ Got name server IP. Do ECS Check ===============
                                #enables_ECS = is_ECS_Enabled(domain, IP)
                                #print("ECS-enabled?", str(enables_ECS))
                                if is_ECS_Enabled(domain, IP):
                                    outputf.write(domain + "\n")
                            else:
                                error_count += 1
                                continue
                                #continue #need counter
                        # <Option 2>: If there is no "Additional" section, check "Authority" section
                        # and run another query with the obtained nameserver
                        elif auth_len > 0:
                            #print("AUTHORITY LEN != 0")
                            auth_NS = str(resp.authority[0]).split()[4]
                            #print("auth_NS: " + auth_NS)
                            # Completed try-except block.
                            try:
                                # Issue another query for the authoritative NS
                                resp = issue_query(auth_NS, RECURSIVE_RESOLVER_IP, ns_port=RECURSIVE_RESOLVER_PORT)
                                #print("============<DNS RESPONSE>============")
                                #print_response(resp)
                                #print("======================================")
                                code = resp.rcode()         # Check for NOERROR
                                resp_answ = resp.answer
                                answ_len = len(resp_answ)
                                
                                # ECS Check if NOERROR
                                if code == 0:
                                    # We need the check again whether it is a CNAME.
                                    if answ_len > 0:
                                        is_cname = check_cname(resp_answ)
                                    
                                    # ECS Check if it is not a CNAME record
                                    if not is_cname:    
                                        resp_answ_0 = str(resp_answ[0])
                                        IP = resp_answ_0.split()[4]
                                        #print("✅ NS IP: " + IP)
                                        # ============ Got name server IP. Do ECS Check ===============
                                    else:
                                        # CNAME detected
                                        #print("❌ Error: CNAME detected.")
                                        error_count += 1
                                        continue
                                        # ============ SKIP ECS Check ==============
                                else:
                                    # NOT NOERROR
                                    #print("❌ Error: Domain does not exist! (SERVFAIL/NXDOMAIN)")
                                    error_count += 1
                                    continue
                                    # ============ SKIP ECS Check ==============
                            except:
                                # Catch query fail. (defensive programming)
                                #print("❌ Error: could not find name server!")
                                error_count += 1
                                continue
                                # ============ SKIP ECS Check ==============
                            if not is_IPv6(IP):
                                
                                # ============ Got name server IP. Do ECS Check ===============
                                #enables_ECS = is_ECS_Enabled(domain, IP)
                                #print("ECS-enabled?", str(enables_ECS))
                                if is_ECS_Enabled(domain, IP):
                                    outputf.write(domain + "\n")
                            else:
                                error_count += 1
                                continue
                            #enables_ECS = is_ECS_Enabled(domain, IP)
                            #print("ECS-enabled?", str(enables_ECS))
                    else:
                        # CNAME detected
                        #("❌ Error: CNAME detected.")
                        error_count += 1
                        continue
                        # ============ SKIP ECS Check ==============
                else:
                    # NOT NOERROR
                    #print("❌ Error: Domain does not exist! (SERVFAIL/NXDOMAIN)")
                    error_count += 1
                    continue
                    # ============ SKIP ECS Check ==============
            else:
                # Catch query fail.
                #print("❌ Error: could not find name server!")
                error_count += 1
                continue
                # ============ SKIP ECS Check ==============
        except:
            error_count += 1
            continue
        #print('\n██████████████████████████████████████████████████████\n')

    error_count_lst[index] = error_count
    f.close()
    outputf.close()

def is_IPv6(IP):
    return ":" in IP

def main():
    executor = concurrent.futures.ThreadPoolExecutor(max_workers = 10)
    thread_lst = []
    for i in range(10):
        x = threading.Thread(target=check_threads, args=(data_lst[i], output_lst[i], i))
        thread_lst.append(x)
    for x in thread_lst:
        x.start()
    for x in thread_lst:
        x.join()
    #print(counter_lst)
    
    
    big_output = open('ECS_list.txt','w')
    ECS_count = 0
    for fname in output_lst:
        f = open(fname, 'r')
        for line in f:
            big_output.write(line)
            ECS_count += 1
    big_output.close()

    summary = open('summary.txt','w')
    error_count_final = 0
    for count in error_count_lst:
        error_count_final += count
    summary.write("No. of domains that are ECS-enabled: " + str(ECS_count) + "\n")
    summary.write("No. of error-free domains: " + str(1000000-error_count_final) + "\n")
    summary.write("No. of domains that resulted in errors: " + str(error_count_final) + "\n")
    summary.write("Percent of domains that are ECS-enabled: " + str((ECS_count/(1000000-error_count_final))*100) + "%\n")
    summary.close()






if __name__ == '__main__':
    main()
