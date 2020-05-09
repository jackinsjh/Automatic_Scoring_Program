# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\problemSettingUI.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!

from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget
from PyQt5 import QtCore, QtGui, QtWidgets

import numpy as np
import cv2
import pytesseract

from skimage.measure import compare_ssim

from totalResult import Ui_totalResult

from descriptiveGradingUI import Ui_AutomaticScoringProgramUI10

import copy


class personResult:  # 한 사람의 시험지를 채점한 최종 결과
    def __init__(self, name, isCorrectList, marks):
        self.name = name  # 이름
        self.isCorrectList = isCorrectList  # 정답 여부 True/False 리스트, 서술형 문제의 경우 획득한 점수가 대신 들어감
        self.marks = marks  # 마킹 리스트


class eachProblemInfo:  # 각 문제의 정보를 저장하는 데 사용하는 클래스
    def __init__(self, type, areas, isAnswer, score, page, OCRsubjectiveAnswer):
        self.type = type  # 문제 타입 -> 1: 객관식, 2: 주관식, 3: 서술형
        self.areas = areas  # 문제 마킹 영역 좌표들
        self.isAnswer = isAnswer  # 각 마킹 영역들이 맞는지 틀리는지의 리스트
        self.score = score  # 이 문제의 점수
        self.page = page  # 이 문제가 위치하는 페이지
        self.OCRsubjectiveAnswer = OCRsubjectiveAnswer  # OCR 주관식 채점시에만 사용 - 주관식 정답 텍스트

    def show(self):  # 디버깅용 문제 정보 열람 메소드
        print("Type : {}".format(self.type))
        print("Areas : {}".format(self.areas))
        print("isAnswer : {}".format(self.isAnswer))
        print("score : {}".format(self.score))
        print("page : {}".format(self.page))


