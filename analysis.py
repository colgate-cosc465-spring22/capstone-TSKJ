#!/usr/bin/python3

def allCat():

    catsDict = {} #dictionary of key = categories and values = [frequency, average confidence]
    num_categorized = 0
    names_searched = 0
    for n in ['DN1', 'DN2', 'DN3', 'DN4', 'DN5','DN6', 'DN7']:
        f = open(n+"categories.txt",'r')
        for line in f:
            names_searched += 1
            l = line.strip().split(':')
            conf = l[-1].strip()
            if len(l)>2 and conf[0].isnumeric():
                num_categorized += 1
                cats = l[2].strip().split(';')[0].split('\/')
                conf = float(conf)
                for cat in cats:
                    if cat not in catsDict:
                        catsDict[cat] = [1, conf]
                    else:
                        prev_freq = catsDict[cat][0]
                        prev_conf = catsDict[cat][1]
                        catsDict[cat][0] += 1
                        catsDict[cat][1] = ((prev_freq*prev_conf) + conf) / (prev_freq + 1)

    outf = open("allCat.csv", 'w')
    outf.write("Categories, Count, Average confidence\n")
    for key in catsDict:
        v = catsDict[key]
        k = key
        if "," in key:
            k = key.split(',')[0][:-1]
        outf.write(k + "," + str(v[0]) + "," + str(v[1]) + "\n")
    outf.close()

    outf = open("summary.txt", "a")
    outf.write("Unique DNs found from IP address from sflow record: " + str(names_searched) + "\n")
    outf.write("DNs for which a category was found: " + str(num_categorized) + " i.e only " + str((num_categorized/names_searched)*100)+ "% \n")
    outf.write(str(catsDict) + "\n\n")
    outf.close()

def getSummary():

    sflows_examined = 0
    DNs_not_found = 0

    f = open("sflow_by_subnet.txt", 'r')
    for line in f:
        l = line.strip().split(":")[1].strip()[1:-1].split(",")
        sflows_examined+= int(l[0])
    f.close()

    f = open("DNs_not_found.txt", 'r')
    for line in f:
        DNs_not_found += 1
    f.close()


    outf= open("summary.txt", 'w')
    outf.write("Sflow records checked: " + str(sflows_examined) + "\n")
    outf.write("IP addresses from sflows for which domain names were NOT found " + str(DNs_not_found) + " i.e " + str((DNs_not_found/sflows_examined)*100) + "% \n\n")
    outf.close()

def main():
    getSummary()
    allCat()

if __name__=="__main__":
    main()