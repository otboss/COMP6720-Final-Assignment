from Record import  Record

class Block:
  records: list[list] = []

  def add_record(self, record: Record):
    if(len(self.records) >= 5):
      raise Exception("block full") 

    self.records.append(record.to_list())