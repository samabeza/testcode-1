import sys
import os
import glob
import subprocess
import csv
failed = 0
def main():
    try:
        file = os.stat("Callflow.txt")
        if file.st_size == 0:
            print "Callflow.txt is Empty"
    except OSError:
        print "Callflow.txt not Found"
        sys.exit(1)

    try:
        file = os.stat("Calllog.txt")
        if file.st_size == 0:
            print "Calllog.txt is Empty"
            sys.exit(1)
    except OSError:
        print "Calllog.txt not Found"
        sys.exit(1)

def compare(calllog1, callflow1, y):
    gen_Report = open("report.html","a")
    global failed
    with open(calllog1) as calllog:
        flag=0
        # hello = open("HatScript" + ".txt", 'w')
        verbiage = set()
        for line in calllog:
            if 'fetch' in line and 'fetchtype=audio' in line and 'outcome=success' in line and 'wicstd' not in line and 'TVMusic' not in line and 'typing_30Sec' not in line and 'kalimba' not in line and 'hold_music' not in line:
                # HAT = open("HatScript" + ".txt", 'a')
                endvalue = line.find(".wav")
                strtvalue = line.rfind('/', 0, endvalue)
                prompt = line[strtvalue:endvalue].replace('/','')
                # print prompt
                verbiage.add(prompt)
                # HAT.write(prompt +"\n")
                flag = 1
            if 'fetch_end Done (memory)' in line and 'dynocat' not in line:
                endvalue = line.find(".wav")
                strtvalue = line.rfind('/', 0, endvalue)
                prompt = line[strtvalue:endvalue].replace('/', '')
                verbiage.add(prompt)
                flag = 1
            if 'fetch' in line and 'audio' in line and 'dynocat' not in line:
                endvalue = line.find(".wav")
                strtvalue = line.rfind('/', 0, endvalue)
                prompt = line[strtvalue:endvalue].replace('/', '')
                # print prompt
                verbiage.add(prompt)
                flag = 1
            # elif 'prompt_play' in line and 'dynocat' not in line:
            #     endvalue = line.find(".wav")
            #     strtvalue = line.rfind('/', 0, endvalue)
            #     prompt = line[strtvalue:endvalue].replace('/', '')
            #     verbiage.add(prompt)
            #     flag = 1
    # print verbiage

    # print callflow1
    promptlist = callflow1.split()
    countlist =len(promptlist)
    x= 0
    z=0
    y =str(y)
    print "\nTest "+ y+ ": List of Expected Verbiage:"
    while x < countlist:
        if promptlist[x] in verbiage:
            print promptlist[x] + " Found"
            x+=1
        else:
            print promptlist[x] + " Not Found"
            x+=1
            z = 1
            failed = 1
    if z == 1:
        print "                   STATUS: FAILED"
    else:
        print "                   STATUS: PASSED"
    if flag == 0:
        print "\nTest "+ y + ": Calllog does not contain any .wav file "+ calllog1
    # with open("Callflow.txt") as success:
    #     print "\nChecked Expected prompts:"
    #     y=0
    #     for line in success:
    #         x = line.strip()
    #         if x in verbiage:
    #             print x + "  Found "
    #             # y+=1
    #         else:
    #             print x + " Not Found "

    if flag ==1:
        print "\nTest "+ y+ ": List of Verbiage hit by Calllogs for " + calllog1 +":"
        print '\n'.join(verbiage)
        # print y


def excel():
    z= 0
    with open('Data File.csv', 'rb') as f:
        reader = csv.reader(f)
        next(reader, None)
        # flow =[]
        y= 1;
        for line in reader:
            callflow1 =line[0]
            calllog1 = line[2]
            # print callflow
            # print len(callflow)
            if len(callflow1) >= 10:
                if len(calllog1)>= 10:
                    # print callflow1
                    # print calllog1
                    compare(calllog1, callflow1, y)
                    y+=1

            # print callflow
            # print calllog
            # print flow[0]

if __name__ == "__main__":

    # main()
    # compare()
    excel()
    if failed == 1:
        print"\n\n\n"
        raise SystemError('One of the Test Cases Failed')
