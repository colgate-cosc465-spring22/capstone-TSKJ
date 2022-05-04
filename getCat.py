#!/usr/bin/python3
import requests
import re

'''
Gets categories for domain names from input file f (opened in main())
'''
#breaks large file of Domain Names in 100-entry chunks
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
<<<<<<< HEAD
                'Authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiYjA0NGIzMGFjMmNlZGQ4ZTE3ZGU5OTA0OWYyNjdhNGJkZThjZTQ3MzIwNjI1ZjAwNGVkYmFmMzQzZDdiMDEzMDE4NTFjZWU1Y2QyYmVkM2IiLCJpYXQiOjE2NTE2ODg1ODYsIm5iZiI6MTY1MTY4ODU4NiwiZXhwIjoxNjgzMjI0NTg2LCJzdWIiOiI2MTE4Iiwic2NvcGVzIjpbXX0.o0Em_dd6js5TBBh539DqKKGOhbDqSS7UX8-NUq-3UbtBD5hrZHYUA7dZN-4TK63UJ5A3EwmAwgDL8RI5W7bYvw",
=======
                'Authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiZmI3YzM2Nzc4MGVmODIxZmI4ZWI5N2MzMmM3ZTllNGI3MzkzYzdhMjZjMTExMzkxNmU5YmQ4ZmMzN2MzNTVlMDI2YTRlOWIxOGFmZDE4NDUiLCJpYXQiOjE2NTE2ODg3NDIsIm5iZiI6MTY1MTY4ODc0MiwiZXhwIjoxNjgzMjI0NzQyLCJzdWIiOiI2MTIwIiwic2NvcGVzIjpbXX0.fBwgW9a87XXnJB-Yo6Hu8b4957QzeyP6Mn5PouSQuDhUbJy_RhT4VmgCl0PF__kQChJ3cCT9mhr4LoAbTfsLCQ",
>>>>>>> 61806ab5eb778025c5a106fddb716b50fc7a7a60
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
    
    fname = "DN5.txt"
    f = open(fname,'r')  #replace number after "DN" in fname for the smaller file of DNs to categorize
                         #and use a valid key on line 41
    outf = open(fname[0:3] + "categories.txt", 'a')
    for line in f:
        #line = f.readline()
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
