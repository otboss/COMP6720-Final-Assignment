
def write_to_binary_file(file_name: str, text: str):
  file = open("%s.bin"%(file_name), "wb")
  file.write(text.encode())
  file.close()

def read_from_binary_file(file_name: str):
  file = open("%s.bin"%(file_name), "rb")
  contents = file.read().decode('ascii')
  file.close()
  return contents