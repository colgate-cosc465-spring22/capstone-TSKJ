#!/usr/bin/python3
import sys

def main():
    
    if (len(sys.argv) > 1):
        file = sys.argv[1]
    else:
        file = "kwireshark.txt"
    f=open(file,"r")
    file = "IPs.txt"
    outfile = open(file, 'w')
    lines=f.readlines()
    counter = 0
    for x in lines:
        if(counter != 0):
            outfile.write(x.split()[3])
            outfile.write('\n')
        counter = counter + 1
    f.close()
    outfile.close()

if __name__=="__main__":
    main()
