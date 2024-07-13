import subprocess
import sys
import os

import pathlib
from pathlib import Path
pathlib.PosixPath = pathlib.WindowsPath

def run_yolo(file_path):
    activate_venv = Path("C:/Users/User/Documents/GitHub/Contagem-Arvores-Yolov5/venv/Scripts/activate.bat")
    yolo_script = Path("C:/Users/User/Documents/GitHub/Contagem-Arvores-Yolov5/yolov5/detect.py")
    weights = Path("C:/Users/User/Documents/GitHub/Contagem-Arvores-Yolov5/model/best.pt")
    file_path = Path(file_path).resolve()

    command = f'call {activate_venv} && python {yolo_script} --weights {weights} --img 500 --conf 0.15 --hide-conf --hide-labels --source {file_path}'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    print("Command executed:", command)
    print("STDERR:", result.stderr)

    if result.returncode != 0:
        print(f"Error occurred: {result.stderr}")
        sys.exit(1)
    

    for line in result.stderr.split('\n'):
        if "Foram detectadas" in line:
            num_arvores = int(line.split()[2])
            break
    else:
        num_arvores = 0

    return num_arvores

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: run_yolo.py <file_path>")
        sys.exit(1)

    num_arvores = 0
    num_arvores = run_yolo(sys.argv[1])
    
    print(f"Número de Árvores detectadas: {num_arvores}")
