#!/usr/bin/python3
import requests
import re

'''
Gets categories for domain names from input file f (opened in main())
'''
def divide100DNs():
    inf = open("allDNs.txt", 'r')
    for n in ['DN1', 'DN2', 'DN3', 'DN4', 'DN5','DN6']:
        outf = open(n+".txt", 'w')
        for i in range(100):
            line = inf.readline()
            outf.write(line)
        outf.close()
    outf = open('DN7.txt','w')
    for i in range(22):
        line = inf.readline()
        outf.write(line)
    outf.close()
    inf.close()
def getCat(d_name, outf):
    '''
    takes a domain name (str) and prints its category and confidence
    '''
    #found the code to sent request to categorize on the Klazify website

    url = "https://www.klazify.com/api/categorize"

    #payload = "{\"url\":\"https://www.google.com\"}\n"

    payload = "{\"url\":\"" + "https://" + d_name + "\"}\n"

    #in the Authorization field, the thing after "Bearer" is a key you get if you sign up for the Klazify API online
    #sign up by clicking "Get API Key"
    #has a limit of 100 categorizations per month
    headers = {
                'Accept': "application/json",
                'Content-Type': "application/json",
                'Authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiN2I4MmQ2N2I1YWY2MmExNTc3NmVjZDVjMmFkZTFiYzc1NmYzZGQ4N2M0NmFiMWNiNDlhZjhmMzQ4YmEyMmU5ODM0MzQ2ZGMwNGIyM2U2NjYiLCJpYXQiOjE2NTAzOTgyNTEsIm5iZiI6MTY1MDM5ODI1MSwiZXhwIjoxNjgxOTM0MjUxLCJzdWIiOiI2MDcxIiwic2NvcGVzIjpbXX0.fuA3XeYGrzXGeeX9go9Edm70XSiZxgcAxuMGU3_lcfEFqMTv3Ims06qvGTiag8BhF5uKfHQWkX_hHPxPLzh4kQ",
                'cache-control': "no-cache"
                }
                
    r = requests.request("POST", url, data=payload, headers=headers)
    
    #extract category and confidence from response
    s_resp = r.text
    l = s_resp.split(":")[3:5]
    outf.write("Category: " + l[1].split("}")[0][3:-1] + "; " + " ")
    outf.write("Confidence: " + l[0].split(",")[0] + "\n")

def main():

    # print("Testing getCat(): ")
    # d_name = "tiktok.com"
    # print("Domain: " + d_name, end="; ")
    # getCat(d_name)

    # *******************    IMPORTANT         **************************

    #test output is in categories.txt
    #run using --> ./getCat.py > categories.txt (if you do not modify code)
    #send output to a different file if you modify code, so that we have access to old test cases

    #divide100DNs()  #breaks large file of Domain Names in 100-entry chunks

    f = open("DN7.txt",'r')
    outf = open("categories.txt", 'a')
    for i in range(4):
        line = f.readline()
        d_name = line.strip()
        outf.write("Domain: " + d_name + ";")
        try:
            getCat(d_name, outf)
        except:
            outf.write(" ERROR\n")
    f.close()
    outf.close()

if __name__=="__main__":
    main()
