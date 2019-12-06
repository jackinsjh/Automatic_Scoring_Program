# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'blankPaperInput.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel
from PyQt5 import QtCore, QtGui, QtWidgets

import numpy as np
import cv2

from skimage.measure import compare_ssim
import argparse
import imutils

class Ui_blankPaperInput(object):
    problemNum = -1

    mouse_is_pressing = False
    clickX, clickY = -1, -1
    clickCoordinates = []

    def setupUi(self, blankPaperInput):  #problemNum
        #self.problemNum = problemNum

        blankPaperInput.setObjectName("blankPaperInput")
        blankPaperInput.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(blankPaperInput)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(320, 260, 171, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect((self.onInputButtonClicked))
        blankPaperInput.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(blankPaperInput)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        blankPaperInput.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(blankPaperInput)
        self.statusbar.setObjectName("statusbar")
        blankPaperInput.setStatusBar(self.statusbar)

        self.retranslateUi(blankPaperInput)
        QtCore.QMetaObject.connectSlotsByName(blankPaperInput)

        """
        # original code
        blankPaperInput.setObjectName("blankPaperInput")
        blankPaperInput.resize(568, 109)
        self.centralwidget = QtWidgets.QWidget(blankPaperInput)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(110, 30, 371, 41))
        font = QtGui.QFont()
        font.setPointSize(22)
        self.label.setFont(font)
        self.label.setObjectName("label")
        blankPaperInput.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(blankPaperInput)
        self.statusbar.setObjectName("statusbar")
        blankPaperInput.setStatusBar(self.statusbar)

        self.retranslateUi(blankPaperInput)
        QtCore.QMetaObject.connectSlotsByName(blankPaperInput)
        #print(self.problemNum)
        """

    def mouseCallbackSpot(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.mouse_is_pressing = True
            self.clickX, self.clickY = x, y
            self.clickCoordinates.append([self.clickX, self.clickY])





    def retranslateUi(self, blankPaperInput):
        _translate = QtCore.QCoreApplication.translate
        blankPaperInput.setWindowTitle(_translate("blankPaperInput", "blankPaperInput"))
        self.pushButton.setText(_translate("blankPaperInput", "Add blank test paper"))


    def onInputButtonClicked(self):  # 파일 열고, 사각 지정해 수동으로 그림 늘리기
        fname = QFileDialog.getOpenFileName()
        #self.label.setText(fname[0])    #해당 파일의 절대 경로
        fileLoc = fname[0]





        # read unmarked image
        src = cv2.imread(fileLoc, cv2.IMREAD_COLOR)
        height = src.shape[0]
        width = src.shape[1]

        if height >= width:
            resizeScale = 1000 / height
        else:
            resizeScale = 1000 / width
        src = cv2.resize(src, (int(width * resizeScale), int(height * resizeScale)), interpolation=cv2.INTER_AREA)

        print("Changed dimensions : ", src.shape)

        height, width, channel = src.shape

        cv2.imshow("UnmarkedOriginal", src)
        cv2.setMouseCallback('UnmarkedOriginal', self.mouseCallbackSpot)

        print("Click 4 spot of the image, starting from left-upper side, clockwise")
        print("After that, press any key")
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        print(self.clickCoordinates)

        srcPoint = np.array(self.clickCoordinates, dtype=np.float32)
        self.clickCoordinates = []

        # assign 4 test paper's edges' coordinates and warp it to the original image size
        # srcPoint=np.array([[66, 36], [699, 31], [734, 977], [41, 973]], dtype=np.float32) # for imageSet 1
        # srcPoint=np.array([[72, 57], [692, 54], [758, 976], [39, 995]], dtype=np.float32) # for imageSet 2
        dstPoint = np.array([[0, 0], [width, 0], [width, height], [0, height]], dtype=np.float32)
        matrix = cv2.getPerspectiveTransform(srcPoint, dstPoint)
        # dstUnmarked : warped testing paper with no mark as original size
        warpedUnmarkedPaper = cv2.warpPerspective(src, matrix, (width, height))
        cv2.imshow("warpedUnmarkedPaper", warpedUnmarkedPaper)
        cv2.imwrite('./buffer/warpedBlankPaper.jpg', warpedUnmarkedPaper)
        cv2.waitKey(0)
        cv2.destroyAllWindows()








if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    blankPaperInput = QtWidgets.QMainWindow()
    ui = Ui_blankPaperInput()
    ui.setupUi(blankPaperInput)
    blankPaperInput.show()
    sys.exit(app.exec_())

