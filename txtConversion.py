
inputName = '009_sleepyCombination_drowsiness'
convertedFile = open(inputName+'.txt','a')

startFrame = [436,1023,1444,1818,2267,2811]
endFrame = [611,1334,1559,2007,2548,2884]

frameCounter = 1

for i in range(0, len(startFrame)):    
    while frameCounter < startFrame[i]:
       convertedFile.write('0')
       frameCounter += 1
    while frameCounter <= endFrame[i]:
        convertedFile.write('1')
        frameCounter += 1

convertedFile.close()
