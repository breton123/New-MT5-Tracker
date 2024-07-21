import os
import chardet

def findChartPath(profilePath, magic):
     paths = []
     for chart in os.listdir(profilePath):
          chartFile = os.path.join(profilePath, chart)
          with open(chartFile, 'r', encoding=detect_encoding(chartFile)) as file:
               lines = file.readlines()
          for line in lines:
               if "MAGIC_NUMBER=" in line:
                    magicNumber = line.split("MAGIC_NUMBER=")[1]
                    if int(magicNumber) == int(magic):
                         paths.append(chartFile)
                         
     return paths
               
def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read()
    result = chardet.detect(raw_data)
    return result['encoding']