import os

y = os.path.abspath("./HTTPRequest.jmx")
z = y.replace('\\','\\\\') 


initial_path = "jmeter -Jjmeter.save.saveservice.output_format=xml -n -t"
command = "-l HTTPRequest.jtl"
print "PATH: ", y
print "INITIAL_PATH: ", initial_path

final = initial_path + " " + z + " " + command
print final

#os.system(final)
