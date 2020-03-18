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

class Ui_blankPaperInput(object):
    problemAmount = -1
    testpaperAmount = -1

    mouse_is_pressing = False
    clickX, clickY = -1, -1
    clickCoordinates = []
    problemCoordinateList = []
    problemIsAnswerList = []


    def setupUi(self, blankPaperInput, problemAmount, testpaperAmount):
        self.problemAmount = problemAmount
        self.testpaperAmount = testpaperAmount

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
        self.totalProblemCoordinates = []
        self.totalIsAnswers = []

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
        fname = QFileDialog.getOpenFileNames()
        #self.label.setText(fname[0])    #해당 파일의 절대 경로
        fileLocs = fname[0]

        counter = 0
        for imageLoc in fileLocs:
            # read unmarked image
            src = cv2.imread(imageLoc, cv2.IMREAD_COLOR)
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
            dstPoint = np.array([[0, 0], [width, 0], [width, height], [0, height]], dtype=np.float32)
            matrix = cv2.getPerspectiveTransform(srcPoint, dstPoint)
            # dstUnmarked : warped testing paper with no mark as original size
            warpedUnmarkedPaper = cv2.warpPerspective(src, matrix, (width, height))
            cv2.imshow("warpedUnmarkedPaper", warpedUnmarkedPaper)
            cv2.waitKey(0)

            # 마킹 안 된 시험지 Blur, 흑백화 등 정제

            # convert the images to grayscale
            unmarkedPaper = cv2.cvtColor(warpedUnmarkedPaper, cv2.COLOR_BGR2GRAY)

            # blur
            for i in range(10):
                unmarkedPaper = cv2.GaussianBlur(unmarkedPaper, (7, 7), 0)

            cv2.imwrite('./buffer/processedBlankPaper_{}.jpg'.format(counter), unmarkedPaper)

            cv2.destroyAllWindows()

            counter = counter + 1

        """
        # 각 문제영역 지정
        curProblemCoordinates = []
        curProblemIsAnswers = []

        for i in range(self.problemNum):
            while True:
                cv2.imshow("warpedUnmarkedPaper", warpedUnmarkedPaper)
                cv2.setMouseCallback('warpedUnmarkedPaper', self.mouseCallbackROI)

                print("Drag the area of each problem, starting from left-upper side, to right-under side")
                print("After that, press 1 if correct, press 2 if incorrect, else if all the choices are marked")
                keyInput = cv2.waitKey(0)
                dragCoordinates = [self.clickXFirst, self.clickYFirst, self.clickXLast, self.clickYLast]

                cv2.destroyAllWindows()
                print(dragCoordinates)

                if keyInput == ord('1'):  # 정답
                    print('correct')
                    curProblemIsAnswers.append(True)
                    curProblemCoordinates.append(dragCoordinates)
                elif keyInput == ord('2'):  # 오답
                    print('incorrect')
                    curProblemIsAnswers.append(False)
                    curProblemCoordinates.append(dragCoordinates)
                else:  # 문제 영역 마킹 끝
                    break

            self.totalProblemCoordinates.append(curProblemCoordinates)
            print("added coordinates: {}".format(curProblemCoordinates))
            self.totalIsAnswers.append(curProblemIsAnswers)
            print("added isAnswers: {}".format(curProblemIsAnswers))
            curProblemCoordinates = []
            curProblemIsAnswers = []




        # srcPoint = np.array(self.clickCoordinates, dtype=np.float32)
        # self.clickCoordinates = []


        print('area designation completed')
        print('final problem areas:')
        print(self.totalProblemCoordinates)
        print('final problem isAnswers:')
        print(self.totalIsAnswers)
        """


        self.window = QtWidgets.QMainWindow()
        self.ui = UI_ProblemSetting([], self.problemAmount, self.testpaperAmount)
        # self.ui.setupUi(self.window)
        # blankPaperInput.hide()
        self.window.show()





if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    blankPaperInput = QtWidgets.QMainWindow()
    ui = Ui_blankPaperInput()
    ui.setupUi(blankPaperInput)
    blankPaperInput.show()
    sys.exit(app.exec_())

