from zipfile import ZipFile
import os

def traverse_and_backup(path, subdir):
    for filename in os.listdir(path):
        filePath = path + "/" + filename
        if os.path.isdir(filePath):
            tempSubDir = ""
            if subdir:
                tempSubDir = subdir + "/" + filename
            else:
                tempSubDir = filename
            traverse_and_backup(filePath, tempSubDir)
        else:
            print(filename, subdir)


def start_Path():
    print("Traversing the current directory...")
    traverse_and_backup(os.getcwd(), "")


def traverse_zip():
    filename = "ThreadOS.zip"
    with ZipFile(filename, 'r') as zip:
        print(zip.namelist())
        print(type(zip))

if __name__ == '__main__':
    traverse_zip()
    #start_Path()
