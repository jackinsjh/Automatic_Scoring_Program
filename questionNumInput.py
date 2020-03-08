# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'questionNumInput.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from blankPaperInput import Ui_blankPaperInput

class Ui_QuestionNumInput(object):

    def confirmButtonClicked(self):
        problemAmount = self.problemNumInput.toPlainText()  # 문제 갯수
        testpaperAmount = self.paperNumInput.toPlainText()  # 한 시험지 세트의 총 페이지 수
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_blankPaperInput()
        self.ui.setupUi(self.window, problemAmount, testpaperAmount)
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


        self.retranslateUi(questionNumInput)
        QtCore.QMetaObject.connectSlotsByName(questionNumInput)

        """
        # original code
        questionNumInput.setObjectName("questionNumInput")
        questionNumInput.resize(371, 297)
        self.centralwidget = QtWidgets.QWidget(questionNumInput)
        self.centralwidget.setObjectName("centralwidget")
        self.btn_open = QtWidgets.QPushButton(self.centralwidget)
        self.btn_open.setGeometry(QtCore.QRect(110, 140, 141, 51))
        self.btn_open.setObjectName("btn_open")

        self.btn_open.clicked.connect(self.openWindow)
    
        
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(70, 40, 211, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setObjectName("label")
        questionNumInput.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(questionNumInput)
        self.statusbar.setObjectName("statusbar")
        questionNumInput.setStatusBar(self.statusbar)

        self.retranslateUi(questionNumInput)
        QtCore.QMetaObject.connectSlotsByName(questionNumInput)
        """

    def retranslateUi(self, questionNumInput):
        _translate = QtCore.QCoreApplication.translate
        questionNumInput.setWindowTitle(_translate("questionNumInput", "questionNumInput"))
        self.confirmButton.setText(_translate("questionNumInput", "Enter"))
        self.labelQuestionNum.setText(_translate("questionNumInput", "Enter the number of questions"))
        self.labelPaperNum.setText(_translate("questionNumInput", "Enter the number of pages of each test"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    questionNumInput = QtWidgets.QMainWindow()
    ui = Ui_QuestionNumInput()
    ui.setupUi(questionNumInput)
    questionNumInput.show()
    sys.exit(app.exec_())

