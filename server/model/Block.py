
from typing import List
from Record import  Record


class Block:
  records: List[List] = []

  def add_record(self, record: Record):
    if(len(self.records) >= 5):
      raise Exception("block full") 
      
    self.records.append(record.to_list())