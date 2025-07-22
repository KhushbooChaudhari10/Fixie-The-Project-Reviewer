import os

def extract_text_from_py_files(folder_path):
    all_text = ""

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        all_text += f"\n\n# ===== File: {file_path} =====\n"
                        all_text += f.read()
                except Exception as e:
                    all_text += f"\n\n# Error reading {file_path}: {e}\n"

    return all_text
