#!/usr/bin/python3
import requests
import re

'''
Gets categories for domain names from input file f (opened in main())
'''

def getCat(d_name):
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
                'Authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiZmQ1NGI5MGMzN2M4MGIwOTFhYTkxNDY5YjBkMGEyYjgxMmVlMzU2ZDA2OGE1M2U5ZjlkMmZiY2IwNjhhNGRlYWE4MTIzZDcxZmM0YjA3ZmUiLCJpYXQiOjE2NTAzOTY4NTEsIm5iZiI6MTY1MDM5Njg1MSwiZXhwIjoxNjgxOTMyODUxLCJzdWIiOiI2MDcwIiwic2NvcGVzIjpbXX0.HvLyDwtfpR8LLxE7Ru2uhP9ZeanNpeo-LSgqRhmucva4zt34ZQ2Y6-oU4qxbxJRN2kXp84Vi4kHuJFnSsFe5cg",
                'cache-control': "no-cache"
                }
                
    r = requests.request("POST", url, data=payload, headers=headers)
    
    #extract category and confidence from response
    s_resp = r.text
    l = s_resp.split(":")[3:5]
    print("Category: " + l[1].split("}")[0][3:-1] + "; ", end =" ")
    print("Confidence: " + l[0].split(",")[0])

def main():

    # print("Testing getCat(): ")
    # d_name = "tiktok.com"
    # print("Domain: " + d_name, end="; ")
    # getCat(d_name)

    # *******************    IMPORTANT         **************************

    #test output is in categories.txt
    #run using --> ./getCat.py > categories.txt (if you do not modify code)
    #send output to a different file if you modify code, so that we have access to old test cases


    f = open("data2.txt",'r')
    for line in f:
        d_name = line.strip()
        print("Domain: " + d_name, end="; ")
        try:
            getCat(d_name)
        except:
            print(" ERROR")

if __name__=="__main__":
    main()
