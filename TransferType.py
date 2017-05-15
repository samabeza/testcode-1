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
    global failed
    transfer =transfertype1.split()
    total_terms =len(transfer)
    split_1 = transfer[0].split('=')
    print split_1[0]




    with open(calllog1) as calllog:
        flag=0
        verbiage = set()
        for line in calllog:
            if split_1[0].lower().strip() in line.lower() and (':'in line or'='in line):
                # endvalue = line.find("|")
                # strtvalue = line.rfind('|', 0, endvalue)
                # prompt = line[strtvalue:endvalue].replace('/','')
                verbiage.add(line)
                flag = 1

    print calllog1
    print '\n'.join(verbiage)

    #
    # promptlist = transfertype1.split()
    # countlist =len(promptlist)
    # x= 0
    # z=0
    # y =str(y)
    # print "\nTest "+ y+ ": List of Expected Verbiage:"
    # while x < countlist:
    #     if promptlist[x] in verbiage:
    #         print promptlist[x] + " Found"
    #         x+=1
    #     else:
    #         print promptlist[x] + " Not Found"
    #         x+=1
    #         z = 1
    #         failed = 1
    # if z == 1:
    #     print "                   STATUS: FAILED"
    # else:
    #     print "                   STATUS: PASSED"
    # if flag == 0:
    #     print "\nTest "+ y + ": Calllog does not contain any .wav file "+ calllog1
    # # with open("transfertype.txt") as success:
    # #     print "\nChecked Expected prompts:"
    # #     y=0
    # #     for line in success:
    # #         x = line.strip()
    # #         if x in verbiage:
    # #             print x + "  Found "
    # #             # y+=1
    # #         else:
    # #             print x + " Not Found "
    #
    # if flag ==1:
    #     print "\nTest "+ y+ ": List of Verbiage hit by Calllogs for " + calllog1 +":"
    #     print '\n'.join(verbiage)
    #     # print y


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