import sys
import os
import glob
import subprocess
import csv
from decimal import *
from datetime import datetime
import os.path

failed_callflow = 0
testcases_callflow = 0#add on top (divider)
exec_counter_callflow = 0 #thissss 
overall_passed_callflow = 0 #thissss

failed_transfer = 0
testcases_transfer = 0
exec_counter_transfer = 0
overall_passed_transfer = 0

def main(foldername):
	for arg in sys.argv[1:]:
		data_path=arg
		print data_path

def start():
    try:
        file = os.stat("Data File.csv")
        if file.st_size == 0:
            print "Data File is Empty"
    except OSError:
        print "Data File.csv not Found"
        sys.exit(1)


def compare_callflow(calllog1, callflow1, y, gen_result, gen_report):
	global overall_passed_callflow #thisssss
	global failed_callflow

	global exec_counter_callflow #thisss
	with open(calllog1) as calllog:
		flag=0
		verbiage = set()
		for line in calllog:
			if 'fetch' in line and 'fetchtype=audio' in line and 'outcome=success' in line and 'wicstd' not in line and 'TVMusic' not in line and 'typing_30Sec' not in line and 'kalimba' not in line and 'hold_music' not in line:
				endvalue = line.find(".wav")
				strtvalue = line.rfind('/', 0, endvalue)
				prompt = line[strtvalue:endvalue].replace('/','')
				verbiage.add(prompt)
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
				verbiage.add(prompt)
				flag = 1

	promptlist = callflow1.split()
	countlist =len(promptlist)
	testcases_callflow = countlist
	x= 0
	z=0
	y =str(y)
	found_prompt = set()
	not_found_prompt = set()
	print "\nTest "+ y+ ": List of Expected Verbiage:"
	while x < countlist:
		if promptlist[x] in verbiage:
			print promptlist[x] + " Found"
			found_prompt.add(promptlist[x] + " Found")
			x+=1
		else:
			print promptlist[x] + " Not Found"
			not_found_prompt.add(promptlist[x] + " Not Found")
			x+=1
			z = 1
			failed = 1
	f_prompt = '<br/>'.join(found_prompt)
	nf_prompt = '<br/>'.join(not_found_prompt)
	verbi ='<br/>'.join(verbiage)
	prompi = '<br/>'.join(promptlist)
	if z == 1:
		print "                   STATUS: FAILED"
		gen_result.write("<tr><td align='center'>" + y + "</td><td>" + prompi + "</td> <td>" + verbi + "</td> <td>" + calllog1 + "</td> <td>" + nf_prompt + "</td> <td bgcolor='#e06745' align='center'>Failed</td>  </tr>")
		gen_report.write("<tr><td align='center'>" + y + "</td> <td>" + calllog1 + "</td> <td bgcolor='#e06745'>Failed </td></tr>")
	else:
		overall_passed_callflow+=1#add this
		print "                   STATUS: PASSED"
		gen_result.write("<tr><td align='center'" + y + "</td><td>" + prompi + "</td> <td>" + verbi + "</td> <td>" + calllog1 + "</td> <td>" + f_prompt + "</td>  <td bgcolor='#99e26f'>Passed</td>  </tr>")
		gen_report.write("<tr><td align='center'>" + y + "</td> <td>" + calllog1 + "</td> <td bgcolor='#99e26f'>Passed </td></tr>")
	if flag == 0:
		print "\nTest "+ y + ": Calllog does not contain any .wav file "+ calllog1
	if flag ==1:
		print "\nTest "+ y+ ": List of Verbiage hit by Calllogs for " + calllog1 +":"
		print '\n'.join(verbiage)
		# print y
	exec_counter_callflow +=1 #---------------------
 
