# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainPage.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from ServerInterface import ServerInterface

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

INIT_WORK_DIR = '/'
SERVER = 'http://localhost:8080'

interface = ServerInterface(INIT_WORK_DIR, SERVER)

CurrentPath = '/'

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(711, 450)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.Upload = QtGui.QPushButton(self.centralwidget)
        self.Upload.setGeometry(QtCore.QRect(310, 10, 90, 28))
        self.Upload.setObjectName(_fromUtf8("Upload"))
        self.FolderExploer = QtGui.QListWidget(self.centralwidget)
        self.FolderExploer.setGeometry(QtCore.QRect(10, 40, 691, 381))
        self.FolderExploer.setObjectName(_fromUtf8("FolderExploer"))
        self.Download = QtGui.QPushButton(self.centralwidget)
        self.Download.setGeometry(QtCore.QRect(410, 10, 90, 28))
        self.Download.setObjectName(_fromUtf8("Download"))
        self.Back = QtGui.QPushButton(self.centralwidget)
        self.Back.setGeometry(QtCore.QRect(210, 10, 90, 28))
        self.Back.setObjectName(_fromUtf8("Back"))
        self.Enter = QtGui.QPushButton(self.centralwidget)
        self.Enter.setGeometry(QtCore.QRect(110, 10, 90, 28))
        self.Enter.setObjectName(_fromUtf8("Enter"))
        self.New = QtGui.QPushButton(self.centralwidget)
        self.New.setGeometry(QtCore.QRect(10, 10, 90, 28))
        self.New.setObjectName(_fromUtf8("New"))
        self.Rename = QtGui.QPushButton(self.centralwidget)
        self.Rename.setGeometry(QtCore.QRect(510, 10, 90, 28))
        self.Rename.setObjectName(_fromUtf8("Rename"))
        self.Remove = QtGui.QPushButton(self.centralwidget)
        self.Remove.setGeometry(QtCore.QRect(610, 10, 90, 28))
        self.Remove.setObjectName(_fromUtf8("Remove"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))

        MainWindow.setStatusBar(self.statusbar)

        fruit = ["Banana", "Apple", "Elderberry", "Clementine", "Fig", "Guava", "Mango", "Honeydew Melon"]
        self.FolderExploer.addItems(fruit)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        QtCore.QObject.connect(self.New, QtCore.SIGNAL(_fromUtf8("clicked()")), self.NewClick)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        QtCore.QObject.connect(self.Enter, QtCore.SIGNAL(_fromUtf8("clicked()")), self.EnterClick)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        QtCore.QObject.connect(self.Back, QtCore.SIGNAL(_fromUtf8("clicked()")), self.BackClick)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        QtCore.QObject.connect(self.Upload, QtCore.SIGNAL(_fromUtf8("clicked()")), self.UploadClick)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        QtCore.QObject.connect(self.Download, QtCore.SIGNAL(_fromUtf8("clicked()")), self.DwonloadClick)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        QtCore.QObject.connect(self.Rename, QtCore.SIGNAL(_fromUtf8("clicked()")), self.RenameClick)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        QtCore.QObject.connect(self.Remove, QtCore.SIGNAL(_fromUtf8("clicked()")), self.RemoveClick)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.Upload.setText(_translate("MainWindow", "Upload", None))
        self.Download.setText(_translate("MainWindow", "Download", None))
        self.Back.setText(_translate("MainWindow", "Back", None))
        self.Enter.setText(_translate("MainWindow", "Enter", None))
        self.New.setText(_translate("MainWindow", "New", None))
        self.Rename.setText(_translate("MainWindow", "Rename", None))
        self.Remove.setText(_translate("MainWindow", "Remove", None))

    def NewClick(self):
        self.dialog = QtGui.QInputDialog(self.centralwidget)
        NewName, ok = QtGui.QInputDialog.getText(self.dialog, "InputDialog",  "Please input the name" )
        if ok:
            result = interface.mkdir(NewName)
            if result is not None:
                MsgBox = QtGui.QMessageBox()
                MsgBox.setText(result['status'])
                MsgBox.exec_()
                self.FolderExploer.clear()
                for i, row in enumerate(result['result']):
                    self.FolderExploer.addItem(row['name'])

    def EnterClick(self):
        Target = self.FolderExploer.currentItem()
        Targettext = Target.text()
        TargetStr = str(Targettext)
        global CurrentPath
        CurrentPath += TargetStr + '/'
        result = interface.ls(CurrentPath)
        if result['status'] == 200:
            self.FolderExploer.clear()
            for i, row in enumerate(result['result']):
                self.FolderExploer.addItem(row['name'])

    def BackClick(self):
        global CurrentPath
        CurrentPath = CurrentPath[0:len(CurrentPath)-1]
        index = CurrentPath.rindex('/')
        CurrentPath = CurrentPath[0:index+1]
        result = interface.ls(CurrentPath)
        if result['status'] == 200:
            self.FolderExploer.clear()
            for i, row in enumerate(result['result']):
                self.FolderExploer.addItem(row['name'])


    def UploadClick(self):
        self.filedialog = QtGui.QFileDialog(self.centralwidget)
        LocalFilePath = QtGui.QFileDialog.getOpenFileName(self.filedialog, 'Open file', './root/Desktop')
        result = interface.up(LocalFilePath, CurrentPath)
        if result is not None:
            MsgBox = QtGui.QMessageBox()
            MsgBox.setText(result['status'])
            MsgBox.exec_()

    def DwonloadClick(self):
        Target = self.FolderExploer.currentItem()
        Targettext = Target.text()
        TargetStr = str(Targettext)
        RemotePath = CurrentPath + '/' + TargetStr
        result = interface.up(RemotePath, '/root/Desktop/')
        if result is not None:
            MsgBox = QtGui.QMessageBox()
            MsgBox.setText(result['status'])
            MsgBox.exec_()

    def RenameClick(self):
        Target = self.FolderExploer.currentItem()
        Targettext = Target.text()
        TargetStr = str(Targettext)
        RemotePath = CurrentPath + '/' + TargetStr
        self.dialog = QtGui.QInputDialog(self.centralwidget)
        NewName, ok = QtGui.QInputDialog.getText(self.dialog, "InputDialog", "Please input the name")
        if ok:
            result = interface.re(RemotePath, NewName)
            if result is not None:
                MsgBox = QtGui.QMessageBox()
                MsgBox.setText(result['status'])
                MsgBox.exec_()
                self.FolderExploer.clear()
                for i, row in enumerate(result['result']):
                    self.FolderExploer.addItem(row['name'])

    def RemoveClick(self):
        Target = self.FolderExploer.currentItem()
        Targettext = Target.text()
        TargetStr = str(Targettext)
        RemotePath = CurrentPath + '/' + TargetStr
        result = interface.rm(RemotePath)
        if result is not None:
            MsgBox = QtGui.QMessageBox()
            MsgBox.setText(result['status'])
            MsgBox.exec_()
            self.FolderExploer.clear()
            for i, row in enumerate(result['result']):
                self.FolderExploer.addItem(row['name'])


