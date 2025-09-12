FOLDER_PATH = "./processed_data/"

def file_name_builder(folder_path, file_prefix, file_extension, index=None):
  index_part = ""
  if index != None:
    index_part = f"_{index:02d}"
  return f"{folder_path}{file_prefix}{index_part}.{file_extension}"
