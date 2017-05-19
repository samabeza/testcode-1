import os

y = os.path.abspath("./HTTP Request.jmx")
z = y.replace('\\','\\\\') 


initial_path = "jmeter -J jmeter.save.saveservice.output_format=xml -n -t"
command = "-l HTTPRequest.jtl"
print "PATH: ", y
print "INITIAL_PATH: ", initial_path

final = initial_path + " " + z + " " + command
print final

os.system(final)
