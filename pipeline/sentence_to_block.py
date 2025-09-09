import json
import util

def merge_content_by_gap(content_object_list, gap_threshold=5.0):
    merged_object_list = []
    object_buffer = []

    for content_object in content_object_list:
        if not object_buffer:
            object_buffer.append(content_object)
            continue

        previous_object = object_buffer[-1]
        time_gap = content_object["startTime"] - previous_object["endTime"]

        if time_gap <= gap_threshold:
            object_buffer.append(content_object)
        else:
            # flush the buffer, the current object is of the next block
            merged_object_list.append({
                "content": " ".join(obj["content"] for obj in object_buffer),
                "startTime": object_buffer[0]["startTime"],
                "endTime": object_buffer[-1]["endTime"],
                "titleIndex": None
            })
            object_buffer = [content_object]

    # flush the last buffer
    if object_buffer:
        merged_object_list.append({
            "content": " ".join(obj["content"] for obj in object_buffer),
            "startTime": object_buffer[0]["startTime"],
            "endTime": object_buffer[-1]["endTime"],
            "titleIndex": None
        })
    return merged_object_list

def process_sentence_in_files(start_index, end_index):
    for i in range(start_index, end_index):
        input_file_name = util.file_name_builder(util.FOLDER_PATH + "text_from_audio/", "Eph", "json", i)
        output_file_name = util.file_name_builder(util.FOLDER_PATH + "combined_text_block/", "Eph", "json", i)
        with open(input_file_name, "r", encoding="utf-8") as f:
            content_object_list = json.load(f)
        merged_object_list = merge_content_by_gap(content_object_list, 0.6)
        with open(output_file_name, "w", encoding="utf-8") as f:
            json.dump(merged_object_list, f, ensure_ascii=False, indent=2)