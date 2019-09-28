import sys

from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel

class guiMain(QWidget):
    def __init__(self):
        super().__init__()

        #함수 역할
        #UI요소별로 함수 설정 해둠
        #move(a,b)로 위치 선정. 절대값. a가 왼쪽에서 얼마나 떨어지는지, b가 위에서 얼마나 아래인지.
        self.comboBoxUI()
        self.radioButtonUI()
        self.buttonUI()
        self.labelUI()
        self.lineEditUI()
        self.initUI()

    #EditText
    def lineEditUI(self):
        lineEditQNums = QLineEdit(self)
        lineEditQNums.move(800, 60)

        lineEditQMemo = QLineEdit(self)
        lineEditQMemo.move(1105, 270)
        lineEditQMemo.resize(270, 200)
        lineEditQMemo.setText("문제에 대한 메모 내용")

        lineEditQScore = QLineEdit(self)
        lineEditQScore.move(1105, 535)
        lineEditQScore.resize(100, 30)

    #TextView
    def labelUI(self):
        labelQNums = QLabel('문제 개수', self)
        labelQNums.move(800, 20)

        labelQNumbers = QLabel('문제', self)
        labelQNumbers.move(960, 63)

        labelQNum = QLabel('문제 번호', self)
        labelQNum.move(800, 100)

        labelQType = QLabel('문제 분류 설정', self)
        labelQType.move(800, 200)

        labelTestSheetOpen = QLabel('시험지 펼치기', self)
        labelTestSheetOpen.move(1100, 20)

        labelMakeTestSheet = QLabel('정답지 만들기', self)
        labelMakeTestSheet.move(1100, 200)

        labelQScore = QLabel('배점', self)
        labelQScore.move(1100, 500)

        labelQScoreName = QLabel('점', self)
        labelQScoreName.move(1210, 538)

        basicLabelFont = labelQNums.font()
        basicLabelFont.setPointSize(20)
        basicLabelFont.setBold(True)

        #글씨체 및 속성 설정
        font1 = labelQNum.font()
        font1.setFamily('Times New Roman')
        font1.setPointSize(15)
        font1.setBold(True)

        font2 = labelQNum.font()
        font2.setFamily('Times New Roman')
        font2.setPointSize(12)
        font2.setBold(True)

        #Font 설정
        labelQNums.setFont(basicLabelFont)
        labelQNum.setFont(basicLabelFont)
        labelQType.setFont(basicLabelFont)
        labelTestSheetOpen.setFont(basicLabelFont)
        labelMakeTestSheet.setFont(basicLabelFont)
        labelQScore.setFont(basicLabelFont)
        labelQScoreName.setFont(font2)

    #Button
    def buttonUI(self):
        btnGetImage = QPushButton('시험지 가져오기', self)
        btnGetImage.setToolTip('시험지 가져오기 버튼')
        btnGetImage.resize(btnGetImage.sizeHint())
        btnGetImage.move(400, 200)

        btnVertexSelect = QPushButton('꼭지점 설정', self)
        btnVertexSelect.setToolTip('꼭지점 설정 버튼')
        btnVertexSelect.resize(btnVertexSelect.sizeHint())
        btnVertexSelect.move(1300, 103)

        btn2 = QPushButton('문제 부분 그리기', self)
        btn2.setToolTip('문제 부분 그리기 버튼')
        btn2.resize(btn2.sizeHint())
        btn2.move(1105, 240)

        btnDrag = QPushButton('문제 지우기',self)
        btnDrag.setToolTip('문제 지우기 선택')
        btnDrag.resize(btnDrag.sizeHint())
        btnDrag.move(1300, 240)

        btnTempSave = QPushButton('다음 문제',self)
        btnTempSave.setToolTip('임시 저장 및 다음 문제로 넘어가기')
        btnTempSave.setStyleSheet('color:black; background:#58565b')
        btnTempSave.resize(100,50)
        btnTempSave.move(1700, 900)

        btnSave = QPushButton('전체 저장',self)
        btnSave.setToolTip('저장하기')
        btnSave.setStyleSheet('color:white; background:#424a9f')
        btnSave.resize(100,50)
        btnSave.move(1810, 900)

        #button이 어떤 역할을 할지 각각의 함수로 표현. 각 버튼의 역할 고정.
        btnGetImage.clicked.connect(self.pushButtonClicked)
        btnVertexSelect.clicked.connect(self.clickMethod1)
        btn2.clicked.connect(self.clickMethod2)
        btnDrag.clicked.connect(self.clickMethodDrag)
        btnTempSave.clicked.connect(self.clickMethodDragComplete)
        btnSave.clicked.connect(self.clickMethod3)

    #사진 가져오기 함수. 현재 제대로 작동 안함.
    def pushButtonClicked(self):
        fname = QFileDialog.getOpenFileName(self)
        #self.label.setText(fname[0])    #해당 파일의 절대 경로

        testSheet = QLabel(self)
        testSheet.resize(400, 400)
        testSheet.move(100, 100)
        pixmap = QPixmap(fname[0])
        testSheet.setPixmap(pixmap)
        testSheet.show()

    def clickMethod1(self):
        #그리기 눌렀을 때 해야할 일
        print("그리기")

    def clickMethod2(self):
        #지우기 눌렀을 때 해야할 일
        print("지우기")

    def clickMethodDrag(self):
        #드래그하는 작동
        print("드래그하기")

    def clickMethodDragComplete(self):
        #드래그 완료
        print("Drag Complete")

    def clickMethod3(self):
        buttonReplay = QMessageBox.question(self,"message","저장하시겠습니까?",QMessageBox.Yes, QMessageBox.Cancel)
        if buttonReplay == QMessageBox.Yes:
            print("저장완료")
            #다음 사진으로 넘어가기 or 다른거...?
            sys.exit()
        if buttonReplay == QMessageBox.Cancel:
            print("저장되지 않았습니다.")

    #radioButton
    def radioButtonUI(self):
        groupBox = QGroupBox(self)
        groupBox.move(1100, 60)
        groupBox.resize(170, 80)

        self.radio1 = QRadioButton('그대로 입력',self)
        self.radio1.move(1110, 75)
        self.radio1.setCheckable(True)
        self.radio1.clicked.connect((self.radioButtonClicked))

        self.radio2 = QRadioButton('수동으로 펼치기',self)
        self.radio2.move(1110, 105)
        self.radio2.clicked.connect(self.radioButtonClicked)

        #self.statusBar = QStatusBar(self)
        #self.setStatusBar(self.statusBar)

    def radioButtonClicked(self):
        msg = ""
        if self.radio1.isChecked():
            msg = "그대로 입력 선택"
        elif self.radio2.isChecked():
            msg = "수동으로 펼치기 선택"

        #self.statusBar.showMessage(msg)


    #스크롤 선택
    def comboBoxUI(self):
        cbQNum = QComboBox(self)
        cbQNum.addItem('문제1')
        cbQNum.addItem('문제2')
        cbQNum.addItem('문제3')
        cbQNum.addItem('문제4')
        cbQNum.move(800, 140)

        cbQType = QComboBox(self)
        cbQType.addItem('객관식')
        cbQType.addItem('주관식')
        cbQType.addItem('서술형')
        cbQType.move(800, 240)

        #cb.activated[str].connect(self.onActivated)

    #화면 기본 설정
    def initUI(self):
        self.showMaximized()
        self.setWindowTitle('채점 프로그램')
        self.show()

#실행
app = QApplication(sys.argv)
ex = guiMain()
sys.exit(app.exec_())