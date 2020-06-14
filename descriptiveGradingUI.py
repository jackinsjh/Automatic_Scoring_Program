from PyQt5 import QtCore, QtGui, QtWidgets
import cv2

"""
진행 방향
questionNumInput.py --> problemSetting.py, descriptiveGradingUI.py --> totalResult.py

- descriptiveGradingUI.py 는 problemSetting.py 에 종속되어 사용되는 모듈임
- 주관식/객관식 문제를 사용자가 임의로 채점할 때, problemSetting.py 가 call하며, 
답 마킹 영역과 점수 입력창을 제공하여 사용자가 직접 채점을 진행할 수 있게 함
"""


class descriptiveGradingUI(object):
    def setupUi(self, window, areaImage, problemNoInput, maxScoreInput):
        self.areaImage = areaImage  # 문제 영역을 자른 이미지
        self.problemNoInput = problemNoInput  # 문제 번호
        self.maxScoreInput = maxScoreInput  # 이 문제의 최대 점수
        self.window = window
        self.curScore = -1
        
        self.window.setObjectName("AutomaticScoringProgramUI10")
        self.window.resize(439, 354)
        self.window.setStyleSheet("background: #a8d8fd")
        self.scoreInput = QtWidgets.QLineEdit(self.window)
        self.scoreInput.setGeometry(QtCore.QRect(140, 190, 101, 41))
        self.scoreInput.setStyleSheet("font: 75 12pt \"나눔스퀘어 Bold\";")
        self.scoreInput.setText("")
        self.scoreInput.setObjectName("scoreInput")
        self.scoreInputSlash = QtWidgets.QLabel(self.window)
        self.scoreInputSlash.setEnabled(True)
        self.scoreInputSlash.setGeometry(QtCore.QRect(250, 190, 16, 41))
        self.scoreInputSlash.setMaximumSize(QtCore.QSize(81, 41))
        self.scoreInputSlash.setAcceptDrops(False)
        self.scoreInputSlash.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.scoreInputSlash.setStyleSheet("font: 81 20pt \"나눔스퀘어 ExtraBold\";")
        self.scoreInputSlash.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scoreInputSlash.setObjectName("scoreInputSlash")
        self.scoreInputHeader = QtWidgets.QLabel(self.window)
        self.scoreInputHeader.setGeometry(QtCore.QRect(170, 130, 111, 51))
        self.scoreInputHeader.setStyleSheet("font: 81 20pt \"나눔스퀘어 ExtraBold\";")
        self.scoreInputHeader.setObjectName("scoreInputHeader")
        self.problemNumHeader = QtWidgets.QLabel(self.window)
        self.problemNumHeader.setGeometry(QtCore.QRect(40, 90, 161, 22))
        self.problemNumHeader.setStyleSheet("font: 75 15pt \"나눔스퀘어 Bold\";")
        self.problemNumHeader.setObjectName("problemNumHeader")
        self.nextButton = QtWidgets.QPushButton(self.window)
        self.nextButton.setGeometry(QtCore.QRect(130, 260, 181, 61))
        self.nextButton.setStyleSheet("font: 81 24pt \"나눔스퀘어 ExtraBold\";\n"
"color: rgb(255, 255, 255);\n"
"background-color: rgb(0, 85, 255);")
        self.nextButton.setObjectName("nextButton")
        self.nextButton.clicked.connect(self.onNextButtonClicked)
        self.head = QtWidgets.QLabel(self.window)
        self.head.setGeometry(QtCore.QRect(40, 30, 351, 44))
        font = QtGui.QFont()
        font.setFamily("나눔스퀘어 ExtraBold")
        font.setPointSize(30)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(10)
        self.head.setFont(font)
        self.head.setStyleSheet("font: 81 30pt \"나눔스퀘어 ExtraBold\";")
        self.head.setObjectName("head")
        self.problemNum = QtWidgets.QLabel(self.window)
        self.problemNum.setGeometry(QtCore.QRect(200, 90, 31, 22))
        self.problemNum.setStyleSheet("font: 75 15pt \"나눔스퀘어 Bold\";")
        self.problemNum.setObjectName("problemNum")
        self.maxScore = QtWidgets.QLabel(self.window)
        self.maxScore.setEnabled(True)
        self.maxScore.setGeometry(QtCore.QRect(270, 190, 81, 41))
        self.maxScore.setMaximumSize(QtCore.QSize(81, 41))
        self.maxScore.setAcceptDrops(False)
        self.maxScore.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.maxScore.setStyleSheet("font: 81 20pt \"나눔스퀘어 ExtraBold\";")
        self.maxScore.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.maxScore.setObjectName("maxScore")

        self.retranslateUi(self.window)
        QtCore.QMetaObject.connectSlotsByName(self.window)

        # 문제 영역 이미지 띄우고, 버튼 누르면 점수 입력된 것 리턴, 창 닫기
        cv2.imshow("Automatic Scoring Program", self.areaImage)

    def retranslateUi(self, window):
        _translate = QtCore.QCoreApplication.translate
        window.setWindowTitle(_translate("AutomaticScoringProgramUI10", "Automatic Scoring Program"))
        window.setWindowIcon(QtGui.QIcon("titleIcon.png"))
        self.scoreInputSlash.setText(_translate("AutomaticScoringProgramUI10", "/"))
        self.scoreInputHeader.setText(_translate("AutomaticScoringProgramUI10", "점수 입력"))
        self.problemNumHeader.setText(_translate("AutomaticScoringProgramUI10", "서술형 문제 번호:"))
        self.nextButton.setText(_translate("AutomaticScoringProgramUI10", "다음"))
        self.head.setText(_translate("AutomaticScoringProgramUI10", "서술형 문제 수동 채점"))
        self.problemNum.setText(_translate("AutomaticScoringProgramUI10", str(self.problemNoInput + 1)))
        self.maxScore.setText(_translate("AutomaticScoringProgramUI10", str(self.maxScoreInput)))

    def onNextButtonClicked(self):
        cv2.destroyAllWindows()
        self.window.hide()
        self.curScore = int(self.scoreInput.text())  # 후에 problemSetting.py 에서 이 클래스의 curScore을 참조하여 점수를 추출


