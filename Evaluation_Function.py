import numpy as np

#MAYBE TAKE FILE NAMES AS INPUT?


try: #IF CANNOT READ THE FILE, PRINT ERROR
    datasetFile = open('001_sleepyCombination_drowsiness.txt','r')
    processedFile = open('001_sleepy.txt','r')
except IOError 
    print 'CANNOT OPEN ONE OR MANY FILES'
    quit

datasetData = datasetFile.read()
processedData = processedFile.read()

TruePositiveCounter = 0
TrueNegativeCounter = 0
FalsePositiveCounter = 0
FalseNegativeCounter = 0

if len(datasetData) != len(processedData)
    print 'FILE LENGTHS DO NOT MATCH, QUITTING!'
    quit


for i in range(0, len(datasetData)):
    if datasetData[i] == '1' and processedData[i] == '1':
        TruePositiveCounter += 1
    elif datasetData[i] == '0' and processedData[i] == '0':
        TrueNegativeCounter += 1
    elif datasetData[i] == '0' and processedData[i] == '1':
        FalsePositiveCounter += 1 
    elif datasetData[i] == '1' and processedData[i] == '0':
        FalseNegativeCounter += 1
    else 
        print 'INVALID DATA EXISTS IN THE OUTPUT FILE(S), PLEASE CHECK'


print 'TP = ' + TruePositiveCounter '\n'
print 'TN = ' + TrueNegativeCounter '\n'
print 'FP = ' + FalsePositiveCounter '\n'
print 'FN = ' + FalseNegativeCounter '\n'


datasetFile.close()
processedFile.close()

quit