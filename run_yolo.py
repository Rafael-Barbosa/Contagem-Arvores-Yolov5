import subprocess
import sys


def run_yolo(file_path):
    activate_venv = "C:/Users/User/OneDrive/Documentos/GitHub/TCC-Roni/API/venv/Scripts/activate.bat"
    yolo_script = (
        "C:/Users/User/OneDrive/Documentos/GitHub/TCC-Roni/API/yolov5/detect.py"
    )
    weights = "C:/Users/User/OneDrive/Documentos/GitHub/TCC-Roni/API/yolov5/best.pt"

    command = f"call {activate_venv} && python {yolo_script} --weights {weights} --img 500 --conf 0.15 --hide-conf --hide-labels --source {file_path}"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    print("Command executed:", command)
    print("Return code:", result.returncode)
    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)

    if result.returncode != 0:
        print(f"Error occurred: {result.stderr}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: run_yolo.py <file_path>")
        sys.exit(1)

    run_yolo(sys.argv[1])
