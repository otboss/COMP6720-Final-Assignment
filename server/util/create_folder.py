import os 

global workingDir
baseLocation = 'server/'

def createWorkingDir(workingDir):
    os.mkdir(baseLocation+workingDir)
    file = open("workingDirectory.txt", "w")
    file.write(workingDir)
    file.close()

        
def createsubFolder(folderName):
    subPath = workingDir + "\\" + folderName
    os.mkdir(subPath)
       