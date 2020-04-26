# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'questionNumInput.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from blankPaperInput import Ui_blankPaperInput

"""
실행

-이 파일이 프로그램의 첫 부분. 이 파일을 실행함으로써 프로그램이 실행됨
-nameList.txt 에 학생들의 이름을 한 줄에 하나씩 공백 없이 입력해 두기
-마킹되지 않은 시험지와 마킹된 학생들의 시험지 파일들을 준비. 현재 폴더에 테스트용 시험지들도 존재함
-현재 일부 프로그램 안내들은 팝업 등의 GUI 방식이 아닌, 콘솔창에 안내가 나오고 있음. 수정 고려 필요
"""

class Ui_QuestionNumInput(object):  # 맨 처음 뜨는 창. 문제 수와 한 시험의 총 페이지 수를 질문.

    def confirmButtonClicked(self):  # 확인 버튼 클릭시 동작
        problemAmount = int(self.problemNumInput.toPlainText())  # 시험의 문제 갯수
        testpaperAmount = int(self.paperNumInput.toPlainText())  # 한 시험지 세트의 총 페이지 수
        if self.check_useOCR.toPlainText() == "":  # OCR로 주관식 채점 여부 - 추후 변경 필요
            gradeWithOCR = True  # OCR로 주관식 채점 여부
        else:
            gradeWithOCR = False

        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_blankPaperInput()  # 다음 UI창인 blankPaperInput 창을 열기
        self.ui.setupUi(self.window, problemAmount, testpaperAmount, gradeWithOCR)
        questionNumInput.hide()
        self.window.show()
        
    def setupUi(self, questionNumInput):
        questionNumInput.setObjectName("questionNumInput")
        questionNumInput.resize(400, 300)
        self.labelQuestionNum = QtWidgets.QLabel(questionNumInput)
        self.labelQuestionNum.setGeometry(QtCore.QRect(80, 60, 181, 16))
        self.labelQuestionNum.setObjectName("labelQuestionNum")
        self.problemNumInput = QtWidgets.QTextEdit(questionNumInput)
        self.problemNumInput.setGeometry(QtCore.QRect(80, 90, 201, 31))
        self.problemNumInput.setObjectName("textEditQuestionNum")
        self.labelPaperNum = QtWidgets.QLabel(questionNumInput)
        self.labelPaperNum.setGeometry(QtCore.QRect(80, 140, 181, 16))
        self.labelPaperNum.setObjectName("labelPaperNum")
        self.paperNumInput = QtWidgets.QTextEdit(questionNumInput)
        self.paperNumInput.setGeometry(QtCore.QRect(80, 170, 201, 31))
        self.paperNumInput.setObjectName("textEditPaperNum")
        self.confirmButton = QtWidgets.QPushButton(questionNumInput)
        self.confirmButton.setGeometry(QtCore.QRect(160, 220, 75, 31))
        self.confirmButton.setObjectName("conFirmButton")
        self.confirmButton.clicked.connect((self.confirmButtonClicked))
        self.check_useOCR = QtWidgets.QTextEdit(questionNumInput)  # OCR로 주관식 채점 여부
        self.check_useOCR.setGeometry(QtCore.QRect(160, 270, 75, 31))
        self.check_useOCR.setObjectName("check_useOCR")

        self.retranslateUi(questionNumInput)
        QtCore.QMetaObject.connectSlotsByName(questionNumInput)

    def retranslateUi(self, questionNumInput):
        _translate = QtCore.QCoreApplication.translate
        questionNumInput.setWindowTitle(_translate("questionNumInput", "questionNumInput"))
        self.confirmButton.setText(_translate("questionNumInput", "Enter"))
        self.labelQuestionNum.setText(_translate("questionNumInput", "Enter the number of questions"))
        self.labelPaperNum.setText(_translate("questionNumInput", "Number of pages of each test"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    questionNumInput = QtWidgets.QMainWindow()
    ui = Ui_QuestionNumInput()
    ui.setupUi(questionNumInput)
    questionNumInput.show()
    sys.exit(app.exec_())

