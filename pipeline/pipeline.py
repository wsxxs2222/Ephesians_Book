import sys
import ppt_to_title_object as ptt
import ppt_to_images as pti
import sentence_to_block as stb
import match_title_and_content as match
import title_content_to_latex as to_latex 

def run_pipeline(start_index, end_index):
    ptt.convert_ppt_files_to_title_json(start_index, end_index)
    pti.extract_images_from_folder(start_index, end_index)
    stb.process_sentence_in_files(start_index, end_index)
    match.update_content_json_files_with_matched_titles(start_index, end_index)
    to_latex.convert_folder_files(start_index, end_index)
    
if __name__ == "__main__":
    # print("hello")
    # if len(sys.argv) != 3:
    #     raise Exception("invalid number of arguments, usage: start_file_index, end_file_index")
    # start_index = int(sys.argv[1])
    # end_index = int(sys.argv[2])
    # run_pipeline(start_index, end_index)
    
    run_pipeline(2, 6)