import sys

from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel
from PyQt5 import QtCore, QtGui, QtWidgets

import numpy as np
import cv2

from skimage.measure import compare_ssim
import argparse
import imutils

from totalResult import Ui_totalResult

class personResult:  # 한 사람의 시험지를 채점한 최종 결과
    def __init__(self, name, isCorrectList, marks):
        self.name = name  # 이름
        self.isCorrectList = isCorrectList  # 정답 여부 리스트
        self.marks = marks  # 마킹 리스트
    

class eachProblemInfo:  # 각 문제의 정보를 저장하는 데 사용하는 클래스
    def __init__(self, type, areas, isAnswer, score, page):
        self.type = type  # 문제 타입
        self.areas = areas  # 문제 마킹 영역 좌표들
        self.isAnswer = isAnswer  # 각 마킹 영역들이 맞는지 틀리는지의 리스트
        self.score = score  # 이 문제의 점수
        self.page = page  # 이 문제가 위치하는 페이지
    
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

    def __init__(self, totalProblemList, problemAmount, testPaperAmount):
        super().__init__()
        
        # 넘어온 파라미터들 저장
        self.problemAmount = problemAmount  # 넘어온 문제 수 정보 저장
        self.testPaperAmount = testPaperAmount  # 넘어온 페이지 수 정보 저장

        #함수 역할
        #UI요소별로 함수 설정 해둠
        #move(a,b)로 위치 선정. 절대값. a가 왼쪽에서 얼마나 떨어지는지, b가 위에서 얼마나 아래인지.

        self.curProblemType = -1
        self.curProblemCoordinates = []
        self.curProblemIsAnswers = []
        self.curProblemScore = -1
        self.curProblemPage = -1
        self.nameList = []

        self.totalProblemList = totalProblemList
        self.problemNum = len(totalProblemList) + 1

        self.comboBoxUI()
        self.buttonUI()
        self.labelUI()
        self.lineEditUI()
        self.initUI()


    #EditText
    def lineEditUI(self):
        self.pageOfProblemInput = QLineEdit(self)
        self.pageOfProblemInput.move(100, 350)
        self.pageOfProblemInput.resize(100, 30)

        self.scoreInput = QLineEdit(self)
        self.scoreInput.move(100, 535)
        self.scoreInput.resize(100, 30)


    #TextView
    def labelUI(self):

        labelQNum = QLabel('문제 번호', self)
        labelQNum.move(100, 100)

        labelQNum = QLabel(str(self.problemNum), self)
        labelQNum.move(100, 150)

        labelQType = QLabel('문제 분류 설정', self)
        labelQType.move(100, 200)

        labelQPage = QLabel('문제가 위치하는 페이지', self)
        labelQPage.move(100, 300)

        labelQScore = QLabel('배점', self)
        labelQScore.move(100, 500)

        labelQScoreName = QLabel('점', self)
        labelQScoreName.move(210, 538)



    #Button
    def buttonUI(self):

        btnSetProblemArea = QPushButton('문제 영역 지정', self)
        btnSetProblemArea.setToolTip('문제 영역 지정')
        btnSetProblemArea.move(100, 400)
        btnSetProblemArea.clicked.connect(self.onAreaButtonClicked)

        btnTempSave = QPushButton('다음 문제',self)
        btnTempSave.setToolTip('임시 저장 및 다음 문제로 넘어가기')
        btnTempSave.setStyleSheet('color:black; background:#58565b')
        btnTempSave.resize(100,50)
        btnTempSave.move(100, 700)
        btnTempSave.clicked.connect((self.onNextButtonClicked))

        btnSave = QPushButton('문제 설정 완료',self)
        btnSave.setToolTip('저장하기')
        btnSave.setStyleSheet('color:white; background:#424a9f')
        btnSave.resize(100,50)
        btnSave.move(400, 700)
        btnSave.clicked.connect((self.onFinishButtonClicked))


    def onAreaButtonClicked(self):  # 문제 영역 지정 버튼을 눌렀을 때의 동작

        # 빈 시험지에서 한 문제의 마킹 영역들을 지정하고
        # 각 영역마다 마킹되어야 맞는 건지의 여부를 넣기

        pageNum = int(self.pageOfProblemInput.text()) - 1  # 문제가 위치하는 페이지 번호, 이 번호는 0부터 시작

        # read unmarked image
        src = cv2.imread('./buffer/unprocessedBlankPaper_{}.jpg'.format(pageNum), cv2.IMREAD_COLOR)

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


    def onNextButtonClicked(self):  # 다음 문제로 넘어가기 버튼을 눌렀을 때의 동작
        # 지금까지의 문제 정보 정리해 다음 UI에 넘기기
        self.window = QtWidgets.QMainWindow()
        self.totalProblemList.append(eachProblemInfo(self.curProblemType, self.curProblemCoordinates,
                                                     self.curProblemIsAnswers, float(self.scoreInput.text()),
                                                     self.curProblemPage))
        self.ui = UI_ProblemSetting(self.totalProblemList, self.problemAmount, self.testPaperAmount)
        problemSetting.hide()
        self.window.show()


    def onFinishButtonClicked(self):  # 문제 메타데이터 입력 완료 버튼을 눌렀을 때의 동작.
        # 문제 취합 종료하고 취합된 모든 문제 메타데이터 넘기기

        # 마지막 문제의 정보 저장
        self.totalProblemList.append(eachProblemInfo(self.curProblemType, self.curProblemCoordinates,
                                                     self.curProblemIsAnswers, float(self.scoreInput.text()),
                                                     self.curProblemPage))

        self.grader(self.totalProblemList)  # 지금까지의 메타데이터를 기반으로 채점하기


    def comboBoxUI(self):  # 문제 유형 지정 콤보박스
        cbQType = QComboBox(self)
        cbQType.addItem('객관식')
        cbQType.addItem('주관식')
        cbQType.addItem('서술형')
        cbQType.move(100, 240)
        cbQType.activated.connect(self.problemTypeSelected)


    def problemTypeSelected(self, index):
        self.curProblemType = index

    def mouseCallbackSpot(self, event, x, y, flags, param):  # 마우스 클릭 지점 인식용 메소드
        if event == cv2.EVENT_LBUTTONDOWN:
            self.mouse_is_pressing = True
            self.clickX, self.clickY = x, y
            self.clickCoordinates.append([self.clickX, self.clickY])

    def totalProblemListShow(self, totalProblemList):  # 디버깅용 전체 문제 메타데이터 출력 메소드
        count = 1
        for problem in totalProblemList:
            print("=== Problem {} ===".format(count))
            problem.show()
            print("==================")
            count = count + 1

    def grader(self, totalProblemList):
        # totalProblemList 정보 정리해 놓기 - 문제영역들&정답여부, 각 문제 점수이름 순서

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
            markedPaper = warpedMarkedPaper

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
                bestChoice = -1
                bestValidity = -1
                for choiceNo in range(len(self.totalProblemList[curProblemNo].areas)):  # 가장 마킹이 뚜렷하게 된 곳 골라내기
                    ROI = thresh[self.totalProblemList[curProblemNo].areas[choiceNo][1]:self.totalProblemList[curProblemNo].areas[choiceNo][3],
                          self.totalProblemList[curProblemNo].areas[choiceNo][0]:self.totalProblemList[curProblemNo].areas[choiceNo][2]]  # 마킹 부분을 잘라낸 이미지

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
        # problemSetting.hide()
        self.window.show()


    # 화면 기본 설정
    def initUI(self):
        # self.showMaximized()
        self.setWindowTitle('채점 프로그램')
        self.show()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    problemSetting = QtWidgets.QMainWindow()
    ui = UI_ProblemSetting()
    ui.setupUi(problemSetting)
    problemSetting.show()
    sys.exit(app.exec_())