from PyQt5 import QtCore, QtGui, QtWidgets
from openpyxl import Workbook

"""
진행 방향
problemSetting.py, descriptiveGradingUI.py --> totalResult.py

- 채점 최종 결과 창을 보여주고, 요청시 채점 결과를 액셀 파일로 export 함
- 액셀 파일은 프로그램의 경로에 result.xlsx 로 저장됨
- 프로그램의 마지막 부분
"""

class popupExcelSavedClass(object):  # 엑셀 파일로 결과 저장시 나오는 알림창
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
        self.nameGuideLabel_1.setGeometry(QtCore.QRect(140, 40, 261, 51))
        font = QtGui.QFont()
        font.setFamily("나눔스퀘어 Bold")
        font.setPointSize(25)
        font.setBold(True)
        font.setWeight(75)
        self.nameGuideLabel_1.setFont(font)
        self.nameGuideLabel_1.setObjectName("nameGuideLabel_1")
        self.confirmButton = QtWidgets.QPushButton(Form)
        self.confirmButton.setGeometry(QtCore.QRect(140, 140, 140, 50))
        self.confirmButton.clicked.connect(self.onConfirmButtonClicked)
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

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Automatic Scoring Program"))
        Form.setWindowIcon(QtGui.QIcon("titleIcon.png"))
        self.nameGuideLabel_1.setText(_translate("Form", "저장되었습니다!"))
        self.confirmButton.setText(_translate("Form", "뒤로"))

    def onConfirmButtonClicked(self):
        self.proceed = 1


