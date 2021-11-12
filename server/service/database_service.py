import crud.read

def show_databases(working_directory: str) -> list[str]:
  return crud.read.show_databases(working_directory)