
def parseSetFile(file_path):
     with open(file_path, 'r') as file:
         all = file.read()
         all = all.split("\n")
     config = {}
     for line in all:
          if ";" not in line:
               try:
                    key, value = line.split("=")
                    value = value.split("|")[0]
                    config[key] = value
               except:
                    pass
     return config