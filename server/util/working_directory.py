import os 
import sys

db_path_file = "./db_path.txt"

def create_working_directory():
    working_directory_path: str = "./%s-db"%(sys.argv[1]) if len(sys.argv) > 1 else "./default-db"
    try:
        if os.access(working_directory_path[0:working_directory_path.rfind("/")], os.W_OK) == False:
            sys.exit("Provided working directory path not accessible")
        os.mkdir(working_directory_path)
    except Exception as e:
        print(str(e))
    file = open(db_path_file, "w")
    file.write(working_directory_path)
    file.close()

def load_working_directory() -> str:
    file = open(db_path_file, "r")
    working_dir_path = file.read()
    file.close()
    return working_dir_path

def create_sub_folder(folder_name):
    sub_path = load_working_directory() + "/" + folder_name
    os.mkdir(sub_path)

def create_index_folder(database: str, table_name: str):
    incides_folder_path = "%s/%s/indices/%s"%(load_working_directory(), database, table_name)
    os.mkdir(incides_folder_path)
       