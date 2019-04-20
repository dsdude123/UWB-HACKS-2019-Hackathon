from zipfile import ZipFile
import os
import json


def traverse_zip(filename):
    with ZipFile(filename, 'r') as zip:
        print(zip.namelist())
        print(type(zip))
        to_json(zip.namelist())

def to_json(path_list):
    for i in range(len(path_list)):
        path_list[i] = {"path":path_list[i]} 
    json_file = open("paths.json", 'w')
    json.dump({"files":path_list},json_file)


if __name__ == '__main__':
    traverse_zip()
    #start_Path()

