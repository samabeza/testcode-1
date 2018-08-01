import sys
import os

def main(foldername):
    # print command line arguments
    for arg in sys.argv[1:]:
        print arg

if __name__ == "__main__":
    if len(sys.argv)==0:
            print("Please pass foldername as argument")
            exit()
    foldername=sys.argv[1]
    main(foldername)
    
