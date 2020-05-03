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

from problemSetting import UI_ProblemSetting

class Ui_blankPaperInput(object):  # 마킹이 되지 않은 원본 시험지를 입력하는 창
    problemAmount = -1  # 시험의 문제 수
    testpaperAmount = -1  # 시험 1세트의 장 수

    mouse_is_pressing = False  # 마우스를 누르고 있는지 여부
    clickX, clickY = -1, -1  # 클릭 지점 저장용 임시 변수
    clickCoordinates = []  # 클릭한 지점들을 저장하는 임시 변수
    problemCoordinateList = []  # 드래그된 문제 마킹 영역들을 저장하는 임시 변수
    problemIsAnswerList = []  # 각 드래그된 마킹 영역들 별 정답 여부를 저장하는 임시 변수, True 와 False


    def setupUi(self, blankPaperInput, problemAmount, testpaperAmount, gradeWithOCR):
        self.problemAmount = problemAmount
        self.testpaperAmount = testpaperAmount
        self.blankPaperInput = blankPaperInput
        self.gradeWithOCR = gradeWithOCR

        self.blankPaperInput.setObjectName("blankPaperInput")
        self.blankPaperInput.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(self.blankPaperInput)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(320, 260, 171, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect((self.onInputButtonClicked))
        self.blankPaperInput.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self.blankPaperInput)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.blankPaperInput.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self.blankPaperInput)
        self.statusbar.setObjectName("statusbar")
        self.blankPaperInput.setStatusBar(self.statusbar)

        self.retranslateUi(self.blankPaperInput)
        QtCore.QMetaObject.connectSlotsByName(self.blankPaperInput)
        self.totalProblemCoordinates = []
        self.totalIsAnswers = []


    def mouseCallbackSpot(self, event, x, y, flags, param):  # 마우스 클릭 좌표 저장용 메소드
        if event == cv2.EVENT_LBUTTONDOWN:
            self.mouse_is_pressing = True
            self.clickX, self.clickY = x, y
            self.clickCoordinates.append([self.clickX, self.clickY])



    def retranslateUi(self, blankPaperInput):
        _translate = QtCore.QCoreApplication.translate
        blankPaperInput.setWindowTitle(_translate("blankPaperInput", "blankPaperInput"))
        self.pushButton.setText(_translate("blankPaperInput", "Add blank test paper"))


    def onInputButtonClicked(self):  # 마킹되지 않은 시험지 이미지를 열고, 각 사각 좌표를 지정해 수동으로 그림 늘리기
        fname = QFileDialog.getOpenFileNames()  # 비 마킹 시험지들의 파일 읽기
        fileLocs = fname[0]  # 비 마킹 시험지 파일들의 절대 경로 리스트

        counter = 0  # 임시 변수
        for imageLoc in fileLocs:  # 각 시험지 이미지마다

            src = cv2.imread(imageLoc, cv2.IMREAD_COLOR)
            height = src.shape[0]  # 시험지 이미지 높이
            width = src.shape[1]  # 시험지 이미지 너비

            # 시험지가 너무 커 처리가 힘든 경우, 리사이징
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
            dstPoint = np.array([[0, 0], [width, 0], [width, height], [0, height]], dtype=np.float32)
            matrix = cv2.getPerspectiveTransform(srcPoint, dstPoint)
            # dstUnmarked : warped testing paper with no mark as original size
            warpedUnmarkedPaper = cv2.warpPerspective(src, matrix, (width, height))
            cv2.imshow("warpedUnmarkedPaper", warpedUnmarkedPaper)
            cv2.waitKey(0)

            # 리사이징한 시험지 파일 저장
            cv2.imwrite('./buffer/unprocessedBlankPaper_{}.jpg'.format(counter), warpedUnmarkedPaper)

            # 마킹 안 된 시험지 Blur, 흑백화 등 이미지 정제

            # convert the images to grayscale
            unmarkedPaper = cv2.cvtColor(warpedUnmarkedPaper, cv2.COLOR_BGR2GRAY)

            # blur
            for i in range(10):
                unmarkedPaper = cv2.GaussianBlur(unmarkedPaper, (7, 7), 0)

            cv2.imwrite('./buffer/processedBlankPaper_{}.jpg'.format(counter), unmarkedPaper)

            cv2.destroyAllWindows()

            counter = counter + 1

        self.ui = UI_ProblemSetting([], self.problemAmount, self.testpaperAmount, self.gradeWithOCR)
        self.blankPaperInput.hide()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    blankPaperInput = QtWidgets.QMainWindow()
    ui = Ui_blankPaperInput()
    ui.setupUi(blankPaperInput)
    blankPaperInput.show()
    sys.exit(app.exec_())

