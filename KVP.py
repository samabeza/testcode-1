import csv

def excel():
	with open('Data File.csv','rb') as f:
		reader = csv.reader(f)
		next(reader, None)
		for line in reader:
			transferterm=line[1]
			calllog=line[2]
			transfers = transferterm
			run(transfers,calllog)
			
			
def run(transfers,calllog):
	arr_logs = set()
	terms = transfers.split(';') #SPLIT Transfer Term per line in csv (delimiter = ;)
	total_terms = len(terms) # Count number of TERMS
	terms = str(terms).replace(",''","") #Remove unnecessary characters
	match = 0
	total_terms-=1 #magic
	print "Terms to check: ", terms
	
	count = 1
	print "Number of terms to check: ", total_terms	
	
	
	spl_term_val = terms.split('=')
	value_counter = 1 #magic 1
	term_counter = 0 #magic 2
		
	with open (calllog,"r") as call_log:
		for line in call_log:
			arr_logs.add(line + "\n")	
		
	while count <= total_terms:
		x = str(spl_term_val).split(',')
		final_term = x[term_counter].replace('["[','').replace('\\','').replace('"','').replace("'n",'').replace("'","").strip()
		final_value = x[value_counter].replace("'","").replace('"','').strip()
		
		print "KEY: ",final_term,"in Call Log: ", calllog, "with VALUE: ", final_value
		
		for b in arr_logs:
			if final_term.lower() in b.lower():
				terms_found = b
				print terms_found
				
				if final_value.lower() in terms_found.lower():
					match +=1

		
		if match != 0:
			print "Match"
		else:
			print "No Match"
		print "\n----------------------------------------\n"
		
		count+=1
		value_counter+=2 #magic 1
		term_counter+=2 #magic 2
		
		
	print "\n----------------------------------------\n"
			
if __name__== "__main__":
	excel()
	
	
	
	
	




