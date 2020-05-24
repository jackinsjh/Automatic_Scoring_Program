# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\questionNumInput.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
import numpy as np
import cv2

from problemSetting import UI_ProblemSetting


class Ui_QuestionNumInput(object):  # 맨 처음 뜨는 창. 문제 수와 한 시험의 총 페이지 수를 질문.

    mouse_is_pressing = False  # 마우스를 누르고 있는지 여부
    clickX, clickY = -1, -1  # 클릭 지점 저장용 임시 변수
    clickCoordinates = []  # 클릭한 지점들을 저장하는 임시 변수
    problemCoordinateList = []  # 드래그된 문제 마킹 영역들을 저장하는 임시 변수
    problemIsAnswerList = []  # 각 드래그된 마킹 영역들 별 정답 여부를 저장하는 임시 변수, True 와 False

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(484, 505)
        Form.setStyleSheet("background: #a8d8fd")
        self.descriptiveProblemNumberLabel_2 = QtWidgets.QLabel(Form)
        self.descriptiveProblemNumberLabel_2.setGeometry(QtCore.QRect(20, 130, 872, 22))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.descriptiveProblemNumberLabel_2.sizePolicy().hasHeightForWidth())
        self.descriptiveProblemNumberLabel_2.setSizePolicy(sizePolicy)
        self.descriptiveProblemNumberLabel_2.setMinimumSize(QtCore.QSize(100, 20))
        self.descriptiveProblemNumberLabel_2.setStyleSheet("font: 75 15pt \"나눔스퀘어 Bold\";")
        self.descriptiveProblemNumberLabel_2.setObjectName("descriptiveProblemNumberLabel_2")
        self.descriptiveProblemNumberLabel_3 = QtWidgets.QLabel(Form)
        self.descriptiveProblemNumberLabel_3.setGeometry(QtCore.QRect(20, 240, 872, 22))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.descriptiveProblemNumberLabel_3.sizePolicy().hasHeightForWidth())
        self.descriptiveProblemNumberLabel_3.setSizePolicy(sizePolicy)
        self.descriptiveProblemNumberLabel_3.setMinimumSize(QtCore.QSize(100, 20))
        self.descriptiveProblemNumberLabel_3.setStyleSheet("font: 75 15pt \"나눔스퀘어 Bold\";")
        self.descriptiveProblemNumberLabel_3.setObjectName("descriptiveProblemNumberLabel_3")
        self.check_useOCR = QtWidgets.QCheckBox(Form)
        self.check_useOCR.setGeometry(QtCore.QRect(20, 350, 872, 22))
        self.check_useOCR.setStyleSheet("font: 75 12pt \"나눔스퀘어 Bold\";")
        self.check_useOCR.setObjectName("check_useOCR")
        self.confirmButton = QtWidgets.QPushButton(Form)
        self.confirmButton.setGeometry(QtCore.QRect(180, 410, 140, 50))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.confirmButton.sizePolicy().hasHeightForWidth())
        self.confirmButton.setSizePolicy(sizePolicy)
        self.confirmButton.setMinimumSize(QtCore.QSize(140, 50))
        self.confirmButton.setStyleSheet("font: 81 24pt \"나눔스퀘어 ExtraBold\";\n"
"color: rgb(255, 255, 255);\n"
"background-color: rgb(0, 85, 255);")
        self.confirmButton.setObjectName("confirmButton")
        self.confirmButton.clicked.connect(self.confirmButtonClicked)
        self.descriptive = QtWidgets.QLabel(Form)
        self.descriptive.setGeometry(QtCore.QRect(110, 50, 876, 44))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.descriptive.sizePolicy().hasHeightForWidth())
        self.descriptive.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("나눔스퀘어 ExtraBold")
        font.setPointSize(30)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(10)
        self.descriptive.setFont(font)
        self.descriptive.setStyleSheet("font: 81 30pt \"나눔스퀘어 ExtraBold\";")
        self.descriptive.setObjectName("descriptive")
        self.paperNumInput = QtWidgets.QLineEdit(Form)
        self.paperNumInput.setGeometry(QtCore.QRect(20, 170, 81, 24))
        self.paperNumInput.setStyleSheet("font: 12pt \"나눔스퀘어\";")
        self.paperNumInput.setText("")
        self.paperNumInput.setObjectName("paperNumInput")
        self.problemNumInput = QtWidgets.QLineEdit(Form)
        self.problemNumInput.setGeometry(QtCore.QRect(20, 280, 81, 24))
        self.problemNumInput.setStyleSheet("font: 12pt \"나눔스퀘어\";")
        self.problemNumInput.setText("")
        self.problemNumInput.setObjectName("problemNumInput")

        self.nameGuideLabel_1 = QtWidgets.QLabel(Form)
        self.nameGuideLabel_1.setGeometry(QtCore.QRect(190, 200, 271, 21))
        font = QtGui.QFont()
        font.setFamily("나눔스퀘어 Bold")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.nameGuideLabel_1.setFont(font)
        self.nameGuideLabel_1.setObjectName("nameGuideLabel_1")
        self.nameGuideLabel_2 = QtWidgets.QLabel(Form)
        self.nameGuideLabel_2.setGeometry(QtCore.QRect(190, 240, 271, 21))
        font = QtGui.QFont()
        font.setFamily("나눔스퀘어 Bold")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.nameGuideLabel_2.setFont(font)
        self.nameGuideLabel_2.setObjectName("nameGuideLabel_2")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        self.Form = Form

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Automatic Scoring Program"))
        Form.setWindowIcon(QtGui.QIcon("titleIcon.png"))
        self.descriptiveProblemNumberLabel_2.setText(_translate("Form", "시험지 장수"))
        self.descriptiveProblemNumberLabel_3.setText(_translate("Form", "시험지 문제수"))
        self.check_useOCR.setText(_translate("Form", "OCR 주관식 채점 여부"))
        self.confirmButton.setText(_translate("Form", "다음"))
        self.descriptive.setText(_translate("Form", "시험지 초기 설정"))
        self.nameGuideLabel_1.setText(_translate("Form", "# 학생들의 이름을 nameList.txt 파일에"))
        self.nameGuideLabel_2.setText(_translate("Form", "한 줄에 하나씩 순서대로 적어주세요"))

    def mouseCallbackSpot(self, event, x, y, flags, param):  # 마우스 클릭 좌표 저장용 메소드
        if event == cv2.EVENT_LBUTTONDOWN:
            self.mouse_is_pressing = True
            self.clickX, self.clickY = x, y
            self.clickCoordinates.append([self.clickX, self.clickY])

    def showPopupUnmarkedPaperInput(self):
        popupUnmarked = QtWidgets.QWidget()
        popupUnmarked_UI = popupUnmarkedClass()
        popupUnmarked_UI.setupUi(popupUnmarked)
        popupUnmarked.show()
        while popupUnmarked_UI.proceed == 0:  # 다음 버튼이 눌리기까지 대기
            QtCore.QCoreApplication.processEvents()
        popupUnmarked.hide()

    def showPopupEdgeInstruction_1(self):
        popupEdge = QtWidgets.QWidget()
        popupEdge_UI = popupEdgeInstructionClass_1()
        popupEdge_UI.setupUi(popupEdge)
        popupEdge.show()
        while popupEdge_UI.proceed == 0:  # 다음 버튼이 눌리기까지 대기
            QtCore.QCoreApplication.processEvents()
        popupEdge.hide()

    def confirmButtonClicked(self):  # 확인 버튼 클릭시 동작

        self.showPopupUnmarkedPaperInput()

        self.problemAmount = int(self.problemNumInput.text())  # 시험의 문제 갯수
        self.testpaperAmount = int(self.paperNumInput.text())  # 한 시험지 세트의 총 페이지 수
        self.gradeWithOCR = self.check_useOCR.isChecked()  # OCR로 주관식 채점 여부

        fileLocs = []
        while True:
            fname = QFileDialog.getOpenFileName()  # 비 마킹 시험지들의 파일 읽기
            if fname[0] != '':  # 아직 읽을 파일이 들어온 경우
                fileLocs.append(fname[0])
            else:  # 읽을 파일이 더 없는 경우 - 루프 종료
                break

        self.showPopupEdgeInstruction_1()

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

            cv2.imshow("Automatic Scoring Program", src)
            cv2.setMouseCallback('Automatic Scoring Program', self.mouseCallbackSpot)

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
            cv2.imshow("Automatic Scoring Program", warpedUnmarkedPaper)
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

        self.Form.hide()

        #문제 설정 창 띄우기
        self.problemSettingWindow = QtWidgets.QWidget()
        self.problemSettingWindowUI = UI_ProblemSetting()
        self.problemSettingWindowUI.setupUi(self.problemSettingWindow, [], self.problemAmount, self.testpaperAmount, self.gradeWithOCR)
        self.problemSettingWindow.show()


