# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AutomaticScoringProgramUI11-1.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!

import pandas as pd
from PyQt5 import QtCore, QtGui, QtWidgets

# from problemSetting import personResult, eachProblemInfo


class Ui_totalResult(object):
    def resultPushButtonClicked(self, data):
        data.to_csv("result.csv")

    def studentNameComboBoxClicked(self, name):
        self.currentStudentNameLabel.setText(name)

    def setupUi(self, Form, totalProblemList, totalResults):

        self.totalProblemList = totalProblemList
        self.totalResults = totalResults

        print("Are the parameters passed?")
        print(self.totalProblemList)
        print(self.totalResults)

        Form.setObjectName("Form")
        Form.resize(1181, 899)
        self.layoutWidget = QtWidgets.QWidget(Form)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 60, 1133, 751))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout_17 = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout_17.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_17.setObjectName("gridLayout_17")
        self.ResultPushButton = QtWidgets.QPushButton(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ResultPushButton.sizePolicy().hasHeightForWidth())
        self.ResultPushButton.setSizePolicy(sizePolicy)
        self.ResultPushButton.setMinimumSize(QtCore.QSize(140, 50))
        self.ResultPushButton.setStyleSheet("font: 81 24pt \"나눔스퀘어 ExtraBold\";\n"
"color: rgb(255, 255, 255);\n"
"background-color: rgb(0, 85, 255);")
        self.ResultPushButton.setObjectName("ResultPushButton")
        self.gridLayout_17.addWidget(self.ResultPushButton, 3, 1, 1, 1)

        # 엑셀로 만들기
        rData = pd.DataFrame(data=[1, 2, 3])  # TODO: 나중에 설정 해줘야함. 엑셀로 넣을 데이터
        self.ResultPushButton.clicked.connect(lambda: self.resultPushButtonClicked(rData))

        self.gridLayout_18 = QtWidgets.QGridLayout()
        self.gridLayout_18.setObjectName("gridLayout_18")
        spacerItem = QtWidgets.QSpacerItem(220, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_18.addItem(spacerItem, 1, 2, 1, 1)
        self.studentNameComboBox = QtWidgets.QComboBox(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.studentNameComboBox.sizePolicy().hasHeightForWidth())
        self.studentNameComboBox.setSizePolicy(sizePolicy)
        self.studentNameComboBox.setMinimumSize(QtCore.QSize(90, 25))
        self.studentNameComboBox.setStyleSheet("font: 75 12pt \"나눔스퀘어 Bold\";")
        self.studentNameComboBox.setObjectName("studentNameComboBox")
        self.studentNameComboBox.addItem("")
        self.studentNameComboBox.addItem("")
        self.studentNameComboBox.addItem("")
        self.studentNameComboBox.addItem("")

        # combobox 학생 이름 설정
        self.studentNameList = ["박서연", "손재호", "하은영", "박소영"]  # TODO: 학생 이름 가져와야함
        self.studentNameComboBox.addItems(self.studentNameList)

        # 학생 이름 선택시 label 변경
        self.studentNameComboBox.activated.connect(lambda: self.studentNameComboBoxClicked(self.studentNameComboBox.currentText()))


        self.gridLayout_18.addWidget(self.studentNameComboBox, 1, 3, 1, 1)
        self.studentLabel_5 = QtWidgets.QLabel(self.layoutWidget)
        self.studentLabel_5.setStyleSheet("font: 75 15pt \"나눔스퀘어 Bold\";")
        self.studentLabel_5.setObjectName("studentLabel_5")
        self.gridLayout_18.addWidget(self.studentLabel_5, 1, 0, 1, 1)
        self.currentStudentNameLabel = QtWidgets.QLabel(self.layoutWidget)
        self.currentStudentNameLabel.setStyleSheet("font: 75 15pt \"나눔스퀘어 Bold\";")
        self.currentStudentNameLabel.setObjectName("currentStudentNameLabel")
        self.gridLayout_18.addWidget(self.currentStudentNameLabel, 1, 1, 1, 1)
        self.testNameLabel_5 = QtWidgets.QLabel(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.testNameLabel_5.sizePolicy().hasHeightForWidth())
        self.testNameLabel_5.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("나눔스퀘어 ExtraBold")
        font.setPointSize(30)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(10)
        self.testNameLabel_5.setFont(font)
        self.testNameLabel_5.setStyleSheet("font: 81 30pt \"나눔스퀘어 ExtraBold\";")
        self.testNameLabel_5.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.testNameLabel_5.setObjectName("testNameLabel_5")
        self.gridLayout_18.addWidget(self.testNameLabel_5, 0, 0, 1, 4)
        spacerItem1 = QtWidgets.QSpacerItem(500, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_18.addItem(spacerItem1, 1, 4, 1, 1)
        self.gridLayout_17.addLayout(self.gridLayout_18, 0, 0, 1, 1)
        self.gridLayout_19 = QtWidgets.QGridLayout()
        self.gridLayout_19.setObjectName("gridLayout_19")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.scoreNameLabel_13 = QtWidgets.QLabel(self.layoutWidget)
        self.scoreNameLabel_13.setStyleSheet("font: 81 15pt \"나눔스퀘어 ExtraBold\";")
        self.scoreNameLabel_13.setObjectName("scoreNameLabel_13")
        self.verticalLayout_5.addWidget(self.scoreNameLabel_13)
        self.tableWidget = QtWidgets.QTableWidget(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy)
        self.tableWidget.setMinimumSize(QtCore.QSize(200, 525))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.verticalLayout_5.addWidget(self.tableWidget)
        self.gridLayout_19.addLayout(self.verticalLayout_5, 0, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_19.addItem(spacerItem2, 0, 1, 1, 1)
        self.line_9 = QtWidgets.QFrame(self.layoutWidget)
        self.line_9.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_9.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_9.setObjectName("line_9")
        self.gridLayout_19.addWidget(self.line_9, 0, 2, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_19.addItem(spacerItem3, 0, 3, 1, 1)
        self.gridLayout_20 = QtWidgets.QGridLayout()
        self.gridLayout_20.setObjectName("gridLayout_20")
        self.myScoreLabel = QtWidgets.QLabel(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.myScoreLabel.sizePolicy().hasHeightForWidth())
        self.myScoreLabel.setSizePolicy(sizePolicy)
        self.myScoreLabel.setMinimumSize(QtCore.QSize(50, 30))
        self.myScoreLabel.setStyleSheet("font: 81 15pt \"나눔스퀘어 ExtraBold\";")
        self.myScoreLabel.setObjectName("myScoreLabel")
        self.gridLayout_20.addWidget(self.myScoreLabel, 0, 2, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout_20.addItem(spacerItem4, 5, 0, 1, 1)
        self.wrongProblemLabel_5 = QtWidgets.QLabel(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.wrongProblemLabel_5.sizePolicy().hasHeightForWidth())
        self.wrongProblemLabel_5.setSizePolicy(sizePolicy)
        self.wrongProblemLabel_5.setMinimumSize(QtCore.QSize(110, 30))
        self.wrongProblemLabel_5.setStyleSheet("font: 81 18pt \"나눔스퀘어 ExtraBold\";")
        self.wrongProblemLabel_5.setObjectName("wrongProblemLabel_5")
        self.gridLayout_20.addWidget(self.wrongProblemLabel_5, 3, 0, 1, 2)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout_20.addItem(spacerItem5, 2, 0, 1, 1)
        self.myScoreLabel_5 = QtWidgets.QLabel(self.layoutWidget)
        self.myScoreLabel_5.setStyleSheet("font: 81 15pt \"나눔스퀘어 Bold\";")
        self.myScoreLabel_5.setObjectName("myScoreLabel_5")
        self.gridLayout_20.addWidget(self.myScoreLabel_5, 7, 0, 1, 1)
        self.wrongProblemListLabel_5 = QtWidgets.QLabel(self.layoutWidget)
        self.wrongProblemListLabel_5.setStyleSheet("font: 81 15pt \"나눔스퀘어 Bold\";")
        self.wrongProblemListLabel_5.setObjectName("wrongProblemListLabel_5")
        self.gridLayout_20.addWidget(self.wrongProblemListLabel_5, 4, 0, 1, 1)
        self.scoreLabel_5 = QtWidgets.QLabel(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scoreLabel_5.sizePolicy().hasHeightForWidth())
        self.scoreLabel_5.setSizePolicy(sizePolicy)
        self.scoreLabel_5.setMinimumSize(QtCore.QSize(80, 30))
        self.scoreLabel_5.setStyleSheet("font: 81 18pt \"나눔스퀘어 ExtraBold\";")
        self.scoreLabel_5.setObjectName("scoreLabel_5")
        self.gridLayout_20.addWidget(self.scoreLabel_5, 6, 0, 1, 1)
        self.scoreNameLabel_14 = QtWidgets.QLabel(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scoreNameLabel_14.sizePolicy().hasHeightForWidth())
        self.scoreNameLabel_14.setSizePolicy(sizePolicy)
        self.scoreNameLabel_14.setMinimumSize(QtCore.QSize(70, 30))
        self.scoreNameLabel_14.setStyleSheet("font: 81 15pt \"나눔스퀘어 ExtraBold\";")
        self.scoreNameLabel_14.setObjectName("scoreNameLabel_14")
        self.gridLayout_20.addWidget(self.scoreNameLabel_14, 0, 0, 1, 1)
        self.ProblemNumberLabel_5 = QtWidgets.QLabel(self.layoutWidget)
        self.ProblemNumberLabel_5.setMinimumSize(QtCore.QSize(100, 30))
        self.ProblemNumberLabel_5.setStyleSheet("font: 81 15pt \"나눔스퀘어 ExtraBold\";")
        self.ProblemNumberLabel_5.setObjectName("ProblemNumberLabel_5")
        self.gridLayout_20.addWidget(self.ProblemNumberLabel_5, 0, 1, 1, 1)
        self.resultTableView_5 = QtWidgets.QTableView(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.resultTableView_5.sizePolicy().hasHeightForWidth())
        self.resultTableView_5.setSizePolicy(sizePolicy)
        self.resultTableView_5.setMinimumSize(QtCore.QSize(200, 200))
        self.resultTableView_5.setObjectName("resultTableView_5")
        self.gridLayout_20.addWidget(self.resultTableView_5, 1, 0, 1, 3)
        self.gridLayout_19.addLayout(self.gridLayout_20, 0, 4, 1, 1)
        spacerItem6 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_19.addItem(spacerItem6, 0, 5, 1, 1)
        self.line_10 = QtWidgets.QFrame(self.layoutWidget)
        self.line_10.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_10.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_10.setObjectName("line_10")
        self.gridLayout_19.addWidget(self.line_10, 0, 6, 1, 1)
        self.gridLayout_17.addLayout(self.gridLayout_19, 2, 0, 1, 1)
        spacerItem7 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout_17.addItem(spacerItem7, 1, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.ResultPushButton.setText(_translate("Form", "엑셀 저장"))

        # combobox 학생 이름 설정
        self.studentNameList = ["박서연", "손재호", "하은영", "박소영"]  # TODO: 학생 이름 가져와야함
        for i in range(len(self.studentNameList)):
            self.studentNameComboBox.setItemText(i, _translate("Form", self.studentNameList[i]))


        self.studentLabel_5.setText(_translate("Form", "- 학생:"))

        #현재 설정한 학생의 이름을 넣은 Label
        self.currentStudentNameLabel.setText(_translate("Form", str(self.studentNameComboBox.currentText())))

        self.scoreNameLabel_13.setText(_translate("Form", "문제 처리 결과"))
        self.myScoreLabel.setText(_translate("Form", "문제"))
        self.wrongProblemLabel_5.setText(_translate("Form", "틀린 문제"))
        self.scoreLabel_5.setText(_translate("Form", "점수"))
        self.scoreNameLabel_14.setText(_translate("Form", "문제수: "))

        #TODO: 시험지 이름 받아오기
        testName = '[2020년 수능 영어]'
        self.testNameLabel_5.setText(_translate("Form", testName))

        # TODO: 전체 점수, 현재 점수 받아오기
        totalScore = 100
        myScore = 70
        myScoreLabelText = str(myScore) + ' / ' + str(totalScore)
        self.myScoreLabel.setText(_translate("Form", myScoreLabelText))

        # TODO: 틀린 문제 str 형태로 나열되서 받아오기
        wrongProblem = "2, 6, 10"
        self.wrongProblemListLabel_5.setText(_translate("Form", wrongProblem))

        self.scoreNameLabel_14.setText(_translate("Form", "문제수: "))

        # TODO: 문제수 받아오기
        problemNumber = '50'
        self.ProblemNumberLabel_5.setText(_translate("Form", problemNumber))

        self.myScoreLabel.setText(_translate("Form", "문제"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_totalResult()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
