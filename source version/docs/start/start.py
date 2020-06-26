from PyQt5 import QtCore, QtGui, QtWidgets

#from questionNumInput import Ui_QuestionNumInput

class Ui_Form(object):
    """Main UI Class
    """
    def setupUi(self, Form):
        """This function is intended to set the initial UI.

        :param Form form: A form to be set
        :return: nothing
        """
        self.Form = Form
        Form.setObjectName("Form")
        Form.resize(1064, 562)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setStyleSheet("background: #a8d8fd")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(90, 110, 881, 131))
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
        self.startButton_2 = QtWidgets.QPushButton(Form)
        self.startButton_2.setGeometry(QtCore.QRect(400, 350, 281, 91))
        font = QtGui.QFont()
        font.setFamily("나눔스퀘어 ExtraBold")
        font.setPointSize(30)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(10)
        self.startButton_2.setFont(font)
        self.startButton_2.setStyleSheet("font: 81 30pt \"나눔스퀘어 ExtraBold\";\n"
"color: rgb(255, 255, 255);\n"
"background-color: rgb(0, 85, 255);")
        self.startButton_2.setObjectName("startButton_2")
        self.startButton_2.clicked.connect(self.startButtonClicked)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(320, 355, 61, 81))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("pencil.png"))
        self.label.setObjectName("label")

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Automatic Scoring Program"))
        Form.setWindowIcon(QtGui.QIcon("titleIcon.png"))
        self.label.setText(_translate("Form", "Automatic Scoring Program"))
        self.startButton_2.setText(_translate("Form", "시작"))

    def startButtonClicked(self):
        """Action when Start button is clicked - Move to the QuestionNumInput section
        :return: nothing
        """
        self.questionNumInput = QtWidgets.QWidget()
        self.ui = Ui_QuestionNumInput()
        self.ui.setupUi(self.questionNumInput)
        self.questionNumInput.show()
        self.Form.hide()



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
