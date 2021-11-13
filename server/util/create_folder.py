import os 



global workingDir

def createWorkingDir(workingDir) :
    isFile = os.path.isdir(workingDir)
    if isFile is False:
        print('Path not found!!!')
        question = input('Create Path [yes or no] : ')    
        if question.lower() == 'yes' or question.lower() == 'y':
            os.mkdir(workingDir)
            print('Path Successfully Created ', workingDir)
        else:
            print('Exiting Program.........')
            exit()

def createsubFolder(folderName) :
    if folderName:
        subPath = workingDir + "\\" + folderName
        os.mkdir(subPath)
        print('Path Successfully Created. ', subPath)


workingDir = input('Please enter Working Directory: ')
createWorkingDir(workingDir)

fName = "DB_Folder"
createsubFolder(fName)

