import os
from decimal import *
gen_report = open("report.html", "a")
gen_report.write("<html><table align='center' border='1' width='80%'> </table><center>  <h3>API</h3></center>")
gen_report.write("<br/> <table border='1' align='center' width='35%'> <tr><td align='center' bgcolor='#c2c4c6' width='10%'> <b>Test Case</b> </td> <td align='center' bgcolor='#c2c4c6' width='60%'> <b>API </b></td>""<td align='center' bgcolor='#c2c4c6' width='20%'> <b>Pass/Fail </b></td></tr>")

passed = 0
failed = 0
gettestcases = set()
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
getcontext().prec = 2
percentage = Decimal(passed) / Decimal(testcases) * 100
totalper = str(percentage) + '%'
gen_report.write("</table><br/><br/><table align='center'> <tr><td><h2>Passed: " + totalper + "</h2></td></tr> </table>")
