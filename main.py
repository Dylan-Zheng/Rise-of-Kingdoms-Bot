from adb import enable_adb
from bot import Bot
from gui.main_window import MainWindow


from utils import resource_path
from PIL import Image
from constants.file_relative_paths import FilePaths
from device_gui_detector import GuiName
from device_gui_detector import GuiDetector
from constants.file_relative_paths import ImagePathAndProps
import base64
from io import BytesIO
import haoi
from utils import img_to_string
import json


import numpy as np
import io
import cv2
import aircv


def main():

    adb = enable_adb()
    window = MainWindow(adb)
    window.run()



if __name__ == '__main__':
    main()
