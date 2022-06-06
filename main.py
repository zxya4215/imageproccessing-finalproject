import os.path
import sys
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from interface import *
from Detect import *

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setup_picture()

    def setup_picture(self):
        self.action_interface.triggered.connect(self.open_file)
        self.search_Button.clicked.connect(self.search)

    def open_file(self):
        self.filename, _ = QFileDialog.getOpenFileName(self, 'Open Image', 'Image', '*.jpg *.png *.bmp')
        self.img = self.filename
        self.img_path = os.path.relpath(self.img)
        self.showImage()

    def showImage(self):
        self.originalimg = cv.imread(self.img)
        height, width, channel = self.originalimg.shape
        bytesPerline = 3 * width
        self.qImg = QImage(self.originalimg, width, height, bytesPerline, QImage.Format_RGB888).rgbSwapped()
        self.qpixmap = QPixmap.fromImage(self.qImg)
        self.qpixmap_height = self.qpixmap.height()
        self.UserImage.setPixmap(QPixmap.fromImage(self.qImg))

    def search(self):
        tmpImg = {
            'hash': GetImageHash(self.img_path),
            'cvData': cv.imread(self.img_path)
        }
        resImg = {
            'file': "",
            'dist': -1
        }

        start = time.time()
        # 指定要列出所有檔案的目錄
        for i in range(2, sheet.max_row + 1):
            name, dct = ExcRead(i)
            dis = HammingDistance(tmpImg["hash"], dct)

            if resImg["dist"] == -1 or dis < resImg["dist"]:
                resImg["dist"] = dis
                resImg["file"] = name
        end = time.time()

        self.compareimg = cv.imread(IMAGE_DB_PATH + resImg["file"])
        height, width, channel = self.compareimg.shape
        bytesPerline = 3 * width
        self.qImg = QImage(self.compareimg, width, height, bytesPerline, QImage.Format_RGB888).rgbSwapped()
        self.qpixmap = QPixmap.fromImage(self.qImg)
        self.qpixmap_height = self.qpixmap.height()
        self.CompareImage.setPixmap(QPixmap.fromImage(self.qImg))
        self.hammingdistance_label.setText("HammingDistance using time： " + format(end - start))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())