import json
from ast import mod
import util
import json

def handle_latex_special_characters(c):
  match c:
    case "&" | "%" | "$" | "#" | "_" | "{" | "}":
      return "\\" + c
    case "~":
      return "\\textasciitilde"
    case "^":
      return "\\textasciicircum"
    case "\\":
      return "\\textbackslash"
    case _:
      return c

def modify_string_for_latex(s):
  new_string = ""
  for c in s:
    new_string += handle_latex_special_characters(c)
  return new_string

def json_to_latex(title_file, content_file, output_file):
    # Map levels to LaTeX sectioning
    level_to_cmd = {
        0: "\\section",
        1: "\\subsection",
        2: "\\subsubsection",
    }

    with open(title_file, "r", encoding="utf-8") as f:
        titles = json.load(f)

    with open(content_file, "r", encoding="utf-8") as f:
        contents = json.load(f)

    latex_lines = [
        r"\documentclass[lang=cn,newtx,10pt,scheme=chinese]{elegantbook}",  # ctex for Chinese
        r"\begin{document}",
        r"\usepackage{graphicx}",
        r"\usepackage{fontspec}",
        r"\setmainfont{Times New Roman}[",
        "  Ligatures=TeX,"
        "  Script=Latin,",
        "  Script=Greek",
        r"]",
        "",
        r"\tcbset{",
        r"  mybox/.style={",
        "    colframe=black,",
        "    colback=white,",
        "    boxrule=0.8pt,",
        "    arc=0mm,",
        "    left=6pt,",
        "    right=6pt,",
        "    top=6pt,",
        "    bottom=6pt",
        r"  }",
        r"}",
        ""
    ]

    current_title_index = -1
    for idx, content_object in enumerate(contents):
        content = content_object["content"]
        content = modify_string_for_latex(content)
        paired_title_index = content_object["titleIndex"]
        title_object = titles[paired_title_index]
        title_text = modify_string_for_latex(title_object["content"].strip())
        latex_command = level_to_cmd.get(title_object["level"], "\\subsubsection")
        
        if paired_title_index > current_title_index:
            # write titles between the the current title and the next title
            for j in range(current_title_index + 1, paired_title_index + 1):
                title_object = titles[j]
                title_text = modify_string_for_latex(title_object["content"].strip())
                latex_command = level_to_cmd.get(title_object["level"], "\\subsubsection")
                latex_lines.append(latex_command + "{" + title_text + "}")
                latex_lines.append("")  # blank line after each title section
            latex_lines.append(content)
            latex_lines.append("")  # blank line after each title section
            current_title_index = paired_title_index
        elif paired_title_index == -1:
            latex_lines.append(content)
        elif paired_title_index == current_title_index:
            latex_lines.append(content)
        else:
            raise Exception("invalid title index")

    latex_lines.append(r"\end{document}")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(latex_lines))

def convert_folder_files(start_index, end_index):
    for i in range(start_index, end_index):
        title_file_name = util.file_name_builder(util.FOLDER_PATH + "title_from_ppt/", "Eph"
        , "json", i)
        content_file_name = util.file_name_builder(util.FOLDER_PATH + "combined_text_block/", "Eph"
        , "json", i)
        output_file_name = util.file_name_builder(util.FOLDER_PATH + "latex/", "Eph"
        , "tex", i)
        json_to_latex(title_file_name, content_file_name, output_file_name)