class Ui_SignUp(object):
    def setupUi(self, SignUp):
        SignUp.setObjectName(_fromUtf8("SignUp"))
        SignUp.resize(271, 271)
        self.centralwidget = QtGui.QWidget(SignUp)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.Signup = QtGui.QPushButton(self.centralwidget)
        self.Signup.setGeometry(QtCore.QRect(90, 200, 90, 28))
        self.Signup.setObjectName(_fromUtf8("Signup"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(50, 10, 81, 31))
        self.label.setObjectName(_fromUtf8("label"))
        self.Username = QtGui.QTextEdit(self.centralwidget)
        self.Username.setGeometry(QtCore.QRect(40, 40, 191, 31))
        self.Username.setObjectName(_fromUtf8("Username"))
        self.Password = QtGui.QTextEdit(self.centralwidget)
        self.Password.setGeometry(QtCore.QRect(40, 110, 191, 31))
        self.Password.setObjectName(_fromUtf8("Password"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(50, 80, 81, 31))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        SignUp.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(SignUp)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        SignUp.setStatusBar(self.statusbar)

        self.retranslateUi(SignUp)
        QtCore.QObject.connect(self.Signup, QtCore.SIGNAL(_fromUtf8("clicked()")), self.SignUpCheck)
        QtCore.QMetaObject.connectSlotsByName(SignUp)

    def retranslateUi(self, SignUp):
        SignUp.setWindowTitle(_translate("SignUp", "MainWindow", None))
        self.Signup.setText(_translate("SignUp", "Sign Up", None))
        self.label.setText(_translate("SignUp", "Username", None))
        self.label_2.setText(_translate("SignUp", "Password", None))

    def SignUpCheck(self):
        username = str(self.Username.toPlainText())
        password = str(self.Password.toPlainText())
        result = interface.login(username, password)
        MsgBox = QtGui.QMessageBox()
        MsgBox.setText(result)
        MsgBox.exec_()


class Ui_SignIn(object):
    def setupUi(self, SignIn):
        SignIn.setObjectName(_fromUtf8("SignIn"))
        SignIn.resize(271, 271)
        self.centralwidget = QtGui.QWidget(SignIn)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.Signup = QtGui.QPushButton(self.centralwidget)
        self.Signup.setGeometry(QtCore.QRect(90, 200, 90, 28))
        self.Signup.setObjectName(_fromUtf8("Signup"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(50, 10, 81, 31))
        self.label.setObjectName(_fromUtf8("label"))
        self.Username = QtGui.QTextEdit(self.centralwidget)
        self.Username.setGeometry(QtCore.QRect(40, 40, 191, 31))
        self.Username.setObjectName(_fromUtf8("Username"))
        self.Password = QtGui.QTextEdit(self.centralwidget)
        self.Password.setGeometry(QtCore.QRect(40, 110, 191, 31))
        self.Password.setObjectName(_fromUtf8("Password"))
        self.Signin = QtGui.QPushButton(self.centralwidget)
        self.Signin.setGeometry(QtCore.QRect(90, 160, 90, 28))
        self.Signin.setObjectName(_fromUtf8("Signin"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(50, 80, 81, 31))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        SignIn.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(SignIn)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        SignIn.setStatusBar(self.statusbar)
        self.signuppage = SignUp()

        self.retranslateUi(SignIn)
        QtCore.QObject.connect(self.Signin, QtCore.SIGNAL(_fromUtf8("clicked()")), self.SignInCheck)
        QtCore.QMetaObject.connectSlotsByName(SignIn)
        QtCore.QObject.connect(self.Signup, QtCore.SIGNAL(_fromUtf8("clicked()")), self.SignUpPage)
        QtCore.QMetaObject.connectSlotsByName(SignIn)

    def retranslateUi(self, SignIn):
        SignIn.setWindowTitle(_translate("SignIn", "MainWindow", None))
        self.Signup.setText(_translate("SignIn", "Sign Up", None))
        self.label.setText(_translate("SignIn", "Username", None))
        self.Signin.setText(_translate("SignIn", "Sign In", None))
        self.label_2.setText(_translate("SignIn", "Password", None))

    def SignInCheck(self):
        username = str(self.Username.toPlainText())
        password = str(self.Password.toPlainText())
        result = interface.login(username, password)
        if result['status'] == 200:
            global CurrentPath
            CurrentPath += str(username)
            CurrentPath += '/'
            MsgBox = QtGui.QMessageBox()
            MsgBox.setText("Succeed to sign in!")
            MsgBox.exec_()
            mainpage.show()
            signin.close()
        else:
            MsgBox = QtGui.QMessageBox()
            MsgBox.setText("Incorrect Username or Password!")
            MsgBox.exec_()

    def SignUpPage(self):
        self.signuppage.show()


class Ui_Input(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(272, 144)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(40, 10, 181, 31))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.Name = QtGui.QTextEdit(self.centralwidget)
        self.Name.setGeometry(QtCore.QRect(40, 40, 191, 31))
        self.Name.setObjectName(_fromUtf8("Name"))
        self.Ok = QtGui.QPushButton(self.centralwidget)
        self.Ok.setGeometry(QtCore.QRect(90, 80, 90, 28))
        self.Ok.setObjectName(_fromUtf8("Ok"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        QtCore.QObject.connect(self.Ok, QtCore.SIGNAL(_fromUtf8("clicked()")), self.Click)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.label_2.setText(_translate("MainWindow", "Input the name", None))
        self.Ok.setText(_translate("MainWindow", "Ok", None))

    def Click(self):
        NewName = self.Name.text()


class MainPage(QtGui.QMainWindow):

    def __init__(self,parent=None):

        QtGui.QWidget.__init__(self,parent)
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)


class SignIn(QtGui.QMainWindow):

    def __init__(self,parent=None):

        QtGui.QWidget.__init__(self,parent)
        self.ui=Ui_SignIn()
        self.ui.setupUi(self)


class SignUp(QtGui.QMainWindow):

    def __init__(self,parent=None):

        QtGui.QWidget.__init__(self,parent)
        self.ui=Ui_SignUp()
        self.ui.setupUi(self)


class Input(QtGui.QMainWindow):

    def __init__(self,parent=None):

        QtGui.QWidget.__init__(self,parent)
        self.ui=Ui_Input()
        self.ui.setupUi(self)


if __name__ == "__main__":

    import sys

    app = QtGui.QApplication(sys.argv)
    mainpage=MainPage()
    signin=SignIn()
    signin.show()
    app.exec_()