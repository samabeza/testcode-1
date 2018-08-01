import sys
import os

def main(foldername):
    # print command line arguments
    for arg in sys.argv[1:]:
        data_path=arg
        #print data_path
        #os.system("dir")
        global testpath
        testpath = "dir" + " " + data_path + "/"
        return testpath

def getdirbyparam(testpath):
    print testpath 
        
if __name__ == "__main__":
    if len(sys.argv)==0:
            print("Please pass foldername as argument")
            exit()
    foldername=sys.argv[1]
    main(foldername)
    testpath = main()
    getdirbyparam(testpath)
