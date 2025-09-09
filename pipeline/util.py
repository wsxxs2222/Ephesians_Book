FOLDER_PATH = "./processed_data/"

def file_name_builder(folder_path, file_prefix, file_extension, index):
  return f"{folder_path}{file_prefix}_{index:02d}.{file_extension}"
