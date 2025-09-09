from pptx import Presentation
import zipfile
import os

processed_data_folder_path = './processed_data/'
raw_data_folder_path = "./raw_data/"

def extract_images_from_pptx(input_path, output_folder):

    # Open pptx as zip
    with zipfile.ZipFile(input_path, "r") as pptx:
        # Look for files inside ppt/media/
        for file_name in pptx.namelist():
            if file_name.startswith("ppt/media/"):
                # Extract the image
                image_data = pptx.read(file_name)
                image_path = os.path.join(output_folder, os.path.basename(file_name))
                with open(image_path, "wb") as f:
                    f.write(image_data)
                
def extract_images_from_folder(start_index, end_index):
    input_folder = raw_data_folder_path + "ppt/"
    output_parent_folder = processed_data_folder_path + "ppt_images/"
    input_file_prefix = "Eph"
    for i in range(start_index, end_index):
        input_path = input_folder + input_file_prefix + "_" + f"{i:02d}" + ".pptx"
        output_folder = output_parent_folder + "Eph_" + f"{i:02d}/"
        os.makedirs(output_folder, exist_ok=True)
        extract_images_from_pptx(input_path, output_folder)