class popupUnmarkedClass(object):
    def setupUi(self, Form):
        self.proceed = 0  # 계속 프로그램을 진행할지 여부를 저장하는 변수

        Form.setObjectName("Form")
        Form.resize(423, 219)
        Form.setStyleSheet("background: #a8d8fd")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(20, 10, 61, 81))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("pencil.png"))
        self.label.setObjectName("label")
        self.nameGuideLabel_1 = QtWidgets.QLabel(Form)
        self.nameGuideLabel_1.setGeometry(QtCore.QRect(100, 20, 301, 21))
        font = QtGui.QFont()
        font.setFamily("나눔스퀘어 Bold")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.nameGuideLabel_1.setFont(font)
        self.nameGuideLabel_1.setObjectName("nameGuideLabel_1")
        self.nameGuideLabel_2 = QtWidgets.QLabel(Form)
        self.nameGuideLabel_2.setGeometry(QtCore.QRect(100, 60, 301, 21))
        font = QtGui.QFont()
        font.setFamily("나눔스퀘어 Bold")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.nameGuideLabel_2.setFont(font)
        self.nameGuideLabel_2.setObjectName("nameGuideLabel_2")
        self.confirmButton = QtWidgets.QPushButton(Form)
        self.confirmButton.setGeometry(QtCore.QRect(150, 150, 140, 50))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.confirmButton.sizePolicy().hasHeightForWidth())
        self.confirmButton.setSizePolicy(sizePolicy)
        self.confirmButton.setMinimumSize(QtCore.QSize(140, 50))
        self.confirmButton.setStyleSheet("font: 81 24pt \"나눔스퀘어 ExtraBold\";\n"
                                         "color: rgb(255, 255, 255);\n"
                                         "background-color: rgb(0, 85, 255);")
        self.confirmButton.setObjectName("confirmButton")
        self.confirmButton.clicked.connect(self.onConfirmButtonClicked)
        self.nameGuideLabel_3 = QtWidgets.QLabel(Form)
        self.nameGuideLabel_3.setGeometry(QtCore.QRect(100, 100, 401, 21))
        font = QtGui.QFont()
        font.setFamily("나눔스퀘어 Bold")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.nameGuideLabel_3.setFont(font)
        self.nameGuideLabel_3.setObjectName("nameGuideLabel_3")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Automatic Scoring Program"))
        Form.setWindowIcon(QtGui.QIcon("titleIcon.png"))
        self.nameGuideLabel_1.setText(_translate("Form", "마킹하지 않은 원본 시험지 파일들을"))
        self.nameGuideLabel_2.setText(_translate("Form", "페이지 순서대로 선택해 주세요"))
        self.nameGuideLabel_3.setText(_translate("Form", "모두 입력하면 취소 버튼을 눌러주세요"))
        self.confirmButton.setText(_translate("Form", "계속"))

    def onConfirmButtonClicked(self):
        self.proceed = 1


