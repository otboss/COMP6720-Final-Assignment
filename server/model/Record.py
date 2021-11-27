import uuid

# Record : A block record where each ID is a uuid4 string
def Record(schema: list[str], values: list[str], id: str = str(uuid.uuid4())):
  result = { 'id': id }
  for x in range(0, len(schema)):
    result[schema[x]] = values[x]
  return result