class Ui_totalResult(object):  # 마지막 결과창 UI

    def showPopupExcelSaved(self):
        popupExcelSaved = QtWidgets.QWidget()
        popupExcelSaved_UI = popupExcelSavedClass()
        popupExcelSaved_UI.setupUi(popupExcelSaved)
        popupExcelSaved.show()
        while popupExcelSaved_UI.proceed == 0:  # 다음 버튼이 눌리기까지 대기
            QtCore.QCoreApplication.processEvents()
        popupExcelSaved.hide()


    def resultPushButtonClicked(self, data):  # 엑셀파일 생성 버튼 클릭 시 동작
        excelWorkbook = Workbook()
        excelSheet = excelWorkbook.active
        for personIndex in range(len(self.totalResults)):
            excelSheet.append(["이름: {}".format(self.totalResults[personIndex].name)])
            excelSheet.append\
                (["점수: {}".format("{} / {}".format(self.totalResults[personIndex].totalScore, self.fullScore))])
            excelSheet.append(["틀린 문제: {}".format(self.totalResults[personIndex].wrongProblemString)])
            excelSheet.append([""])
            excelSheet.append(["문제 번호", "문제 유형", "마킹한 답", "실제 정답", "정답 여부", "획득 점수"])


            for problemNum in range(len(self.totalProblemList)):

                # 문제 유형
                if self.totalProblemList[problemNum].type == 1:  # 객관식일 시
                    problemType = "객관식"
                elif self.totalProblemList[problemNum].type == 2:  # 주관식일 시
                    problemType = "주관식"
                elif self.totalProblemList[problemNum].type == 3:  # 서술형일 시
                    problemType = "서술형"
                else:
                    problemType = "-1"
                    print("Error")

                # 마킹
                if self.totalProblemList[problemNum].type == 1 or \
                        (self.totalProblemList[
                             problemNum].type == 2 and self.gradeWithOCR is True):  # 객관식이나 OCR 사용 주관식일 시
                    userMark = str(self.totalResults[personIndex].marks[problemNum])
                else:  # OCR 미사용 주관식, 서술형일 시
                    userMark = "-"

                # 정답 마킹
                if self.totalProblemList[problemNum].type == 1:  # 객관식일 시
                    realMark = str(self.getAnswerOfProblem(self.totalProblemList[problemNum]))
                elif self.totalProblemList[problemNum].type == 1 or \
                        (self.totalProblemList[
                             problemNum].type == 2 and self.gradeWithOCR is True):  # OCR 사용 주관식일 시
                    realMark = str(self.totalProblemList[problemNum].OCRsubjectiveAnswer)
                else:  # OCR 미사용 주관식, 서술형일 시
                    realMark = "-"

                # 정답 여부
                if self.totalProblemList[problemNum].type == 1 or \
                        (self.totalProblemList[
                             problemNum].type == 2 and self.gradeWithOCR is True):  # 객관식, OCR 사용 주관식일 시
                    if self.totalResults[personIndex].isCorrectList[problemNum] is True:
                        isCorrect = "정답"
                    else:
                        isCorrect = "오답"
                elif (self.totalProblemList[problemNum].type == 2 and self.gradeWithOCR is False) or \
                        self.totalProblemList[problemNum].type == 3:  # OCR 미사용 주관식, 서술형일 시
                    isCorrect = "-"
                else:
                    isCorrect = "error"

                # 점수
                if self.totalProblemList[problemNum].type == 1 or \
                        (self.totalProblemList[
                             problemNum].type == 2 and self.gradeWithOCR is True):  # 객관식, OCR 사용 주관식일 시
                    if self.totalResults[personIndex].isCorrectList[problemNum] is True:  # 정답 시
                        givenScore = str(self.totalProblemList[problemNum].score)
                    else:  # 오답 시
                        givenScore = "0"
                elif (self.totalProblemList[problemNum].type == 2 and self.gradeWithOCR is False) or \
                        self.totalProblemList[problemNum].type == 3:  # OCR 미사용 주관식, 서술형일 시
                    givenScore = str(self.totalResults[personIndex].isCorrectList[problemNum])
                else:
                    givenScore = "error"

                excelSheet.append([problemNum + 1, problemType, userMark, realMark, isCorrect, givenScore])


            excelSheet.append([""])
            excelSheet.append(["--------------------------------------------------------------------------"])

        excelWorkbook.save('result.xlsx')

        self.showPopupExcelSaved()



    def studentNameComboBoxClicked(self, name):  # 위 체크박스에서 다른 사람을 선택시 화면 정보를 다른 사람의 것으로 변경함
        
        # 해당 시험자 위치 탐색
        personLocation = 0  # 결과 리스트에서 해당 사람이 위치하는 인덱스
        # 해당 이름의 시험자가 위치하는 인덱스 찾기
        while self.totalResults[personLocation].name != name:
            personLocation = personLocation + 1

        self.changeInfo(personLocation)  # 화면 정보를 다른 사람의 것으로 변경함

    def setupUi(self, Form, totalProblemList, totalResults, gradeWithOCR):  # 초기 UI 세팅

        self.totalProblemList = totalProblemList  # 전달된 파라미터: 전체 문제들의 정보
        self.totalResults = totalResults  # 전달된 파라미터, 전체 시험자들의 정보
        self.gradeWithOCR = gradeWithOCR  # 전달된 파라미터, 주관식 채점에 OCR 사용 여부, True/False

        # debug
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
        # 엑셀로 만들기 버튼
        self.ResultPushButton.clicked.connect(self.resultPushButtonClicked)

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

        # combobox 학생 이름 설정
        self.studentNameList = []  # 학생 이름 리스트
        for person in self.totalResults:  # 학생 이름들 가져오기
            self.studentNameList.append(person.name)
            print("student added in result page : {}".format(person.name))
        self.studentNameComboBox.addItems(self.studentNameList)

        # 학생 이름 선택시 표시 정보들 변경
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
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        font = QtGui.QFont()
        font.setFamily("나눔스퀘어 ExtraBold")
        font.setPointSize(30)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(10)
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
        
        # 좌측 문제 처리 결과 테이블
        self.leftResultTable = QtWidgets.QTableWidget(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.leftResultTable.sizePolicy().hasHeightForWidth())
        self.leftResultTable.setSizePolicy(sizePolicy)
        self.leftResultTable.setMinimumSize(QtCore.QSize(200, 525))
        self.leftResultTable.setObjectName("tableWidget")
        self.leftResultTable.setColumnCount(5)
        self.leftResultTable.setRowCount(len(self.totalProblemList))
        # 헤더는 반드시 행과 열이 들어간 상태에서 삽입해야 함!
        self.leftResultTable.setHorizontalHeaderLabels(["문제 유형", "마킹", "정답 마킹", "정답 여부", "점수"])
        self.verticalLayout_5.addWidget(self.leftResultTable)
        
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

        self.rightResultTable = QtWidgets.QTableWidget(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rightResultTable.sizePolicy().hasHeightForWidth())
        self.rightResultTable.setSizePolicy(sizePolicy)
        self.rightResultTable.setMinimumSize(QtCore.QSize(200, 200))
        self.rightResultTable.setObjectName("rightResultTable")
        self.rightResultTable.setColumnCount(1)
        self.rightResultTable.setRowCount(3)
        # 헤더는 반드시 행과 열이 들어간 상태에서 삽입해야 함!
        self.rightResultTable.setVerticalHeaderLabels(["맞은 갯수", "틀린 갯수", "정답률"])
        self.gridLayout_20.addWidget(self.rightResultTable, 1, 0, 1, 3)

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
        Form.setWindowTitle(_translate("Form", "Automatic Scoring Program"))
        Form.setWindowIcon(QtGui.QIcon("titleIcon.png"))
        self.ResultPushButton.setText(_translate("Form", "엑셀 저장"))

        """
        화면 표시 정보 초기 설정
        """

        self.studentLabel_5.setText(_translate("Form", "- 학생:"))

        # 현재 설정한 학생의 이름을 넣은 Label
        self.currentStudentNameLabel.setText(_translate("Form", str(self.studentNameComboBox.currentText())))

        self.scoreNameLabel_13.setText(_translate("Form", "문제 처리 결과"))
        self.myScoreLabel.setText(_translate("Form", "문제"))
        self.wrongProblemLabel_5.setText(_translate("Form", "틀린 문제"))
        self.scoreLabel_5.setText(_translate("Form", "점수"))
        self.scoreNameLabel_14.setText(_translate("Form", "문제수: "))

        self.changeInfo(0)  # 맨 첫 번째 사람의 정보로 화면 정보 표시

        self.scoreNameLabel_14.setText(_translate("Form", "문제수: "))

        # 문제수 받아오기
        problemNumber = str(len(self.totalProblemList))
        self.ProblemNumberLabel_5.setText(_translate("Form", problemNumber))

        self.myScoreLabel.setText(_translate("Form", "문제"))

    def changeInfo(self, personLocation):  # 화면의 정보를 personLocation 인덱스에 있는 사람의 것으로 바꾸기

        self.currentStudentNameLabel.setText(self.totalResults[personLocation].name)  # 이름 레이블 변경

        # 전체 점수, 현재 점수 받아오기
        totalScore = 0
        myScore = 0
        problemCounter = 0
        for problem in self.totalProblemList:
            totalScore = totalScore + problem.score
            if problem.type == 1 or (problem.type == 2 and self.gradeWithOCR is True):  # 객관식 문제, OCR 사용 주관식 문제인 경우
                if self.totalResults[personLocation].isCorrectList[problemCounter] is True:
                    myScore = myScore + problem.score
            elif (problem.type == 2 and self.gradeWithOCR is False) or problem.type == 3:  # 서술형 문제인 경우
                myScore = myScore + self.totalResults[personLocation].isCorrectList[problemCounter]
            else:  # 문제 타입 에러
                print('Error')
            problemCounter = problemCounter + 1

        myScoreLabelText = str(myScore) + ' / ' + str(totalScore)
        self.fullScore = totalScore
        self.totalResults[personLocation].totalScore = myScore
        # self.myScoreLabel.setText(_translate("Form", myScoreLabelText))
        self.myScoreLabel_5.setText(myScoreLabelText)

        # 틀린 문제 str 형태로 나열되서 받아오기
        wrongProblem = []
        counter = 1
        for isCorrect in self.totalResults[personLocation].isCorrectList:
            if isCorrect is False or isCorrect == 0:
                wrongProblem.append(str(counter))
            counter = counter + 1
        wrongProblem = ', '.join(wrongProblem)
        if wrongProblem == '':
            wrongProblem = '없음'
        self.totalResults[personLocation].wrongProblemString = wrongProblem
        # self.wrongProblemListLabel_5.setText(_translate("Form", wrongProblem))
        self.wrongProblemListLabel_5.setText(wrongProblem)
        
        # 좌측 결과 테이블 데이터 삽입
        self.leftResultTable.clearContents()
        # QTableWidgetItem 파라미터 int 넣는 건 안 되더라... str은 됨
        for problemNum in range(len(self.totalProblemList)):
            # 문제 유형
            if self.totalProblemList[problemNum].type == 1:  # 객관식일 시
                self.leftResultTable.setItem(problemNum, 0, QtWidgets.QTableWidgetItem("객관식"))
            elif self.totalProblemList[problemNum].type == 2:  # 주관식일 시
                self.leftResultTable.setItem(problemNum, 0, QtWidgets.QTableWidgetItem("주관식"))
            elif self.totalProblemList[problemNum].type == 3:  # 서술형일 시
                self.leftResultTable.setItem(problemNum, 0, QtWidgets.QTableWidgetItem("서술형"))
            else:  # 에러 - 유효하지 않은 문제 타입
                print("error -> invalid problem type")

            # 마킹
            if self.totalProblemList[problemNum].type == 1 or \
                    (self.totalProblemList[problemNum].type == 2 and self.gradeWithOCR is True):  # 객관식이나 OCR 사용 주관식일 시
                self.leftResultTable.setItem(problemNum, 1, QtWidgets.QTableWidgetItem(
                    str(self.totalResults[personLocation].marks[problemNum])))
            else:  # OCR 미사용 주관식, 서술형일 시
                self.leftResultTable.setItem(problemNum, 1, QtWidgets.QTableWidgetItem("-"))

            # 정답
            if self.totalProblemList[problemNum].type == 1:  # 객관식일 시
                self.leftResultTable.setItem(problemNum, 2, QtWidgets.QTableWidgetItem(
                    str(self.getAnswerOfProblem(self.totalProblemList[problemNum]))))
            elif self.totalProblemList[problemNum].type == 1 or \
                    (self.totalProblemList[problemNum].type == 2 and self.gradeWithOCR is True):  # OCR 사용 주관식일 시
                self.leftResultTable.setItem(problemNum, 2, QtWidgets.QTableWidgetItem(
                    str(self.totalProblemList[problemNum].OCRsubjectiveAnswer)))
            else:  # OCR 미사용 주관식, 서술형일 시
                self.leftResultTable.setItem(problemNum, 2, QtWidgets.QTableWidgetItem("-"))

            # 정답 여부
            if self.totalProblemList[problemNum].type == 1 or \
                    (self.totalProblemList[problemNum].type == 2 and self.gradeWithOCR is True):  # 객관식, OCR 사용 주관식일 시
                if self.totalResults[personLocation].isCorrectList[problemNum] is True:
                    self.leftResultTable.setItem(problemNum, 3, QtWidgets.QTableWidgetItem("정답"))
                else:
                    self.leftResultTable.setItem(problemNum, 3, QtWidgets.QTableWidgetItem("오답"))
            elif (self.totalProblemList[problemNum].type == 2 and self.gradeWithOCR is False) or \
                    self.totalProblemList[problemNum].type == 3:  # OCR 미사용 주관식, 서술형일 시
                self.leftResultTable.setItem(problemNum, 3, QtWidgets.QTableWidgetItem("-"))
                
            # 점수
            if self.totalProblemList[problemNum].type == 1 or \
                    (self.totalProblemList[problemNum].type == 2 and self.gradeWithOCR is True):  # 객관식, OCR 사용 주관식일 시
                if self.totalResults[personLocation].isCorrectList[problemNum] is True:  # 정답 시
                    self.leftResultTable.setItem(problemNum, 4, QtWidgets.QTableWidgetItem(
                        str(self.totalProblemList[problemNum].score)))
                else:  # 오답 시
                    self.leftResultTable.setItem(problemNum, 4, QtWidgets.QTableWidgetItem("0"))
            elif (self.totalProblemList[problemNum].type == 2 and self.gradeWithOCR is False) or \
                    self.totalProblemList[problemNum].type == 3:  # OCR 미사용 주관식, 서술형일 시
                self.leftResultTable.setItem(problemNum, 4, QtWidgets.QTableWidgetItem(
                    str(self.totalResults[personLocation].isCorrectList[problemNum])))



        # 우측 결과 테이블 데이터 삽입
        self.rightResultTable.clearContents()
        # QTableWidgetItem 파라미터 int 넣는 건 안 되더라... str은 됨
        correctCounter = 0  # 맞은 갯수
        wrongCounter = 0  # 틀린 갯수
        for problem in self.totalResults[personLocation].isCorrectList:
            if problem is True or problem != 0:  # 맞는 문제인 경우 틀린 문제 리스트에서 배제
                correctCounter = correctCounter + 1
            else:  # 틀린 문제인 경우 틀린 문제 리스트에 추가
                wrongCounter = wrongCounter + 1

        self.rightResultTable.setItem(0, 0, QtWidgets.QTableWidgetItem(str(correctCounter)))  # 정답 수
        self.rightResultTable.setItem(1, 0, QtWidgets.QTableWidgetItem(str(wrongCounter)))  # 오답 수
        self.rightResultTable.setItem(2, 0, QtWidgets.QTableWidgetItem(str((correctCounter/(correctCounter + wrongCounter)) * 100) + "%"))  # 정답률

    def getAnswerOfProblem(self, problem):  # eachProblemInfo 클래스 object 를 넣으면 해당 문제의 정답 선택지 번호를 리턴함
        for choice in range(len(problem.areas)):
            if problem.isAnswer[choice] is True:
                return choice + 1

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_totalResult()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
