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
from pathlib import Path, WindowsPath
import subprocess

# Patch pathlib to replace PosixPath with WindowsPath on Windows
if os.name == "nt":
    Path = WindowsPath

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"
app.config["ALLOWED_EXTENSIONS"] = {"png", "jpg", "jpeg", "gif"}
YOLOV5_DIR = Path("C:/Users/User/OneDrive/Documentos/GitHub/TCC-Roni/API/yolov5")
RUN_YOLO_SCRIPT = Path(
    "C:/Users/User/OneDrive/Documentos/GitHub/TCC-Roni/API/run_yolo.py"
)


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]
    )


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
        yolo_command = f'python "{RUN_YOLO_SCRIPT}" "{file_path}"'
        try:
            result = subprocess.run(
                yolo_command, shell=True, capture_output=True, text=True
            )
            result.check_returncode()
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"Error occurred: {e}")
            print(f"stderr: {e.stderr}")
            return redirect(url_for("index"))

        output_directory = YOLOV5_DIR / "runs" / "detect" / "exp"
        processed_images = os.listdir(output_directory)
        if processed_images:
            processed_image_path = output_directory / processed_images[0]
            return redirect(
                url_for("show_processed_image", filename=processed_image_path.name)
            )
        return redirect(url_for("index"))

    print("File not allowed")
    return redirect(request.url)


@app.route("/processed/<filename>")
def show_processed_image(filename):
    return render_template("index.html", processed_image=filename)


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


@app.route("/runs/detect/exp/<filename>")
def output_file(filename):
    return send_from_directory(YOLOV5_DIR / "runs" / "detect" / "exp", filename)


if __name__ == "__main__":
    app.run(debug=True)
