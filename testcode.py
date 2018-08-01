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

def main():
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

def api_report():
	global ttype_per
	global cflow_per
	gen_report = open("report.html", "a")
	gen_report.write("<html><table align='center' border='1' width='70%'> </table>")
	gen_report.write("<br/><table align='center' width='35%'><tr><td align='center'><font size='4'><b>API</b></font></td></tr></table>")
	gen_report.write("<table border='1' align='center' width='35%'> <tr><td align='center' bgcolor='#c2c4c6' width='10%'> <b>Test Case</b> </td> <td align='center' bgcolor='#c2c4c6' width='60%'> <b>API </b></td>""<td align='center' bgcolor='#c2c4c6' width='20%'> <b>Pass/Fail </b></td></tr>")

	passed = 0
	failed = 0
	gettestcases = set()

	check_file = os.path.isfile("HTTPRequest.jtl")
	check_file = str(check_file)
	if check_file=="True":
		print "TRUEE"
		print check_file

	jtl = open("HTTPRequest.jtl", "r")
	for line in jtl:
		if "lb" in line:
			line = line.replace('</httpSample>','').strip()
			gettestcases.add(line)

	print '\n'.join(gettestcases)
	testcases = len(gettestcases)

	y = 1
	for results in gettestcases:		
		if ('rc="200"' in results) and ('rm="OK"' in results):
			endvalue = results.find("lb=") 
			endvalue2 = results.find("rc")
			strtvalue = results.rfind('', 0, endvalue)
			strtvalue2 = results.rfind('', 0, endvalue2)
			getapi = results[strtvalue:strtvalue2].replace('lb=','').replace('"','')
			print "TEST CASE:", y,   "   ", getapi,  "Passed"
			getapi = str(getapi)
			y = str(y)
			gen_report.write("<tr><td align='center'>" + y + "</td><td>" + getapi + "</td> <td bgcolor='#99e26f'>Passed </td></tr>")
			passed+=1
			y = int(y)
			y+=1
		else:
			endvalue = results.find("lb=") 
			endvalue2 = results.find("rc")
			strtvalue = results.rfind('', 0, endvalue)
			strtvalue2 = results.rfind('', 0, endvalue2)
			getapi = results[strtvalue:strtvalue2].replace('lb=','').replace('"','')
			print "TEST CASE:", y,   "   ", getapi,  "Failed"
			getapi = str(getapi)
			y = str(y)
			gen_report.write("<tr><td align='center'>" + y + "</td><td>" + getapi + "</td> <td bgcolor='#e06745'>Failed </td></tr>")
			failed+=1
			y = int(y)
			y+=1
			
		print "Passed: ", passed
		print "Failed: ", failed
		getcontext().prec = 3
		percentage = Decimal(passed) / Decimal(testcases) * 100 
		totalper = str(percentage) + '%'
		gen_report.write("</table><table align='center'> <tr><td><h3>Passed: " + totalper + "</h3></td></tr> </table>")
			
	else:	
		getcontext().prec = 3
		percentage = 0
		set_API_NA = "N/A"
		totalper = str(percentage) + '%'		  
		gen_report.write("</table><table align='center'> <tr><td><h3>Passed: " + set_API_NA + "</h3></td></tr> </table>")	
		  

