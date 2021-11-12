from Block import Block
#A file is basically a table, one is created whenever a table is created
class File:
    def __init__ (self, table_Name):
      self.data_items = [] #the list that will hold everything
      self.table_Name = table_Name
    
    def table_str(self, fieldNames):
        col =[] #the list for column header
        for i in fieldNames:
            col.append(i)
        self.data_items.append(col)
    def add_blocks(self,blocks): # blocks is a list of records, where each record is a list
        for i in blocks:
          self.data_items.append(i) # the file is created as a list of lists where the first list is the column headers
        
