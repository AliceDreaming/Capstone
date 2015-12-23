import sys


def write_to_file(contentStr, fileName):
	if(contentStr.endswith(",")):
		contentStr=contentStr[:-1]
	outFile = open(fileName, "w")
	outFile.writelines(contentStr)
	outFile.close()

def main():
        args = sys.argv
        if len(args) < 4:
                print("Please provide sufficient paramters. Following parameters should be provided:\n 1. source test case list\n 2. destination test list folder\n 3. maximum number of test cases each list file contains\n")
                quit()

        sourceFile = args[1]
        destFolder = args[2]
        if(destFolder.endswith("\\")):
                destFolder=destFolder[:-1]
                
        limit = int(args[3])
        recCount=0
        fileNo=1
        fileName = destFolder + "\\TestList{}".format(fileNo) + ".txt"
        
        with open(sourceFile) as f:
                lines = f.readlines()
                testList="TestList="
                lineNum = len(lines)
                print(lineNum)
                for  i in range(4,lineNum):
                        line = lines[i].strip()
                        if line != '':
                                testList = testList + lines[i].strip() + ","
                                recCount+=1
                        if recCount >= limit:
                                write_to_file(testList, fileName)			
                                testList="TestList="
                                recCount=0
                                fileNo +=1
                                fileName=destFolder + "\\TestList{}".format(fileNo) + ".txt"
                
                if testList != '':
                        write_to_file(testList, fileName)


if __name__ == "__main__":
        main()
