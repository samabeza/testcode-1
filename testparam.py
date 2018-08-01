import sys
import os
import glob
import subprocess
import csv
from decimal import *
from datetime import datetime

def main(foldername):
    try:
        file = os.stat(foldername+"/Data File.csv")
        if file.st_size == 0:
            print "Data File is Empty"
    except OSError:
        print "Data File.csv not Found"
        sys.exit(1)

if __name__ == "__main__":
	if len(sys.argv)==0:
		print("please pass folder name as argument")
		exit()
	foldername=sys.argv[1]
	print('foldername==>{}'.format(foldername) )
	main(foldername)
