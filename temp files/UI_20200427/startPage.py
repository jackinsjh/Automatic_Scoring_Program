# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'startPage.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets

from questionNumInput import Ui_QuestionNumInput


class Ui_StartPage(object):

    def startButtonClicked(self):  # 버튼 클릭시 동작
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_QuestionNumInput()  # 다음 UI창 열기
        startPage.hide()
        self.window.show()

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1180, 800)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setStyleSheet("background: #a8d8fd")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(150, 210, 881, 131))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(48)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setStyleSheet("background: rgb(189, 189, 189)")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.startButton = QtWidgets.QPushButton(Form)
        self.startButton.setGeometry(QtCore.QRect(460, 480, 281, 91))
        font = QtGui.QFont()
        font.setFamily("나눔스퀘어 ExtraBold")
        font.setPointSize(32)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(10)
        self.startButton.setFont(font)
        self.startButton.setStyleSheet("font: 81 32pt \"나눔스퀘어 ExtraBold\";\n"
"color: rgb(255, 255, 255);\n"
"background-color: rgb(0, 85, 255);")
        self.startButton.setObjectName("startButton")
        self.startButton.clicked.connect((self.startButtonClicked))

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Automatic Scoring Program"))
        self.label.setText(_translate("Form", "Automatic Scoring Program"))
        self.startButton.setText(_translate("Form", "채점하기"))

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    startPage = QtWidgets.QMainWindow()
    ui = Ui_StartPage()
    ui.setupUi(startPage)
    startPage.show()
    sys.exit(app.exec_())
