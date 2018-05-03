
def eval_func(dataset_file,processed_file):

    try: #IF CANNOT READ THE FILE, PRINT ERROR
        datasetFile = open(dataset_file,'r')
        processedFile = open(processed_file,'r')
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
        elif datasetData[i] == '\n' or processedData[i] == '\n':
            print ('EOF')
        else:
            print ('INVALID DATA EXISTS IN THE FILE(S), PLEASE CHECK')

    #print ('TRUE POSITIVE')
    #print (TruePositiveCounter)
    #print ('TRUE NEGATIVE')
    #print (TrueNegativeCounter)
    #print ('FALSE POSITIVE')
    #print (FalsePositiveCounter)
    #print ('FALSE NEGATIVE')
    #print (FalseNegativeCounter)

#print ('TPR = ' + TruePositiveCounter/(TrueNegativeCounter+FalseNegativeCounter+FalsePositiveCounter)) #TRUE POSITIVE RATE

    datasetFile.close()
    processedFile.close()
    output_file = open(processed_file+".eval", "w")
    output_file.write("TRUE POSITIVE = " + str(TruePositiveCounter) )
    output_file.write("\nTRUE NEGATIVE = " + str(TrueNegativeCounter) )
    output_file.write("\nFALSE POSITIVE = " + str(FalsePositiveCounter) )
    output_file.write("\nFALSE NEGATIVE = " + str(FalseNegativeCounter) )
    output_file.close()
    quit()


#eval_func('True_Evaluation.txt','Processed_Evaluation.txt')
