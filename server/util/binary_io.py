import os

def write_to_binary_file(file_name: str, text: str):
  file = open("%s.bin"%(file_name), "wb")
  file.write(text.encode())
  file.close()

def append_to_binary_file(file_name: str, text: str):
  file = open("%s.bin"%(file_name), "ab")
  file.write(text.encode())
  file.close()

def read_from_binary_file(file_name: str) -> str:
  file = open("%s.bin"%(file_name), "rb")
  contents = file.read().decode('ascii')
  file.close()
  return contents

def delete_binary_file(file_name: str) -> str:
  try:
    os.remove("%s.bin"%(file_name))
  except Exception as e:
    print(str(e))