import sys
import os
import glob
import subprocess
import csv
failed = 0
def main():
    try:
        file = os.stat("Data File.csv")
        if file.st_size == 0:
            print "Data File is Empty"
    except OSError:
        print "Data File.csv not Found"
        sys.exit(1)


def compare(calllog1, callflow1, y, gen_Report):


	global failed
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
	x= 0
	z=0
	y =str(y)
	print "\nTest "+ y+ ": List of Expected Verbiage:"
	while x < countlist:
		if promptlist[x] in verbiage:
			print promptlist[x] + " Found"
			#gen_Report.write("<tr><td>" + y + "</td><td>" + promptlist[x] + "</td>")
			x+=1
		else:
			print promptlist[x] + " Not Found"
			#gen_Report.write("<tr><td>" + promptlist[x] + "</td>")
			x+=1
			z = 1
			failed = 1
	verbi ='<br/>'.join(verbiage)
	prompi = '<br/>'.join(promptlist)
	if z == 1:
		print "                   STATUS: FAILED"
		gen_Report.write("<tr><td>" + y + "</td><td>" + prompi + "</td> <td>" + verbi + "</td> <td bgcolor='#e06745'>Failed</td>  <td>" + calllog1 + "</td></tr>")
	
	else:
		print "                   STATUS: PASSED"
		gen_Report.write("<tr><td>" + y + "</td><td>" + prompi + "</td> <td>" + verbi + "</td> <td bgcolor='#99e26f'>Passed</td>  <td>" + calllog1 + "</td></tr>")
		
	if flag == 0:
		print "\nTest "+ y + ": Calllog does not contain any .wav file "+ calllog1
	if flag ==1:
		print "\nTest "+ y+ ": List of Verbiage hit by Calllogs for " + calllog1 +":"
		print '\n'.join(verbiage)
		# print y


def excel():
	gen_Report = open("report.html", "a")
	#gen_Report.write("<html><table align ='center'"
					# "style='background-color:orange;'> "
					# "<style>table, th, td {border: 1px solid black;}</style>"
					# "<h1 >Build Acceptance Test</h1><p>Call Flow</p>")
	gen_Report.write("<html><table align ='center' bgcolor='orange' border='1'> <h1>Build Acceptance Test</h1> <p>Call Flow</p>")
	z= 0
	with open('Data File.csv', 'rb') as f:
		reader = csv.reader(f)
		next(reader, None)
		y= 1;
		gen_Report.write("<tr><td> Test Case </td> "
						 "<td> Expected Verbiage </td> "
						 "<td> Verbiage Found </td> "
						 "<td> Result </td> "
						 "<td>Call Log </td></tr>")
		for line in reader:
			callflow1 =line[0]
			calllog1 = line[2]
			if len(callflow1) >= 10:
				if len(calllog1)>= 10:
					compare(calllog1, callflow1, y, gen_Report)
					y+=1
if __name__ == "__main__":

    main()
    excel()
    if failed == 1:
        print"\n\n\n"
        raise SystemError('One of the Test Cases Failed')
