import numpy as np

datasetFile = open('001_sleepyCombination_drowsiness.txt','r')
processedFile = open('001_sleepy.txt','r')

datasetData = datasetFile.read()
processedData = processedFile.read()

datasetCounter = 0
processedCounter = 0

for i in range(0, len(datasetData)):
    if datasetData[i] == '1':
        datasetCounter += 1

for i in range(0, len(processedData)):
    if processedData[i] == '1':
        processedCounter += 1

print 'Ones in dataset file:',datasetCounter
print 'Ones in processed file:', processedCounter