class UI_ProblemSetting(QWidget):  # 각 문제들의 메타데이터를 지정하고, 채점함

    mouse_is_pressing = False  # 마우스를 누르고 있는지의 여부, 임시 변수
    clickX, clickY = -1, -1  # 클릭 좌표 저장용 임시 변수
    clickCoordinates = []  # 클릭한 좌표들을 저장하는 임시 변수
    problemAmount = -1  # 시험의 문제 수
    testPaperAmount = -1  # 시험의 총 페이지 수

    def setupUi(self, problemSettingWindow, totalProblemList, problemAmount, testPaperAmount, gradeWithOCR):

        # 넘어온 파라미터들 저장
        self.totalProblemList = totalProblemList  # 모든 시험 문제들의 메타데이터 저장
        self.problemAmount = problemAmount  # 넘어온 문제 수 정보 저장
        self.testPaperAmount = testPaperAmount  # 넘어온 페이지 수 정보 저장
        self.gradeWithOCR = gradeWithOCR  # 넘어온 주관식 OCR 채점 여부 저장 - True/False

        self.curProblemType = -1
        self.curProblemCoordinates = []
        self.curProblemIsAnswers = []
        self.curProblemScore = -1
        self.curProblemPage = -1
        self.nameList = []
        self.problemNum = len(totalProblemList) + 1

        problemSettingWindow.setObjectName("problemSettingWindow")
        problemSettingWindow.resize(1135, 733)
        problemSettingWindow.setStyleSheet("background: #a8d8fd")
        self.headLabel = QtWidgets.QLabel(problemSettingWindow)
        self.headLabel.setGeometry(QtCore.QRect(30, 30, 316, 44))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.headLabel.sizePolicy().hasHeightForWidth())
        self.headLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("나눔스퀘어 ExtraBold")
        font.setPointSize(30)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(10)
        self.headLabel.setFont(font)
        self.headLabel.setStyleSheet("font: 81 30pt \"나눔스퀘어 ExtraBold\";")
        self.headLabel.setObjectName("headLabel")
        self.problemNumLabel = QtWidgets.QLabel(problemSettingWindow)
        self.problemNumLabel.setGeometry(QtCore.QRect(30, 120, 100, 22))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.problemNumLabel.sizePolicy().hasHeightForWidth())
        self.problemNumLabel.setSizePolicy(sizePolicy)
        self.problemNumLabel.setMinimumSize(QtCore.QSize(100, 20))
        self.problemNumLabel.setStyleSheet("font: 75 15pt \"나눔스퀘어 Bold\";")
        self.problemNumLabel.setObjectName("problemNumLabel")
        self.problemTypeLabel = QtWidgets.QLabel(problemSettingWindow)
        self.problemTypeLabel.setGeometry(QtCore.QRect(30, 190, 101, 22))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.problemTypeLabel.sizePolicy().hasHeightForWidth())
        self.problemTypeLabel.setSizePolicy(sizePolicy)
        self.problemTypeLabel.setMinimumSize(QtCore.QSize(100, 20))
        self.problemTypeLabel.setStyleSheet("font: 75 15pt \"나눔스퀘어 Bold\";")
        self.problemTypeLabel.setObjectName("problemTypeLabel")
        self.problemTypeComboBox = QtWidgets.QComboBox(problemSettingWindow)
        self.problemTypeComboBox.setGeometry(QtCore.QRect(30, 230, 81, 22))
        self.problemTypeComboBox.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                               "font: 12pt \"나눔스퀘어\";")
        self.problemTypeComboBox.setObjectName("problemTypeComboBox")
        self.problemTypeComboBox.addItem("선택")
        self.problemTypeComboBox.addItem("객관식")
        self.problemTypeComboBox.addItem("주관식")
        self.problemTypeComboBox.addItem("서술형")
        self.problemTypeComboBox.currentIndexChanged.connect(self.problemTypeSelected)
        self.pageOfProblemInput = QtWidgets.QLineEdit(problemSettingWindow)
        self.pageOfProblemInput.setGeometry(QtCore.QRect(30, 340, 111, 24))
        self.pageOfProblemInput.setAutoFillBackground(False)
        self.pageOfProblemInput.setStyleSheet("font: 12pt \"나눔스퀘어\";")
        self.pageOfProblemInput.setText("")
        self.pageOfProblemInput.setObjectName("pageOfProblemInput")
        self.problemScoreLabel = QtWidgets.QLabel(problemSettingWindow)
        self.problemScoreLabel.setGeometry(QtCore.QRect(30, 400, 100, 22))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.problemScoreLabel.sizePolicy().hasHeightForWidth())
        self.problemScoreLabel.setSizePolicy(sizePolicy)
        self.problemScoreLabel.setMinimumSize(QtCore.QSize(100, 20))
        self.problemScoreLabel.setStyleSheet("font: 75 15pt \"나눔스퀘어 Bold\";")
        self.problemScoreLabel.setObjectName("problemScoreLabel")
        self.scoreInput = QtWidgets.QLineEdit(problemSettingWindow)
        self.scoreInput.setGeometry(QtCore.QRect(30, 440, 111, 24))
        self.scoreInput.setStyleSheet("font: 12pt \"나눔스퀘어\";")
        self.scoreInput.setText("")
        self.scoreInput.setObjectName("scoreInput")
        self.problemPageLabel = QtWidgets.QLabel(problemSettingWindow)
        self.problemPageLabel.setGeometry(QtCore.QRect(30, 300, 316, 22))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.problemPageLabel.sizePolicy().hasHeightForWidth())
        self.problemPageLabel.setSizePolicy(sizePolicy)
        self.problemPageLabel.setMinimumSize(QtCore.QSize(100, 20))
        self.problemPageLabel.setStyleSheet("font: 75 15pt \"나눔스퀘어 Bold\";")
        self.problemPageLabel.setObjectName("problemPageLabel")
        self.btnSetProblemArea = QtWidgets.QPushButton(problemSettingWindow)
        self.btnSetProblemArea.setGeometry(QtCore.QRect(730, 490, 191, 50))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnSetProblemArea.sizePolicy().hasHeightForWidth())
        self.btnSetProblemArea.setSizePolicy(sizePolicy)
        self.btnSetProblemArea.setMinimumSize(QtCore.QSize(140, 50))
        font = QtGui.QFont()
        font.setFamily("나눔스퀘어 ExtraBold")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(10)
        self.btnSetProblemArea.setFont(font)
        self.btnSetProblemArea.setStyleSheet("font: 81 \"나눔스퀘어 ExtraBold\";\n"
                                             "color: rgb(255, 255, 255);\n"
                                             "background-color: rgb(0, 85, 255);")
        self.btnSetProblemArea.setObjectName("btnSetProblemArea")
        self.btnSetProblemArea.clicked.connect(self.onAreaButtonClicked)
        self.instructionLabel = QtWidgets.QLabel(problemSettingWindow)
        self.instructionLabel.setGeometry(QtCore.QRect(560, 120, 531, 331))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.instructionLabel.sizePolicy().hasHeightForWidth())
        self.instructionLabel.setSizePolicy(sizePolicy)
        self.instructionLabel.setMinimumSize(QtCore.QSize(0, 180))
        self.instructionLabel.setStyleSheet("font: 75 11pt \"나눔스퀘어 Bold\";\n"
                                            "color: rgb(67, 67, 67);\n"
                                            "background-color: rgb(238, 238, 238);")
        self.instructionLabel.setFrameShape(QtWidgets.QFrame.Panel)
        self.instructionLabel.setFrameShadow(QtWidgets.QFrame.Plain)
        self.instructionLabel.setLineWidth(1)
        self.instructionLabel.setObjectName("instructionLabel")
        self.OCRsubjectiveAnswerInput = QtWidgets.QLineEdit(problemSettingWindow)
        self.OCRsubjectiveAnswerInput.setGeometry(QtCore.QRect(30, 540, 471, 24))
        self.OCRsubjectiveAnswerInput.setStyleSheet("font: 12pt \"나눔스퀘어\";")
        self.OCRsubjectiveAnswerInput.setText("")
        self.OCRsubjectiveAnswerInput.setObjectName("OCRsubjectiveAnswerInput")
        self.subjectiveAnswerLabel = QtWidgets.QLabel(problemSettingWindow)
        self.subjectiveAnswerLabel.setGeometry(QtCore.QRect(30, 500, 511, 30))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.subjectiveAnswerLabel.sizePolicy().hasHeightForWidth())
        self.subjectiveAnswerLabel.setSizePolicy(sizePolicy)
        self.subjectiveAnswerLabel.setMinimumSize(QtCore.QSize(100, 30))
        font = QtGui.QFont()
        font.setFamily("나눔스퀘어 Bold")
        font.setPointSize(13)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.subjectiveAnswerLabel.setFont(font)
        self.subjectiveAnswerLabel.setStyleSheet("font: 75 \"나눔스퀘어 Bold\";")
        self.subjectiveAnswerLabel.setObjectName("subjectiveAnswerLabel")
        self.problemNumLabel_num = QtWidgets.QLabel(problemSettingWindow)
        self.problemNumLabel_num.setGeometry(QtCore.QRect(140, 120, 100, 22))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.problemNumLabel_num.sizePolicy().hasHeightForWidth())
        self.problemNumLabel_num.setSizePolicy(sizePolicy)
        self.problemNumLabel_num.setMinimumSize(QtCore.QSize(100, 20))
        self.problemNumLabel_num.setStyleSheet("font: 75 15pt \"나눔스퀘어 Bold\";")
        self.problemNumLabel_num.setObjectName("problemNumLabel_num")
        self.btnSave = QtWidgets.QPushButton(problemSettingWindow)
        self.btnSave.setGeometry(QtCore.QRect(890, 640, 198, 50))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnSave.sizePolicy().hasHeightForWidth())
        self.btnSave.setSizePolicy(sizePolicy)
        self.btnSave.setMinimumSize(QtCore.QSize(140, 50))
        self.btnSave.setStyleSheet("font: 81 24pt \"나눔스퀘어 ExtraBold\";\n"
                                   "color: rgb(255, 255, 255);\n"
                                   "background-color: rgb(0, 85, 255);")
        self.btnSave.setObjectName("btnSave")
        self.btnSave.clicked.connect((self.onFinishButtonClicked))
        self.btnTempSave = QtWidgets.QPushButton(problemSettingWindow)
        self.btnTempSave.setGeometry(QtCore.QRect(720, 640, 140, 50))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnTempSave.sizePolicy().hasHeightForWidth())
        self.btnTempSave.setSizePolicy(sizePolicy)
        self.btnTempSave.setMinimumSize(QtCore.QSize(140, 50))
        self.btnTempSave.setStyleSheet("font: 81 24pt \"나눔스퀘어 ExtraBold\";\n"
                                       "color: rgb(255, 255, 255);\n"
                                       "background-color: rgb(83, 138, 255);")
        self.btnTempSave.setObjectName("btnTempSave")
        self.btnTempSave.clicked.connect((self.onNextButtonClicked))

        self.retranslateUi(problemSettingWindow)
        QtCore.QMetaObject.connectSlotsByName(problemSettingWindow)

        self.currentWindow = problemSettingWindow

    def retranslateUi(self, problemSettingWindow):
        _translate = QtCore.QCoreApplication.translate
        problemSettingWindow.setWindowTitle(_translate("problemSettingWindow", "Form"))
        self.headLabel.setText(_translate("problemSettingWindow", "시험지 문제 설정"))
        self.problemNumLabel.setText(_translate("problemSettingWindow", "문제 번호:"))
        self.problemTypeLabel.setText(_translate("problemSettingWindow", "문제 유형"))
        self.problemTypeComboBox.setItemText(0, _translate("problemSettingWindow", "선택"))
        self.problemTypeComboBox.setItemText(1, _translate("problemSettingWindow", "객관식"))
        self.problemTypeComboBox.setItemText(2, _translate("problemSettingWindow", "주관식"))
        self.problemTypeComboBox.setItemText(3, _translate("problemSettingWindow", "서술형"))
        self.problemScoreLabel.setText(_translate("problemSettingWindow", "배점"))
        self.problemPageLabel.setText(_translate("problemSettingWindow", "문제가 위치하는 페이지"))
        self.btnSetProblemArea.setText(_translate("problemSettingWindow", "문제 마킹 영역 지정"))
        self.instructionLabel.setText(_translate("problemSettingWindow", "***문제 마킹 영역 지정 가이드***\n"
                                                                         "\n"
                                                                         "- 문제 유형과 문제 페이지를 입력한 후 실행해 주세요.\n"
                                                                         "\n"
                                                                         "- 객관식 문제인 경우: \n"
                                                                         "\n"
                                                                         "문제의 각 선택지 마킹 영역마다 좌상-우하 방향으로 드래그 후\n"
                                                                         "\n"
                                                                         "1번을 누르면, 그 영역은 마킹되어야 정답인 곳으로,\n"
                                                                         "\n"
                                                                         "2번을 누르면 그 영역은 마킹되면 오답인 곳으로 지정됩니다.\n"
                                                                         "\n"
                                                                         "모두 완료되면 1, 2 외의 키를 누르면 영역 지정이 종료됩니다.\n"
                                                                         "\n"
                                                                         "- 주관식, 서술형 문제인 경우 설명:\n"
                                                                         "\n"
                                                                         "문제 답을 기입하는 영역을 좌상-우하 방향으로 드래그한 후 아무 키나 눌러주세요."))
        self.subjectiveAnswerLabel.setText(
            _translate("problemSettingWindow", "주관식 문제 정답 텍스트 (OCR 이용 주관식 채점 시에만 입력해주세요)"))
        self.problemNumLabel_num.setText(_translate("problemSettingWindow", str(self.problemNum)))
        self.btnSave.setText(_translate("problemSettingWindow", "문제 설정 완료"))
        self.btnTempSave.setText(_translate("problemSettingWindow", "다음 문제"))

    def problemTypeSelected(self):
        if self.problemTypeComboBox.currentIndex() == 0:
            print("Error. Problem type is not selected")
        self.curProblemType = self.problemTypeComboBox.currentIndex()  # 1: 객관식  2: 주관식  3: 서술형

    def mouseCallbackROI(self, event, x, y, flags, param):  # 마우스 드래그 인식용 메소드
        if event == cv2.EVENT_LBUTTONDOWN:  # 마우스를 누르는 동안...
            self.mouse_is_pressing = True
            self.clickX, self.clickY = x, y
            self.clickXFirst = x
            self.clickYFirst = y
            print(x)
            print(y)

        elif event == cv2.EVENT_LBUTTONUP:  # 마우스 누르던 것을 떼었을 때
            self.mouse_is_pressing = False
            self.clickXLast = x
            self.clickYLast = y
            print(x)
            print(y)

    def mouseCallbackSpot(self, event, x, y, flags, param):  # 마우스 클릭 지점 인식용 메소드
        if event == cv2.EVENT_LBUTTONDOWN:
            self.mouse_is_pressing = True
            self.clickX, self.clickY = x, y
            self.clickCoordinates.append([self.clickX, self.clickY])

    def onAreaButtonClicked(self):  # 문제 영역 지정 버튼을 눌렀을 때의 동작

        # 빈 시험지에서 한 문제의 마킹 영역들을 지정하고
        # 각 영역마다 마킹되어야 맞는 건지의 여부를 넣기

        pageNum = int(self.pageOfProblemInput.text()) - 1  # 문제가 위치하는 페이지 번호, 이 번호는 0부터 시작

        # read unmarked image
        src = cv2.imread('./buffer/unprocessedBlankPaper_{}.jpg'.format(pageNum), cv2.IMREAD_COLOR)

        if self.problemTypeComboBox.currentIndex() == 1:  # 객관식 문제인 경우
            # 현재 문제의 마킹 영역 좌표와 각 영역의 정답 여부를 임시 저장하는 변수들
            curProblemCoordinates = []
            curProblemIsAnswers = []

            # 각 마킹 영역을 마우스 드래그로 지정 후, 각 영역별로 마킹이 되어야 하는지의 여부를 기록
            while True:
                cv2.imshow("warpedUnmarkedPaper", src)
                cv2.setMouseCallback('warpedUnmarkedPaper', self.mouseCallbackROI)

                print("Drag the area of each problem, starting from left-upper side, to right-under side")
                print("After that, press 1 if correct, press 2 if incorrect, else if all the choices are marked")
                keyInput = cv2.waitKey(0)
                dragCoordinates = [self.clickXFirst, self.clickYFirst, self.clickXLast, self.clickYLast]

                cv2.destroyAllWindows()
                print(dragCoordinates)

                if keyInput == ord('1'):  # 영역 지정후 1번 키를 누름 : 정답
                    print('correct')
                    curProblemIsAnswers.append(True)
                    curProblemCoordinates.append(dragCoordinates)
                elif keyInput == ord('2'):  # 영역 지정 후 2번 키를 누름 : 오답
                    print('incorrect')
                    curProblemIsAnswers.append(False)
                    curProblemCoordinates.append(dragCoordinates)
                else:  # 모든 영역을 지정했을 때 1, 2 외의 다른 키를 누름 : 문제 영역 마킹 끝
                    break

            self.curProblemPage = pageNum
            self.curProblemCoordinates = curProblemCoordinates
            self.curProblemIsAnswers = curProblemIsAnswers
            print("problem page: {}".format(self.curProblemPage))
            print("added coordinates: {}".format(self.curProblemCoordinates))
            print("added isAnswers: {}".format(self.curProblemIsAnswers))

        # 주관식, 서술형 문제인 경우
        elif self.problemTypeComboBox.currentIndex() == 2 or self.problemTypeComboBox.currentIndex() == 3:
            # 현재 문제의 마킹 영역 좌표와 각 영역의 정답 여부를 임시 저장하는 변수들
            curProblemCoordinates = []

            # 문제 답 기입 영역을 마우스 드래그로 지정하고 저장
            cv2.imshow("warpedUnmarkedPaper", src)
            cv2.setMouseCallback('warpedUnmarkedPaper', self.mouseCallbackROI)

            print("Drag the writing area of the problem, starting from left-upper side, to right-under side.")
            print("After that, press any key")
            keyInput = cv2.waitKey(0)
            dragCoordinates = [self.clickXFirst, self.clickYFirst, self.clickXLast, self.clickYLast]

            cv2.destroyAllWindows()
            print(dragCoordinates)
            curProblemCoordinates.append(dragCoordinates)

            self.curProblemPage = pageNum
            self.curProblemCoordinates = curProblemCoordinates
            self.curProblemIsAnswers = []
            print("problem page: {}".format(self.curProblemPage))
            print("added coordinates: {}".format(self.curProblemCoordinates))

        else:  # invalid problem type
            print("Error")

    def onNextButtonClicked(self):  # 다음 문제로 넘어가기 버튼을 눌렀을 때의 동작
        # 지금까지의 문제 정보 정리해 다음 UI에 넘기기
        self.totalProblemList.append(eachProblemInfo(self.curProblemType, self.curProblemCoordinates,
                                                     self.curProblemIsAnswers, float(self.scoreInput.text()),
                                                     self.curProblemPage, self.OCRsubjectiveAnswerInput.text()))
        problemSettingWindow = QtWidgets.QWidget()
        ui = UI_ProblemSetting()
        ui.setupUi(problemSettingWindow, self.totalProblemList, self.problemAmount, self.testPaperAmount, self.gradeWithOCR)
        problemSettingWindow.show()
        self.currentWindow.hide()

    def onFinishButtonClicked(self):  # 문제 메타데이터 입력 완료 버튼을 눌렀을 때의 동작.
        # 문제 취합 종료하고 취합된 모든 문제 메타데이터 넘기기

        # 마지막 문제의 정보 저장
        self.totalProblemList.append(eachProblemInfo(self.curProblemType, self.curProblemCoordinates,
                                                     self.curProblemIsAnswers, float(self.scoreInput.text()),
                                                     self.curProblemPage, self.OCRsubjectiveAnswerInput.text()))

        self.grader(self.totalProblemList)  # 지금까지의 메타데이터를 기반으로 채점하기


    def showPopupMarkedPaperInput(self):  # 마킹된 시험지의 파일 영역 표시 전 안내창
        popupMarked = QtWidgets.QWidget()
        popupMarked_UI = popupMarkedClass()
        popupMarked_UI.setupUi(popupMarked)
        popupMarked.show()
        while popupMarked_UI.proceed == 0:  # 다음 버튼이 눌리기까지 대기
            QtCore.QCoreApplication.processEvents()
        popupMarked.hide()


    def showPopupEdgeInstruction_1(self):
        popupEdge = QtWidgets.QWidget()
        popupEdge_UI = popupEdgeInstructionClass_1()
        popupEdge_UI.setupUi(popupEdge)
        popupEdge.show()
        while popupEdge_UI.proceed == 0:  # 다음 버튼이 눌리기까지 대기
            QtCore.QCoreApplication.processEvents()
        popupEdge.hide()


    def grader(self, totalProblemList):

        self.showPopupMarkedPaperInput()

        """
        각 마킹한 시험지들에서 마킹 정보를 뽑아 채점하고 점수 내기
        """
        print("Please enter the names in nameList.txt file, in sequence, with no duplication")
        print("Enter the pages, in order of name and page")
        # 마킹한 문제지들 입력
        fname = QFileDialog.getOpenFileNames()
        # self.label.setText(fname[0])    #해당 파일들의 절대 경로. 파일을 선택한 순서대로 정렬되네
        fileLocs = fname[0]

        print(fileLocs)

        # 문제지 세트별로 이름 입력 - txt 파일
        self.nameList = []
        nameFile = open("nameList.txt", "r", encoding='UTF8')
        nameCount = 0

        while True:
            name = nameFile.readline()
            if name == '' or name == '\n':
                break
            else:
                nameCount = nameCount + 1
                self.nameList.append(name)
                print("name input: {}".format(name))

        print("{} names entered".format(nameCount))
        nameFile.close()

        self.showPopupEdgeInstruction_1()

        unmarkedPapers = []

        for pageNum in range(self.testPaperAmount):
            # 마킹 안된 시험지들 읽어 오기
            unmarkedPaper = cv2.imread('./buffer/processedBlankPaper_{}.jpg'.format(pageNum), cv2.IMREAD_COLOR)
            # convert the images to grayscale
            unmarkedPaper = cv2.cvtColor(unmarkedPaper, cv2.COLOR_BGR2GRAY)
            unmarkedPapers.append(unmarkedPaper)

        pageNo = 0  # 시험의 몇 번째 페이지인지 카운트
        personNo = 0  # 몇 번째 사람인지 카운트
        isCorrectList = []  # 한 사람의 문제 정답 여부를 순서대로 배열
        marks = []  # 한 사람이 마킹한 번호들
        totalResults = []  # 최종 채점 결과들. personResult 클래스들의 집합임
        curProblemNo = 0  # 현재 채점중인 문제 번호

        # 각각 문제지 모서리 정리, 프로세싱 후 비마킹 시험지와 대비, 그리고 채점

        for imageLoc in fileLocs:  # 읽어온 각 마킹된 시험지마다
            # read marked image
            src = cv2.imread(imageLoc, cv2.IMREAD_COLOR)

            # 너무 이미지 용량이 크다면 리사이징
            height = src.shape[0]
            width = src.shape[1]

            if height >= width:
                resizeScale = 1000 / height
            else:
                resizeScale = 1000 / width
            src = cv2.resize(src, (int(width * resizeScale), int(height * resizeScale)), interpolation=cv2.INTER_AREA)

            print("Changed dimensions : ", src.shape)

            height, width, channel = src.shape

            # 현재 문제지 모서리 잘라내기
            cv2.imshow("markedOriginal", src)
            cv2.setMouseCallback('markedOriginal', self.mouseCallbackSpot)

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
            # dstUnmarked : warped testing paper with marks as original size
            warpedMarkedPaper = cv2.warpPerspective(src, matrix, (width, height))
            cv2.imshow("warpedmarkedPaper", warpedMarkedPaper)
            # cv2.imwrite('./buffer/warpedBlankPaper.jpg', warpedMarkedPaper)
            cv2.waitKey(0)

            # 현재 문제지를 blur 흑백화 등 처리하고 각각 채점 결과 내기
            markedPaper = copy.deepcopy(warpedMarkedPaper)

            # convert the images to grayscale
            markedPaper = cv2.cvtColor(markedPaper, cv2.COLOR_BGR2GRAY)

            # blur
            for i in range(10):
                markedPaper = cv2.GaussianBlur(markedPaper, (7, 7), 0)

            # debug
            cv2.imwrite('./buffer/debugMarked.jpg', markedPaper)
            cv2.imwrite('./buffer/debugUnmarked.jpg', unmarkedPapers[pageNo])

            # compute the Structural Similarity Index (SSIM) between the two
            # images, ensuring that the difference image is returned
            (score, diff) = compare_ssim(unmarkedPapers[pageNo], markedPaper, full=True)
            # diff = (diff * 255).astype("uint8")  # multiplication number can be changed!
            diff = (diff * 255).astype("uint8")
            # print("SSIM: {}".format(score))

            # threshold the difference image, followed by finding contours to
            # image binarization : classify every pixels as 0 or 1, not continuous one.
            # obtain the regions of the two input images that differ
            thresh = cv2.threshold(diff, 0, 255,
                                   cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

            cv2.imshow("Diff", diff)
            cv2.imshow("Thresh", thresh)

            cv2.waitKey(0)
            cv2.destroyAllWindows()

            # 시험지에서 마킹된 곳 파악, 정답과 비교, 채점

            while self.totalProblemList[curProblemNo].page == pageNo:
                if self.totalProblemList[curProblemNo].type == 1:  # 문제가 객관식인 경우
                    bestChoice = -1
                    bestValidity = -1
                    for choiceNo in range(len(self.totalProblemList[curProblemNo].areas)):  # 가장 마킹이 뚜렷하게 된 곳 골라내기
                        ROI = thresh[self.totalProblemList[curProblemNo].areas[choiceNo][1]:
                                     self.totalProblemList[curProblemNo].areas[choiceNo][3],
                              self.totalProblemList[curProblemNo].areas[choiceNo][0]:
                              self.totalProblemList[curProblemNo].areas[choiceNo][2]]  # 마킹 부분을 잘라낸 이미지

                        cv2.imshow("ROI", ROI)
                        cv2.waitKey(0)
                        cv2.destroyAllWindows()

                        unique, counts = np.unique(ROI, return_counts=True)  # 마킹된 정도, 즉 validity 체크
                        if 0 not in unique:
                            validity = 1
                        elif 255 not in unique:
                            validity = 0
                        else:
                            validity = counts[1] / (counts[0] + counts[1])

                        if validity > bestValidity:  # 만약 이 선택지의 마킹이 지금까지의 것들 중 가장 뚜렷하다면 이것을 마킹된 것으로 처리 갱신
                            bestChoice = choiceNo
                            bestValidity = validity

                    # 마킹한 것과 실제 답이 맞는지 확인
                    if self.totalProblemList[curProblemNo].isAnswer[bestChoice] is True:
                        isCorrectList.append(True)
                    else:
                        isCorrectList.append(False)
                    marks.append(bestChoice + 1)


                elif self.totalProblemList[curProblemNo].type == 2 and self.gradeWithOCR is True:  # 주관식 OCR 사용 채점 시
                    x = 1.0
                    y = 1.0
                    img = warpedMarkedPaper[self.totalProblemList[curProblemNo].areas[0][1]:
                                            self.totalProblemList[curProblemNo].areas[0][3],
                          self.totalProblemList[curProblemNo].areas[0][0]:
                          self.totalProblemList[curProblemNo].areas[0][2]]

                    # Rescaling the image (it's recommended if you’re working with images that have a DPI of less than 300 dpi):
                    img = cv2.resize(img, dsize=(0, 0), fx=x, fy=y,
                                     interpolation=cv2.INTER_LINEAR + cv2.INTER_CUBIC)  # 높이와 너비도 정확도에 영향, 작을수록 정확해
                    cv2.imshow("test", img)
                    print('x:', x, 'y:', y)

                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    cv2.imshow("gray", gray)

                    # Applying dilation and erosion to remove the noise (you may play with the kernel size depending on your data set):
                    kernel = np.ones((1, 1), np.uint8)
                    gray = cv2.dilate(gray, kernel, iterations=1)
                    gray = cv2.erode(gray, kernel, iterations=1)

                    # cv2.adaptiveThreshold(cv2.medianBlur(gray, 3), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)  #median blur가 더 정확할거라고 했지만 실제로 적용해보니 그렇지 않음.
                    blur = cv2.GaussianBlur(gray, (3, 3), 0)
                    cv2.imshow("blur", gray)

                    answerText = pytesseract.image_to_string(blur, lang='kor')  # 영어면 'euc'
                    print("주관식 답안: {}".format(answerText))

                    marks.append(answerText)
                    if answerText == self.totalProblemList[
                        curProblemNo].OCRsubjectiveAnswer:  # OCR 리딩 결과가 이전에 설정한 답과 일치할 시
                        isCorrectList.append(True)
                    else:  # OCR 리딩 결과 오답일 시
                        isCorrectList.append(False)


                elif (self.totalProblemList[curProblemNo].type == 2 and self.gradeWithOCR is False) \
                        or self.totalProblemList[curProblemNo].type == 3:  # 문제가 서술형인 경우 또는 주관식 OCR 미사용 채점 시
                    descriptiveUI = QtWidgets.QWidget()
                    descriptiveUI_2 = Ui_AutomaticScoringProgramUI10()
                    descriptiveUI_2.setupUi(descriptiveUI,
                                            warpedMarkedPaper[self.totalProblemList[curProblemNo].areas[0][1]:
                                                              self.totalProblemList[curProblemNo].areas[0][3],
                                            self.totalProblemList[curProblemNo].areas[0][0]:
                                            self.totalProblemList[curProblemNo].areas[0][2]],
                                            curProblemNo, self.totalProblemList[curProblemNo].score)
                    descriptiveUI.show()
                    while descriptiveUI_2.curScore == -1:  # 버튼이 눌리기까지 대기
                        QtCore.QCoreApplication.processEvents()
                    isCorrectList.append(descriptiveUI_2.curScore)
                    marks.append(-1)

                else:  # 문제 타입 인식 에러
                    print("Error")

                if curProblemNo == self.problemAmount - 1:
                    break
                else:
                    curProblemNo = curProblemNo + 1

            # 한 사람 분이 끝났는지 체크
            if pageNo == self.testPaperAmount - 1:  # 한 사람의 시험지의 마지막 장에 도달함 -> 기록 저장과 파라미터들 리셋
                totalResults.append(personResult(self.nameList[personNo], isCorrectList, marks))
                isCorrectList = []
                marks = []
                pageNo = 0
                personNo = personNo + 1
            else:  # 아직 이 사람의 채점할 페이지가 남은 상태. 다음 페이지 채점 필요
                pageNo = pageNo + 1

        # 임시 - 결과 보여주기
        for i in totalResults:
            print(i.name)
            print(i.isCorrectList)
            print(i.marks)

        # 결과창 로드
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_totalResult()
        self.ui.setupUi(self.window, totalProblemList, totalResults)
        self.hide()
        self.window.show()


class popupMarkedClass(object):
    def setupUi(self, Form):
        self.proceed = 0
        Form.setObjectName("Form")
        Form.resize(513, 180)
        Form.setStyleSheet("background: #a8d8fd")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(20, 10, 61, 81))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("pencil.png"))
        self.label.setObjectName("label")
        self.nameGuideLabel_1 = QtWidgets.QLabel(Form)
        self.nameGuideLabel_1.setGeometry(QtCore.QRect(100, 20, 391, 21))
        font = QtGui.QFont()
        font.setFamily("나눔스퀘어 Bold")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.nameGuideLabel_1.setFont(font)
        self.nameGuideLabel_1.setObjectName("nameGuideLabel_1")
        self.nameGuideLabel_2 = QtWidgets.QLabel(Form)
        self.nameGuideLabel_2.setGeometry(QtCore.QRect(100, 60, 401, 21))
        font = QtGui.QFont()
        font.setFamily("나눔스퀘어 Bold")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.nameGuideLabel_2.setFont(font)
        self.nameGuideLabel_2.setObjectName("nameGuideLabel_2")
        self.confirmButton = QtWidgets.QPushButton(Form)
        self.confirmButton.setGeometry(QtCore.QRect(200, 110, 140, 50))
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

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.nameGuideLabel_1.setText(_translate("Form", "마킹된 모든 학생들의 시험지 파일들을"))
        self.nameGuideLabel_2.setText(_translate("Form", "입력한 학생 이름, 페이지 순서대로 선택해 주세요"))
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
        Form.setWindowTitle(_translate("Form", "Form"))
        self.nameGuideLabel_1.setText(_translate("Form", "좌상 - 우상 - 우하 - 좌하 순서대로"))
        self.nameGuideLabel_2.setText(_translate("Form", "시험지 이미지의 모서리 부분을 클릭하고"))
        self.confirmButton.setText(_translate("Form", "계속"))
        self.nameGuideLabel_3.setText(_translate("Form", "엔터 키를 눌러주세요"))

    def onConfirmButtonClicked(self):
        self.proceed = 1

"""
if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    problemSettingWindow = QtWidgets.QWidget()
    ui = UI_ProblemSetting()
    ui.setupUi(problemSettingWindow)
    problemSettingWindow.show()
    sys.exit(app.exec_())
"""