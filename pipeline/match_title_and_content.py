import json
import numpy as np
import re
import copy
import pprint
import util

def pair_lecture_content_final(titles, contents):
    """
    Pairs audio transcript segments with presentation bullet points using
    advanced heuristics for accuracy. (Version 3 - Definitive Logic)

    This version incorporates:
    1. A limited Search Window to prevent illogical jumps.
    2. A Contiguity Bonus to favor a natural, sequential slide progression.
    """
    # --- Parameters ---
    SIMILARITY_THRESHOLD = 0.45  # A balanced threshold
    MIN_TRANSCRIPT_LENGTH = 10
    SEARCH_WINDOW = 8  # **NEW**: Only look ahead this many titles for a match.

    # --- State Initialization ---
    modified_contents = copy.deepcopy(contents)
    search_start_index = 0

    # --- Main Loop ---
    for i, content_item in enumerate(modified_contents):
        transcript_text = content_item['content']
        if len(transcript_text) < MIN_TRANSCRIPT_LENGTH:
            modified_contents[i]['titleIndex'] = -1
            continue
        transcript_chars = set(transcript_text)
        
        candidates = []
        # Define the end of our search window for this specific transcript
        search_end_index = min(search_start_index + SEARCH_WINDOW, len(titles))

        for j in range(search_start_index, search_end_index):
            title_text = titles[j]['content']
            cleaned_title = re.sub(r'[（）\s():\-“”,.V徒Acts]', '', title_text)
            title_chars = set(cleaned_title)
            if not title_chars:
                continue
            
            overlap = len(transcript_chars.intersection(title_chars))
            score = overlap / len(title_chars)

            if score >= SIMILARITY_THRESHOLD:
                # --- NEW: Calculate the Contiguity Bonus ---
                # This rewards matches that are closer to the last known point.
                # A distance of 0 (the current slide) gets the highest bonus.
                distance = j - search_start_index
                bonus = 1.0 / (1.0 + distance) # Bonus is high for small distances
                
                # The final score is a combination of the raw overlap and the bonus
                final_score = overlap * bonus
                
                candidates.append({
                    'index': j,
                    'final_score': final_score, # Our new primary sorting key
                    'overlap': overlap # Fallback sorting key
                })

        if not candidates:
            modified_contents[i]['titleIndex'] = -1
        else:
            # --- UPDATED SORTING LOGIC ---
            # Sort by the new, intelligent final_score. This balances substance (overlap)
            # with natural flow (bonus).
            best_candidate = sorted(candidates, key=lambda x: (x['final_score'], x['overlap']), reverse=True)[0]
            
            best_index = best_candidate['index']
            modified_contents[i]['titleIndex'] = best_index
            search_start_index = best_index

    return modified_contents

def update_content_json_files_with_matched_titles(start_index, end_index):
    for i in range(start_index, end_index):
        title_file_name = util.file_name_builder(f"{util.FOLDER_PATH}title_from_ppt/", "Eph"
        , "json", i)
        content_file_name = util.file_name_builder(f"{util.FOLDER_PATH}combined_text_block/", "Eph"
        , "json", i)
        with open(title_file_name, "r", encoding="utf-8") as f:
            title_object_list = json.load(f)
        with open(content_file_name, "r", encoding="utf-8") as f:
            content_object_list = json.load(f)

        matched_content_object_list = pair_lecture_content_final(title_object_list, content_object_list)

        with open(content_file_name, "w", encoding="utf-8") as f:
            json.dump(matched_content_object_list, f, ensure_ascii=False, indent=2)