class popupEdgeInstructionClass_1(object):
    def setupUi(self, Form):
        self.proceed = 0
        Form.setObjectName("Form")
        Form.resize(409, 218)
        Form.setStyleSheet("background: #a8d8fd")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(20, 30, 61, 81))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("pencil.png"))
        self.label.setObjectName("label")
        self.nameGuideLabel_1 = QtWidgets.QLabel(Form)
        self.nameGuideLabel_1.setGeometry(QtCore.QRect(100, 20, 301, 21))
        font = QtGui.QFont()
        font.setFamily("나눔스퀘어 Bold")
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.nameGuideLabel_1.setFont(font)
        self.nameGuideLabel_1.setObjectName("nameGuideLabel_1")
        self.nameGuideLabel_2 = QtWidgets.QLabel(Form)
        self.nameGuideLabel_2.setGeometry(QtCore.QRect(100, 60, 301, 21))
        font = QtGui.QFont()
        font.setFamily("나눔스퀘어 Bold")
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.nameGuideLabel_2.setFont(font)
        self.nameGuideLabel_2.setObjectName("nameGuideLabel_2")
        self.confirmButton = QtWidgets.QPushButton(Form)
        self.confirmButton.setGeometry(QtCore.QRect(140, 150, 140, 50))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.confirmButton.sizePolicy().hasHeightForWidth())
        self.confirmButton.setSizePolicy(sizePolicy)
        self.confirmButton.setMinimumSize(QtCore.QSize(140, 50))
        self.confirmButton.setStyleSheet("font: 81 24pt \"나눔스퀘어 ExtraBold\";\n"
                                         "color: rgb(255, 255, 255);\n"
                                         "background-color: rgb(0, 85, 255);")
        self.confirmButton.setObjectName("confirmButton")
        self.confirmButton.clicked.connect(self.onConfirmButtonClicked)
        self.nameGuideLabel_3 = QtWidgets.QLabel(Form)
        self.nameGuideLabel_3.setGeometry(QtCore.QRect(100, 100, 301, 21))
        font = QtGui.QFont()
        font.setFamily("나눔스퀘어 Bold")
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.nameGuideLabel_3.setFont(font)
        self.nameGuideLabel_3.setObjectName("nameGuideLabel_3")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Automatic Scoring Program"))
        Form.setWindowIcon(QtGui.QIcon("titleIcon.png"))
        self.nameGuideLabel_1.setText(_translate("Form", "좌상 - 우상 - 우하 - 좌하 순서대로"))
        self.nameGuideLabel_2.setText(_translate("Form", "시험지 이미지의 모서리 부분을 클릭하고"))
        self.confirmButton.setText(_translate("Form", "계속"))
        self.nameGuideLabel_3.setText(_translate("Form", "엔터 키를 눌러주세요"))

    def onConfirmButtonClicked(self):
        self.proceed = 1


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_QuestionNumInput()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
