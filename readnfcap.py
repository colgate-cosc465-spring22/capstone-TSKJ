#!/usr/bin/python3
# import required module
import os
# assign directory
for n in ['22', '23', '24', '25', '26', '27', '28', '29', '51', '52']:
    directory = 'sflowData/sflow' + n
    outf = open(n + ".txt", 'w')
    # iterate over files in
    # that directory
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            outf.write(f + '\n')
            #print(f)
    outf.close()