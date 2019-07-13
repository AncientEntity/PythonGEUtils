import os, sys, shutil

def ExportGameWindows(fileLocation):
    """
    ExportGameWindows() allows you to export your python game into
    an EXE file.
    """
    splittedDirectory = fileLocation.split("\\")
    for pos in range(len(splittedDirectory)-1):
        splittedDirectory[pos] = splittedDirectory[pos]+"\\"
    exportLocation = "".join(splittedDirectory[0:len(splittedDirectory)-1])
    sys.path.append(exportLocation)
    #os.mkdir(exportLocation+"\\"+splittedDirectory[len(splittedDirectory)-1]+" Export")

    fullOriginDirectory = "".join(splittedDirectory[0:len(splittedDirectory)])
    #print(splittedDirectory)
    os.system("pyinstaller \""+fileLocation+"\"")

    thisDir = os.path.dirname(os.path.realpath(__file__))
    targetDir = os.listdir(thisDir+"\\dist")[0]


    #Now move assets to export
    print("--------Complete Walk")
    for f in os.walk(exportLocation):
        print(f)
    print("--------Complete Walk End")
    
    for folder in os.walk(exportLocation):
        #print("======",folder[0])
        for file in folder[2]: #0=directory,1=folders,2=files
            if(file.split(".")[::-1][0] == "py" or file.split(".")[::-1][0] == "pyc"):
                print("Ignoring File: "+file)
                continue
            try:
                shutil.copyfile(folder[0]+"\\"+file,thisDir+"\\dist\\"+targetDir+"\\"+file)
                print("Copied File: " + file)
            except:
                print("Error Copying: ",file)
        #print("======")
    
    os.rename(thisDir+"\\dist\\"+targetDir,exportLocation+"GameExport\\GameData")
    os.rmdir(thisDir+"\\dist")
    shutil.rmtree(thisDir+"\\build")

    print("GAME EXPORT COMPLETE")

              
#ExportGameWindows("C:\\Users\\user\\Desktop\\My Programs\\Python\\PythonGameEngine\\PythonGEUtils\\TheEngine\\PythonGEUtils\\examples\\WallBreaker.py")

