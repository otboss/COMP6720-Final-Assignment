import service.crud.read

def show_databases(working_directory: str) -> list[str]:
  return service.read.show_databases(working_directory)
