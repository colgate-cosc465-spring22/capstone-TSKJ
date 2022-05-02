#!/usr/bin/python3
# import required module
import os

def getIP(fname, d, outf):
    f = open(d+'/'+fname, 'r')
    for line in f:
        l = line.split(',')
        if len(l[0])>8 and len(l)>6:
            t = (l[3], l[4])
            outf.write(str(t) + '\n')
    f.close()


def main():
# assign directory
    for n in ['22', '23', '24', '25', '26', '27', '28', '29', '51', '52']:
        directory = 'sflowData/sflow' + n
        outf = open(n + ".txt", 'w')
        # iterate over files in
        # that directory
        for filename in os.listdir(directory):
            test = filename
            f = os.path.join(directory, filename)
            # checking if it is a file
            if os.path.isfile(f):
                getIP(filename, directory, outf)
        outf.close()

if __name__=="__main__":
    main()