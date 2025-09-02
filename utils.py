import json

def read_json(output_json_path):
    with open(output_json_path, "r", encoding="utf-8") as f:
        json_format = json.load(f)
    return json_format

def write_txt(output_file, output_lines):
    with open(output_file, "w", encoding="utf-8") as f:
        for line in output_lines:
            f.write(line + "\n")