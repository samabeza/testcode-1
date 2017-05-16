import sys
import os
import glob
import subprocess
import csv
failed = 0
def main():
    try:
        file = os.stat("transfertype.txt")
        if file.st_size == 0:
            print "transfertype.txt is Empty"
    except OSError:
        print "transfertype.txt not Found"
        sys.exit(1)

    try:
        file = os.stat("Calllog.txt")
        if file.st_size == 0:
            print "Calllog.txt is Empty"
            sys.exit(1)
    except OSError:
        print "Calllog.txt not Found"
        sys.exit(1)

def compare(calllog1, transfertype1, y):
    x = 0
    transfer = transfertype1.split(';')
    total_terms = len(transfer)
    global failed
    y = str(y)
    # print total_terms
    print "Test " + y + ": " + "For Call log " + calllog1
    total_terms = total_terms -1
    while total_terms > x :
        flag = 0
        split_1 = transfer[x].split('=')
        first = split_1[0].lower().strip()
        second = split_1[1].strip()
        with open(calllog1) as calllog:
            verbiage = set()
            for line in calllog:
                if (first +':' in line.lower() or first +'=' in line.lower()) and second in line:
                    verbiage.add(line)
                    flag = 1
                elif first +':' in line.lower() or first +'=' in line.lower():
                    verbiage.add(line)


        print transfer[x]
        if flag == 0:
            print "Not Found"
        elif len(verbiage)==0:
            print "Not Found"
        else:
            print "Found"
        print ''.join(verbiage)
        x += 1

def excel():
    z= 0
    with open('Data File.csv', 'rb') as f:
        reader = csv.reader(f)
        next(reader, None)
        # flow =[]
        y= 1;
        for line in reader:
            transfertype1 =line[1]
            calllog1 = line[2]
            # print transfertype
            # print len(transfertype)
            if len(transfertype1) >= 5:
                if len(calllog1)>= 5:
                    # print transfertype1
                    # print calllog1
                    compare(calllog1, transfertype1, y)
                    y+=1

            # print transfertype
            # print calllog
            # print flow[0]

if __name__ == "__main__":

    # main()
    # compare()
    excel()
    if failed == 1:
        print"\n\n\n"
        raise SystemError('One of the Test Cases Failed')