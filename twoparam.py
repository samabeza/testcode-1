import os
import os.path
import sys

def main(foldername):
  for arg in sys.argv[1:]:
    data_path=arg
    return data_path


if __name__ == "__main__":
  if len(sys.argv)==0:
    print("Please pass foldername as argument")
    exit()
foldername=sys.argv[1]
usedby=sys.argv[2]
main (foldername)
testpath = main(foldername)
print testpath
print usedby
