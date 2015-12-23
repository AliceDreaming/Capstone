import os
import os.path
import sys
import glob
from StringIO import StringIO
import xml.etree.ElementTree as ET

def main():
    args = sys.argv
    if len(args)< 3:
            print("Please provide the report folder and the combined report file full path.")

    files = args[1]
    if files.endswith("\\"):
        files = files[:-1]
    combinedReport = args[2]
    combinedReport = combinedReport.lower()
    if not combinedReport.endswith(".trx"):
        print("Can only merge to trx report, please provide a file path with trx extension")
        quit()        
    if os.path.isfile(combinedReport):
        os.remove(combinedReport)

    # If there no document or only one document in the folder,
    # there is no need to merge
    trx_files = glob.glob(files +"\\*.trx")
    if(len(trx_files) <= 1):
              quit()
              
    print("Report files to merge:")
    for file in trx_files:
              print(file)          

    # Use the first one as the scheme, append nodes in other report to this one
	# later we will save the final result to the combined report
    merged_file = ET.parse(trx_files[0])
    testRun = merged_file.getroot()
    namespaces = {'resp': 'http://microsoft.com/schemas/VisualStudio/TeamTest/2010'}
    resultSummary = testRun.find("resp:ResultSummary", namespaces=namespaces)
    if resultSummary is None:
            print("Error! No result summary found!")
            quit()
            
    counter = resultSummary.find("resp:Counters", namespaces=namespaces)
    if counter is None:
              print('Error! No counters for result summary found')
              quit()
              
    # Get values from the counter. Here is an example of the counter content:
    # <Counters pending="0" inProgress="0" completed="0" warning="0" disconnected="0"
    # notExecuted="0" notRunnable="0" passedButRunAborted="0" inconclusive="0" aborted="0"
    # timeout="0" failed="0" error="0" passed="4" executed="4" total="4"/>
    pending = int(counter.get("pending"))
    inProgress = int(counter.get("inProgress"))
    completed = int(counter.get("completed"))
    warning = int(counter.get("warning"))
    disconnected = int(counter.get("disconnected"))
    notExecuted = int(counter.get("notExecuted"))
    notRunnable = int(counter.get("notRunnable"))
    passedButRunAborted = int(counter.get("passedButRunAborted"))
    inconclusive = int(counter.get("inconclusive"))
    aborted = int(counter.get("aborted"))
    timeout = int(counter.get("timeout"))
    failed = int(counter.get("failed"))
    error = int(counter.get("error"))
    passed = int(counter.get("passed"))
    executed = int(counter.get("executed"))
    total = int(counter.get("total"))

    print(trx_files[0])
    print("total:{}".format(total))
    print("passed:{}".format(passed))
    print("failed:{}".format(failed))

    testDefinictions_array = testRun.find("resp:TestDefinitions", namespaces=namespaces).getchildren()
    if len(testDefinictions_array) <=0:
              print('Error! No test definitions found.')
              quit()
              
    testEntries_array = testRun.find("resp:TestEntries", namespaces=namespaces).getchildren()
    if len(testEntries_array) <= 0:
            print('Error! No test entries found!')
            quit()

    results_array = testRun.find("resp:Results", namespaces=namespaces).getchildren()
    if len(results_array) <= 0:
            print('Error! No results found!')
            quit()
            
    for index in range(1, len(trx_files)):
              file = ET.parse(trx_files[index])
              print(trx_files[index])
              testRun_1 = file.getroot()

              resultSummary_1 = testRun_1.find("resp:ResultSummary", namespaces=namespaces)
              counter_1 = resultSummary_1.find("resp:Counters", namespaces=namespaces)
              pending += int(counter_1.get("pending"))
              inProgress += int(counter_1.get("inProgress"))
              completed += int(counter_1.get("completed"))
              warning += int(counter_1.get("warning"))
              disconnected += int(counter_1.get("disconnected"))
              notExecuted += int(counter_1.get("notExecuted"))
              notRunnable += int(counter_1.get("notRunnable"))
              passedButRunAborted += int(counter_1.get("passedButRunAborted"))
              inconclusive += int(counter_1.get("inconclusive"))
              aborted += int(counter_1.get("aborted"))
              timeout += int(counter_1.get("timeout"))
              failed += int(counter_1.get("failed"))
              error += int(counter_1.get("error"))
              passed += int(counter_1.get("passed"))
              executed += int(counter_1.get("executed"))
              total += int(counter_1.get("total"))

              print("total:" + counter_1.get("total"))
              print("passed:" + counter_1.get("passed"))
              print("failed:" + counter_1.get("failed"))
              
              testDefinictions_array_1 = testRun_1.find("resp:TestDefinitions", namespaces=namespaces).getchildren()
              testEntries_array_1 = testRun_1.find("resp:TestEntries", namespaces=namespaces).getchildren()
              results_array_1 = testRun_1.find("resp:Results", namespaces=namespaces).getchildren()

              for definition in testDefinictions_array_1:
                        testDefinictions_array.append(definition)

              for entry in testEntries_array_1:
                        testEntries_array.append(entry)

              for result in results_array_1:
                        results_array.append(result)

    counter.set("pending", str(pending))
    counter.set("inProgress", str(inProgress))
    counter.set("completed", str(completed))
    counter.set("warning", str(warning))
    counter.set("disconnected", str(disconnected))
    counter.set("notExecuted", str(notExecuted))
    counter.set("notRunnable", str(notRunnable))
    counter.set("passedButRunAborted", str(passedButRunAborted))
    counter.set("inconclusive", str(inconclusive))
    counter.set("aborted", str(aborted))
    counter.set("timeout", str(timeout))
    counter.set("failed", str(failed))
    counter.set("error", str(error))
    counter.set("passed", str(passed))
    counter.set("executed", str(executed))
    counter.set("total", str(total))

    if os.path.isfile(files +"\\temp.trx"):
            os.remove(files +"\\temp.trx")            
    merged_file.write(files +"\\temp.trx")
    correct_data = open(files +"\\temp.trx").read().replace('ns0:', '').replace(':ns0','')
    
    filewrite = open(combinedReport, 'w')
    filewrite.write(correct_data)
    filewrite.close()

    os.remove(files +"\\temp.trx")

    print(combinedReport)
    print("total:{}".format(total))
    print("passed:{}".format(passed))
    print("failed:{}".format(failed))

if __name__ == "__main__":
    main()
