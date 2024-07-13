from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    send_from_directory,
)
import os
from werkzeug.utils import secure_filename
import subprocess
import pathlib
from pathlib import Path
import glob

# Patch pathlib to replace PosixPath with WindowsPath on Windows
pathlib.PosixPath = pathlib.WindowsPath

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "C:/Users/User/Documents/GitHub/Contagem-Arvores-Yolov5/uploads"
app.config["ALLOWED_EXTENSIONS"] = {"png", "jpg", "jpeg", "gif"}
YOLOV5_DIR = Path("C:/Users/User/Documents/GitHub/Contagem-Arvores-Yolov5/yolov5")
RUN_YOLO_SCRIPT = Path("C:/Users/User/Documents/GitHub/Contagem-Arvores-Yolov5/run_yolo.py")

def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]
    )

def get_latest_exp_dir(base_dir):
    exp_dirs = glob.glob(str(base_dir / 'exp*'))
    if not exp_dirs:
        return None
    latest_exp_dir = max(exp_dirs, key=os.path.getmtime)
    return latest_exp_dir

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        print("No file part")
        return redirect(request.url)
    file = request.files["file"]
    if file.filename == "":
        print("No selected file")
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = Path(app.config["UPLOAD_FOLDER"]) / filename
        file.save(file_path)
        print(f"File saved to {file_path}")

        # Run YOLOv5 detection
        yolo_command = f'python "{RUN_YOLO_SCRIPT}" "{file_path.resolve()}"'
        try:
            result = subprocess.run(
                yolo_command, shell=True, capture_output=True, text=True
            )
            result.check_returncode()
            print(result.stdout)
            # Extrair o número de árvores detectadas do stdout
            num_arvores = 0
            for line in result.stdout.split('\n'):
                if "Foram detectadas" in line:
                    num_arvores = int(line.split()[2])
                    break
        except subprocess.CalledProcessError as e:
            print(f"Error occurred: {e}")
            print(f"stderr: {e.stderr}")
            return redirect(url_for("index"))

        output_directory = get_latest_exp_dir(YOLOV5_DIR / "runs" / "detect")
        if output_directory:
            processed_images = os.listdir(output_directory)
            if processed_images:
                processed_image_path = Path(output_directory) / processed_images[0]
                return redirect(
                    url_for("show_processed_image", filename=processed_image_path.name, folder=Path(output_directory).name, original_filename=file_path.name, num_arvores=num_arvores)
                )
        return redirect(url_for("index"))

    print("File not allowed")
    return redirect(request.url)

@app.route("/processed/<folder>/<filename>/<original_filename>/<num_arvores>")
def show_processed_image(folder, filename, original_filename, num_arvores):
    return render_template("index.html", processed_image=filename, processed_folder=folder, original_image=original_filename, num_arvores=num_arvores)

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

@app.route("/runs/detect/<folder>/<filename>")
def output_file(folder, filename):
    return send_from_directory(YOLOV5_DIR / "runs" / "detect" / folder, filename)

if __name__ == "__main__":
    app.run(debug=True)
