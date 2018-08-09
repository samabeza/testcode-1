import sys
import os
import glob
import subprocess
import csv
from decimal import *
from datetime import datetime
import os.path
import time


###############counter for callflow##############################
failed_callflow = 0
testcases_callflow = 0
exec_counter_callflow = 0  
overall_passed_callflow = 0 
#########################END##############################

###############counter for transfer##############################
failed_transfer = 0
testcases_transfer = 0
exec_counter_transfer = 0
overall_passed_transfer = 0
#########################END##############################

def ini(used_by):
	start = time.time()
	for arg in sys.argv[2:]:
		used_by=arg
		return used_by,start
###############Get the value of the PARAMETER##############################
def main(foldername):
	for arg in sys.argv[1:]:
		data_path=arg
		testpath = data_path + "/"
		return testpath
#########################END##############################

#########################CHECK if DATA file CSV Exist in the folder##############################
def start(testpath):	
    try:
	finaldatapath = testpath + "Data File.csv"
        file = os.stat(finaldatapath)
        if file.st_size == 0:
            print "Data File is Empty"
    except OSError:
        print "Data File.csv not Found"
        sys.exit(1)
#########################END##############################

#########################START COMPARE SET Verbiage in Data File CSV to Call logs prompt##############################
def compare_callflow(calllog1, callflow1, y, gen_result, gen_report,testpath):
	global overall_passed_callflow 
	global failed_callflow
	finaldatapath = testpath + calllog1 ####path of the call logs
	global exec_counter_callflow 
	with open(finaldatapath) as calllog: ####open the call logs associated in the Data File CSV
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
	exec_counter_callflow +=1 
#########################END##############################

########################## START WRITING OF PASSED AND FAILED CALLFLOW (GENERATE HTML) ###############################
def excel_callflow(testpath):
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
	finaldatapath = testpath + "Data File.csv"
	with open(finaldatapath, 'rb') as f:
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
					compare_callflow(calllog1, callflow1, y, gen_result, gen_report,testpath)
					y+=1
	testcases_callflow = y - 1
########################## END CODE OF WRITING PASSED AND FAILED CALLFLOW (GENERATE HTML) ###############################
	
############################### START COMPARE OF TRANSFER TERM FROM DATA CSV FILE TO CALL LOGS ###################################	
def compare_transfer(calllog1, transfertype1, y, gen_result, gen_report,testpath):
    global overall_passed_transfer  
    global failed_transfer
    global exec_counter_transfer  
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
	finaldatapath = testpath + calllog1
        with open(finaldatapath) as calllog:
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
############################### END CODE OF COMPARING THE TRANSFER TERM FROM DATA CSV FILE TO CALL LOGS ###############################

########################## START WRITING OF PASSED AND FAILED TRANSFER TERM (GENERATE HTML) ###############################
def excel_transfer(testpath):
    global gen_report
    global testcases_transfer  
    gen_result = open("KVPs Result.html", "a")
    gen_report = open("report.html", "a")
    gen_result.write("<html> <center><h1>Inbound Build Acceptance Automation</h1> <h3>Transfer Term</h3></center>")
    gen_report.write("<html><table align='center' border='1' width='70%'> </table>")
    gen_report.write("<br/><table align='center' width='35%'><tr><td align='center'><font size='4'><b>Transfer Term</b></font></td></tr></table>")
    z = 0
    finaldatapath = testpath + "Data File.csv"
    with open(finaldatapath, 'rb') as f:
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
                    compare_transfer(calllog1, transfertype1, y, gen_result, gen_report,testpath)
                    y += 1
    testcases_transfer = y - 1	
########################## END CODE OF WRITING PASSED AND FAILED TRANSFER TERM (GENERATE HTML) ###############################

######################### START RUN OF JMETER TEST ###################################
def jmtest(testpath):
	finaldatapath = "./" + testpath + "HTTPRequest.jmx"
	check_file = os.path.isfile(finaldatapath)
	print check_file
	check_file = str(check_file)
	if check_file=="True":
	  y = os.path.abspath(finaldatapath)
	  z = y.replace('\\','\\\\') 
	  initial_path = "jmeter -Jjmeter.save.saveservice.output_format=xml -n -t"
	  command = "-l HTTPRequest.jtl"
	  final = initial_path + " " + z + " " + command
	  os.system(final)

	  	
#########################  END CODE FOR JMETER ###################################
		
if __name__ == "__main__":
	if len(sys.argv)==0:
		print("Please pass foldername as argument")
		exit()
	foldername=sys.argv[1]
	used_by=sys.argv[1]
	ini(used_by)
	user_email,start = ini(used_by)
	main(foldername)
	testpath = main(foldername)
	start(testpath) ############## Check the DATA CVS FILE ########################
	excel_callflow(testpath) ############## RUN Call Flow Test ########################
	####################### COUNTER for Call Flow ##################################
	if exec_counter_callflow == testcases_callflow:
		getcontext().prec = 3
		percentage = Decimal(overall_passed_callflow)/Decimal(testcases_callflow) * 100
		totalper = str(percentage) + '%'
		gen_report.write("</table><table align='center'> <tr><td><h3>Passed: "+ totalper +"</h3></td></tr> </table>")
		writetime.write("Call flow Percentage= " + totalper + "\n")
	if failed_callflow == 1:
		print"\n\n\n"
		raise SystemError('One of the Test Cases Failed')
		##################################### END of Code for Counter for Call Flow ######################################
	excel_transfer(testpath) ############## RUN Transfer Term Test ########################
	####################### COUNTER for Transfer Term ##################################
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
	##################################### END OF CODE of Counter for Transfer Term ######################################
	jmtest(testpath) ############## RUN JMeter Test ########################
	done=jmtest(testpath)
