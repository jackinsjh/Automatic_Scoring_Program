# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'blankPaperInput.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_blankPaperInput(object):
    problemNum = -1

    def setupUi(self, blankPaperInput, problemNum):
        self.problemNum = problemNum

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




    def retranslateUi(self, blankPaperInput):
        _translate = QtCore.QCoreApplication.translate
        blankPaperInput.setWindowTitle(_translate("blankPaperInput", "MainWindow"))
        self.label.setText(_translate("blankPaperInput", "Welcome To This Window"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    blankPaperInput = QtWidgets.QMainWindow()
    ui = Ui_blankPaperInput()
    ui.setupUi(blankPaperInput)
    blankPaperInput.show()
    sys.exit(app.exec_())

