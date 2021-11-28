import uuid

# Record : A block record where each ID is a uuid4 string
def Record(schema: list[str], values: list[str], id: str = str(uuid.uuid4())):
  result = { 'id': id }
  schema_without_id = schema[1:]
  for x in range(0, len(schema_without_id)):
    result[schema_without_id[x]] = values[x]
  return result