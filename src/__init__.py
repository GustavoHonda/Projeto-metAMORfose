import pyautogui as pg
import subprocess
import tempfile
import os
from PIL import Image

# Substitui o método screenshot para forçar uso do scrot
def scrot_screenshot():
    tmp_file = os.path.join(tempfile.gettempdir(), "scrot_capture.png")
    subprocess.run(["scrot", tmp_file], check=True)
    return Image.open(tmp_file)

pg.screenshot = scrot_screenshot
