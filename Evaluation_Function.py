import numpy as np

#MAYBE TAKE FILE NAMES AS INPUT?


try: #IF CANNOT READ THE FILE, PRINT ERROR
    datasetFile = open('True_Evaluation.txt','r')
    processedFile = open('Processed_Evaluation.txt','r')
except IOError:
    print ('CANNOT OPEN ONE OR MANY FILES')
    quit()

datasetData = datasetFile.read()
processedData = processedFile.read()

TruePositiveCounter = 0
TrueNegativeCounter = 0
FalsePositiveCounter = 0
FalseNegativeCounter = 0

if len(datasetData) != len(processedData):
    print ('FILE LENGTHS DO NOT MATCH, QUITTING!')
    quit()


for i in range(0, len(datasetData)):
    if datasetData[i] == '1' and processedData[i] == '1':
        TruePositiveCounter += 1
    elif datasetData[i] == '0' and processedData[i] == '0':
        TrueNegativeCounter += 1
    elif datasetData[i] == '0' and processedData[i] == '1':
        FalsePositiveCounter += 1 
    elif datasetData[i] == '1' and processedData[i] == '0':
        FalseNegativeCounter += 1
    else:
        print ('INVALID DATA EXISTS IN THE FILE(S), PLEASE CHECK')


print 'TRUE POSITIVE'
print TruePositiveCounter

print 'TRUE NEGATIVE'
print TrueNegativeCounter


print 'FALSE POSITIVE'
print FalsePositiveCounter

print 'FALSE NEGATIVE'
print FalseNegativeCounter

#print ('TPR = ' + TruePositiveCounter/(TrueNegativeCounter+FalseNegativeCounter+FalsePositiveCounter)) #TRUE POSITIVE RATE


datasetFile.close()
processedFile.close()

quit()
