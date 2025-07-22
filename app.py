from flask import Flask, request, render_template, redirect
import os
import zipfile
from werkzeug.utils import secure_filename
from services import extract_text_from_py_files
from huggingface_api import ask_llama


app = Flask(__name__)
UPLOAD_FOLDER = 'uploaded_folders'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def upload_form():
    return render_template('upload.html')  # Show the form

@app.route('/upload', methods=['POST'])
def upload_zip():
    uploaded_file = request.files.get('zipfile')

    if uploaded_file and uploaded_file.filename.endswith('.zip'):
        filename = secure_filename(uploaded_file.filename)
        zip_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        uploaded_file.save(zip_path)

        # Extract to folder with the same name as the zip (no .zip)
        extract_dir = os.path.join(app.config['UPLOAD_FOLDER'], filename[:-4])
        os.makedirs(extract_dir, exist_ok=True)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
            
        # Extract all Python code from .py files
        all_python_code = extract_text_from_py_files(extract_dir)

        short_code = all_python_code[:3000]
        # Prepare prompt and call LLaMA
        prompt = "You're a code reviewer. Suggest improvements for the following Python code."
        llama_response = ask_llama(prompt, all_python_code)


        # Return combined result
        return render_template('upload.html', folder=extract_dir, response=llama_response)


    return "❌ Please upload a valid .zip file."


if __name__ == "__main__":
    app.run(debug=True)