#api_result------------------------------------------------------------------------------==========================
	api_result = open("api_result.html","a")
	api_result.write("<center><h1>Inbound Build Acceptance Automation</h1> <h3>API</h3></center>")
	api_result.write("<br/> <table border='1' width='70%' align='center' width='35%'> <tr><td align='center' bgcolor='#c2c4c6' width='10%'> <b>Test Case</b> </td> <td align='center' bgcolor='#c2c4c6' width='40%'> <b>API </b></td> <td align='center' bgcolor='#c2c4c6'><b>Response Code</td>  <td align='center' bgcolor='#c2c4c6'><b>Response Message</td> <td align='center' bgcolor='#c2c4c6' width='20%'> <b>Result</b></td></tr>")


	cc = 1
	for extractor in gettestcases:
		endvalue_rc = extractor.find("rc=") 
		endvalue2_rc = extractor.find("rm")
		strtvalue_rc = extractor.rfind('', 0, endvalue_rc)
		strtvalue2_rc = extractor.rfind('', 0, endvalue2_rc)
		get_rc = extractor[strtvalue_rc:strtvalue2_rc].replace('rc=','').replace('"',' ').strip()
		print get_rc

		endvalue_rm = extractor.find("rm=") 
		endvalue2_rm = extractor.find("tn")
		strtvalue_rm = extractor.rfind('', 0, endvalue_rm)
		strtvalue2_rm = extractor.rfind('', 0, endvalue2_rm)
		get_rm = extractor[strtvalue_rm:strtvalue2_rm].replace('rm=','').replace('"',' ').strip()
		print get_rm

		endvalue_lb = extractor.find("lb=") 
		endvalue2_lb = extractor.find("rc")
		strtvalue_lb = extractor.rfind('', 0, endvalue_lb)
		strtvalue2_lb = extractor.rfind('', 0, endvalue2_lb)
		get_lb = extractor[strtvalue_lb:strtvalue2_lb].replace('lb=','').replace('"',' ').strip()
		print get_lb

		if ('rc="200"' in extractor) and ('rm="OK"' in extractor):
			cc = str(cc)
			api_result.write("<tr><td align='center'>" + cc + "</td><td>" + get_lb + "</td> <td>" + get_rc + "</td> <td>" + get_rm + "</td> <td bgcolor='#99e26f'>Passed </td></tr>")
			cc = int(cc)
			cc+=1
		else:
			cc = str(cc)
			api_result.write("<tr><td align='center'>" + cc + "</td><td>" + get_lb + "</td> <td>" + get_rc + "</td> <td>" + get_rm + "</td> <td bgcolor='#e06745'>Failed </td></tr>")
			cc = int(cc)
			cc+=1
#api_result------------------------------------------------------------------------------=============================
	endtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')#time
	opentime = open("writetime.txt", "r")
	for gettime in opentime:
		if "Start Time" in gettime:
			starttime = gettime[12:].strip()
		if "Call flow Percentage" in gettime:
			cflow_per = gettime[22:].replace('%','').strip()
		if "TransferType Percentage" in gettime:
			ttype_per = gettime[25:].replace('%','').strip()

#new code for computation (normal average)
	check_len_cflow = len(cflow_per)
	check_len_ttype = len(ttype_per)
	percentage_temp_str = str(percentage)
	check_len_api = len(percentage_temp_str)
	if check_len_cflow == 0:
		cflow_per = 0
	if check_len_ttype == 0:
		ttype_per = 0
	if check_len_api == 0:
		percentage = 0

	if check_len_cflow!=0 and check_len_ttype!=0 and percentage>=1:
		getcontext().prec = 3
		cflow_per = Decimal(cflow_per)
		ttype_per = Decimal(ttype_per)
		percentage = Decimal(percentage)
		print "CHECK CHECK CHECK: ", cflow_per, ttype_per, percentage
		overallsum = cflow_per + ttype_per + percentage 
		overall_percentage = Decimal(overallsum) / 3
		overall_percentage_str = str(overall_percentage) + '%'
		gen_report.write("<html><table align='center' border='1' width='80%'> </table>")
		gen_report.write("<br/><center><font size='7'><b>" + overall_percentage_str + "</b></font></center>")

	if check_len_cflow!=0 and check_len_ttype!=0 and percentage<=0:
		getcontext().prec = 3
		cflow_per = Decimal(cflow_per)
		ttype_per = Decimal(ttype_per)
		percentage = Decimal(percentage)
		print "CHECK CHECK CHECK: ", cflow_per, ttype_per, percentage
		overallsum = cflow_per + ttype_per + percentage 
		overall_percentage = Decimal(overallsum) / 2
		overall_percentage_str = str(overall_percentage) + '%'
		gen_report.write("<html><table align='center' border='1' width='80%'> </table>")
		gen_report.write("<br/><center><font size='7'><b>" + overall_percentage_str + "</b></font></center>")
	
	if overall_percentage >= 75:
		gen_report.write("<table align='center'><tr><td bgcolor='#99e26f'>  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  </td> <td>&nbsp;&nbsp;&nbsp;&nbsp;<font size='4'><b>PASSED</b></font></table><br/>")
	else:
		gen_report.write("<table align='center'><tr><td bgcolor='#e06745'>  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  </td> <td>&nbsp;&nbsp;&nbsp;&nbsp;<font size='4'><b>FAILED</b></font></table><br/>")

	gen_report.write("<table align='center' border='1' width='35%'> <tr><td> <b>Start Time:</b></td> <td>" + starttime +  "</td></tr>"
		 "<tr><td><b>End Time:</b></td> <td>" + endtime + "</td></tr>"
		 "<tr><td> <b>Log File:</b></td><td>report.html</td></tr> </table>")
		
if __name__ == "__main__":
	main()
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
	api_report()