def excel_callflow():
	global gen_report
	global testcases_callflow #thisss
	global writetime
	starttime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	writetime = open("writetime.txt", "a")
	writetime.write("Start Time= " + starttime + "\n")
	gen_result = open("Call Flow Result.html", "a")
	gen_report = open("report.html", "a")
	gen_result.write("<html> <center><h1>Inbound Build Acceptance Automation</h1> <h3>Call Flow</h3></center>")
	gen_report.write("<html><table align ='center'  border='1' width='70%'> <center><h1>Inbound Build Acceptance Automation</h1><br/></table>") 
	gen_report.write("<br/><table  align='center' width='35%'><tr><td align='center'><font size='4'><b>Call Flow</b></font></td></tr></table>")
	z= 0
	with open('Data File.csv', 'rb') as f:
		reader = csv.reader(f)
		next(reader, None)
		y= 1;
		gen_result.write("<table border='1' align='center'><tr><td align='center' bgcolor='#c2c4c6'> <b>Test Case </b> </td> "
						 "<td align='center' bgcolor='#c2c4c6'> <b> Expected Prompts</b> </td> "
						 "<td align='center' bgcolor='#c2c4c6'> <b>Prompts Found </b></td> "
						 "<td align='center' bgcolor='#c2c4c6'> <b>Call Log </b></td> "
				 		 "<td align='center' bgcolor='#c2c4c6'> <b>Remarks </b></td>"
						 "<td align='center' bgcolor='#c2c4c6'> <b>Result </b></td></tr>")
		gen_report.write("<table border='1' align='center' width='35%'><tr><td align='center' bgcolor='#c2c4c6' width='10%'> <b>Test Case</b> </td> "
						 "<td align='center' bgcolor='#c2c4c6' width='60%'> <b>Call Log</b> </td> "
						 "<td align='center' bgcolor='#c2c4c6' width='20%'> <b>Pass/Fail </b></td></tr>")
		for line in reader:
			callflow1 =line[0]
			calllog1 = line[2]
			if len(callflow1) >= 10:
				if len(calllog1)>= 10:
					compare_callflow(calllog1, callflow1, y, gen_result, gen_report)
					y+=1
	testcases_callflow = y - 1

def compare_transfer(calllog1, transfertype1, y, gen_result, gen_report):
    global overall_passed_transfer  # thisssss
    global failed_transfer
    global exec_counter_transfer  # thisss
    x = 0
    z = 0
    transfer = transfertype1.split(';')
    total_terms = len(transfer)
    global failed_transfer
    y = str(y)
    print "Test " + y + ": " + "For Call log " + calllog1
    total_terms = total_terms - 1
    alllines = set()
    found_prompt = set()
    not_found_prompt = set()
    while total_terms > x:
        flag = 0
        split_1 = transfer[x].split('=')
        first = split_1[0].lower().strip()
        second = split_1[1].strip()
        with open(calllog1) as calllog:
            verbiage = set()
            for line in calllog:
                if (first + ':' in line.lower() or first + '=' in line.lower()) and second in line:
                    verbiage.add(line)
                    alllines.add(line)
                    flag = 1
                elif first + ':' in line.lower() or first + '=' in line.lower():
                    verbiage.add(line)
                    alllines.add(line)

        if flag == 0:
            print transfer[x] + "\tWrong Value"
            not_found_prompt.add(transfer[x] + " Wrong Value or Not Found")
            z = 1
            failed = 1
        elif len(verbiage) == 0:
            print transfer[x] + "\tNot Found"
            failed = 1
            z = 1
        else:
            print transfer[x] + "\tFound"
            found_prompt.add(transfer[x] + " Found")
        print ''.join(verbiage)
        x += 1
    verbi = '<br/>'.join(alllines)
    prompi = '<br/>'.join(transfer)
    f_prompt = '<br/>'.join(found_prompt)
    nf_prompt = '<br/>'.join(not_found_prompt)
    if z == 1:
        print "                   STATUS: FAILED"
        gen_result.write(
            "<tr><td align='center'>" + y + "</td><td>" + prompi + "</td> <td>" + verbi + "</td>  <td>" + calllog1 + "</td> <td>" + nf_prompt + "</td> <td bgcolor='#e06745'>Failed</td></tr>")
        gen_report.write(
            "<tr><td align='center'>" + y + "</td><td>" + calllog1 + "</td> <td bgcolor='#e06745'>Failed </td></tr>")
    else:
        overall_passed_transfer += 1
        print "                   STATUS: PASSED"
        gen_result.write(
            "<tr><td align='center'>" + y + "</td><td>" + prompi + "</td> <td>" + verbi + "</td>   <td>" + calllog1 + "</td> <td>" + f_prompt + "</td> <td bgcolor='#99e26f'>Passed</td> </tr>")
        gen_report.write(
            "<tr><td align='center'>" + y + "</td><td>" + calllog1 + "</td> <td bgcolor='#99e26f'>Passed </td></tr>")
    exec_counter_transfer += 1	
	
