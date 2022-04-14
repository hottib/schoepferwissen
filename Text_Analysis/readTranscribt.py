import os, glob

def convert2text(searchFolder):
    os.chdir(searchFolder)
    files = glob.glob("*.transcript")

    for file in files: 
        with open (file, "r") as f:
            data =  f.read()
        newFilename = str(file + ".txt")
        with open (newFilename, "w", encoding="utf-8") as f: 
            f.write(data)


convert2text("DATA")