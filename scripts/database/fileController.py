

import json
import os
import portalocker
import gzip


def write(file_path, content):
     with open(file_path, "w+") as file:
          try:
               portalocker.lock(file, portalocker.LOCK_EX)
               json.dump(content, file, indent=4)
               file.flush()  # Ensure all data is written to disk
               os.fsync(file.fileno())
          finally:
               portalocker.unlock(file)

def read(file_path):
     with open(file_path, "r") as file:
          try:
               portalocker.lock(file, portalocker.LOCK_SH)
               content = json.load(file)
          finally:
               portalocker.unlock(file)
               return content

def rread(file_path):
     if ".gz" not in file_path:
          file_path = compressFile(file_path)
     with gzip.open(file_path, 'rt', encoding='utf-8') as file:
          json_data = file.read()
          data = json.loads(json_data)
          return data

def wwrite(file_path, content):
     if ".gz" not in file_path:
          file_path = compressFile(file_path)
     with gzip.open(file_path, 'wt', encoding='utf-8') as file:
          file.write(str(content))
          file.flush()
          os.fsync(file.fileno())

def compressFile(file_path):
     json_data = rread(file_path)
     with gzip.open(file_path+".gz", 'wt', encoding='utf-8') as gz:
          gz.write(str(json_data))
          gz.flush()
          os.fsync(gz.fileno())
     return file_path+".gz"