def excel_transfer():
    global gen_report
    global testcases_transfer  # thisss
    gen_result = open("KVPs Result.html", "a")
    gen_report = open("report.html", "a")
    gen_result.write("<html> <center><h1>Inbound Build Acceptance Automation</h1> <h3>Transfer Term</h3></center>")
    gen_report.write("<html><table align='center' border='1' width='70%'> </table>")
    gen_report.write("<br/><table align='center' width='35%'><tr><td align='center'><font size='4'><b>Transfer Term</b></font></td></tr></table>")
    z = 0
    with open('Data File.csv', 'rb') as f:
        reader = csv.reader(f)
        next(reader, None)
        y = 1;
        gen_result.write(
            "<table border='1' align='center'> <tr><td bgcolor='#c2c4c6' align='center'> <b>Test Case</b> </td> "
            "<td bgcolor='#c2c4c6' align='center'> <b>Transfer Term</b> </td> "
            "<td bgcolor='#c2c4c6' align='center'> <b>Actual Logs</b> </td> "
            "<td bgcolor='#c2c4c6' align='center'> <b>Call Logs</b> </td> "
            "<td bgcolor='#c2c4c6' align='center'> <b>Remarks</b> </td> "
            "<td bgcolor='#c2c4c6' align='center'> <b>Result</b> </td></tr>")
        gen_report.write(
            " <table border='1' align='center' width='35%'> <tr><td align='center' bgcolor='#c2c4c6' width='10%'> <b>Test Case</b> </td> "
            "<td align='center' bgcolor='#c2c4c6' width='60%'> <b>Call Log </b></td>"
            "<td align='center' bgcolor='#c2c4c6' width='20%'> <b>Pass/Fail </b></td></tr>")
        for line in reader:
            transfertype1 = line[1]
            calllog1 = line[2]
            if len(transfertype1) >= 5:
                if len(calllog1) >= 5:
                    compare_transfer(calllog1, transfertype1, y, gen_result, gen_report)
                    y += 1
    testcases_transfer = y - 1	

def jmtest():
	check_file = os.path.isfile("HTTPRequest.jmx")
	print check_file
	check_file = str(check_file)
	if check_file=="True":
	  y = os.path.abspath("./HTTPRequest.jmx")
	  z = y.replace('\\','\\\\') 

	  initial_path = "jmeter -Jjmeter.save.saveservice.output_format=xml -n -t"
	  command = "-l HTTPRequest.jtl"

	  final = initial_path + " " + z + " " + command

	  os.system(final)
		
if __name__ == "__main__":
	if len(sys.argv)==0:
		print("Please pass foldername as argument")
		exit()
	foldername=sys.argv[1]
	main(foldername)
	start()
	excel_callflow()
	if exec_counter_callflow == testcases_callflow:
		getcontext().prec = 3
		percentage = Decimal(overall_passed_callflow)/Decimal(testcases_callflow) * 100
		totalper = str(percentage) + '%'
		gen_report.write("</table><table align='center'> <tr><td><h3>Passed: "+ totalper +"</h3></td></tr> </table>")
		writetime.write("Call flow Percentage= " + totalper + "\n")
	if failed_callflow == 1:
		print"\n\n\n"
		raise SystemError('One of the Test Cases Failed')
	excel_transfer()
	if exec_counter_transfer == testcases_transfer:
        	getcontext().prec = 3
        	percentage = Decimal(overall_passed_transfer) / Decimal(testcases_transfer) * 100
        	totalper = str(percentage) + '%'
        	gen_report.write("</table><table align='center'> <tr><td><h3>Passed: " + totalper + "</h3></td></tr> </table>")
        	writetime = open("writetime.txt","a")
        	writetime.write("TransferType Percentage= " + totalper + "\n")
   	if failed_transfer == 1:
        	print"\n\n\n"
        	raise SystemError('One of the Test Cases Failed')
	jmtest()
	
