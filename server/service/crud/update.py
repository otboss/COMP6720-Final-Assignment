import util.crud_helpers as helper
import os
import util.binary_io as file_helper
import util.working_directory
import json


def update_records(database: str, table_name: str, fields: list[str], values: list[str], filters: str = ""):
    working_dir = util.working_directory.load_working_directory()
    table_path = working_dir + '/' + database + '/' + table_name

    if os.path.exists("%s.bin"%(table_path)):
        #get file contents
        
        contents = file_helper.read_from_binary_file(table_path)
        contents_dict = json.loads(contents) #convert contents from json to dictionary

        #break down conditions into a list
        conditions_list =  helper.create_conds_lst(filters[0].split() if len(filters) > 0 else [])

        #creating a dict with the fields to be updated along with their respective values
        update_dict = {fields[i]: values[i] for i in range(len(fields))}

        #Evaluate each record      
        for block in contents_dict["data_items"]:
          for record in block["records"]:
            if len(conditions_list) != 0:
              result = helper.evaluate_conditions(conditions_list, record)
              if result:
                  for field in update_dict.keys():
                      record[field] = update_dict[field]  # updating record
            else:
              for field in update_dict.keys():
                record[field] = update_dict[field]  # updating record
        file_helper.write_to_binary_file(table_path, json.dumps(contents_dict))

    else:
        raise Exception("Table Does not Exist")  



def alter_table():
  # TODO: Implement alter table support
  pass
