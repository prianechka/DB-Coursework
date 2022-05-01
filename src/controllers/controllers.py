from re import S
from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QBrush
from errors import *
from facade.command import *
from managers.AnalyzeManager import AnalyzerManager

class BaseController():
    def __init__(self, UI) -> None:
        self.UI = UI

    def execute(self):
        pass

class VerifyUIController(BaseController):

    def __init__(self, UI) -> None:
        self.UI = UI

    def execute(self):
        self.UI.playersTable.setColumnWidth(0, 70)
        self.UI.playersTable.setColumnWidth(1, 400)
        self.UI.playersTable.setColumnWidth(2, 210)
        self.UI.playersTable.setColumnWidth(3, 210)
        self.UI.playersTable.setColumnWidth(4, 340)
        
        self.UI.activateButton.clicked.connect(lambda: self.activateAcc())
        self.UI.blockButton.clicked.connect(lambda: self.blockAcc())
        self.UI.cancelButton.clicked.connect(lambda: self.UI.ManagerMainUI())
        self.UI.searchButton.clicked.connect(lambda: self.searchAcc())

        self.createTable("%")
    
    def createTable(self, string):
        errorCode, verifyAccs = self.UI.Facade.execute(FindVerifyCommand(), string)

        if errorCode == OK:
            N = len(verifyAccs)
            self.UI.playersTable.setRowCount(N)
            for i, el in enumerate(verifyAccs):
                self.UI.playersTable.setItem(i, 0, QtWidgets.QTableWidgetItem(str(el[0])))
                self.UI.playersTable.setItem(i, 1, QtWidgets.QTableWidgetItem(str(el[1] + " " + el[2])))
                self.UI.playersTable.setItem(i, 2, QtWidgets.QTableWidgetItem(str(el[3])))
                self.UI.playersTable.setItem(i, 3, QtWidgets.QTableWidgetItem(str(el[4])))
                self.UI.playersTable.setItem(i, 4, QtWidgets.QTableWidgetItem(str(el[5])))
        else:
            print(errorCode)
    
    def searchAcc(self):
        surname = self.UI.surnameEdit.text()
        if len(surname) == 0:
            self.createTable("%")
        else:
            self.createTable(surname + "%")
    
    def activateAcc(self):
        curRow = self.UI.playersTable.selectedItems()[0].row()
        id = self.UI.playersTable.item(curRow, 0).text()
        errorCode = self.UI.Facade.execute(ChangeStatusAccCommand(), id, "Active")

        if errorCode == OK:
            self.UI.playersTable.removeRow(curRow)
        else:
            print(errorCode)
    
    def blockAcc(self):
        curRow = self.UI.playersTable.selectedItems()[0].row()
        id = self.UI.playersTable.item(curRow, 0).text()
        errorCode = self.UI.Facade.execute(ChangeStatusAccCommand(), id, "Blocked")

        if errorCode == OK:
            self.UI.playersTable.removeRow(curRow)
        else:
            print(errorCode, id)

class MainMenuUIController(BaseController):
    def __init__(self, UI) -> None:
        super().__init__(UI)
    
    def execute(self):
        login = self.UI.Facade.execute(LoginCommand())
        status, balance = self.UI.Facade.execute(UserDataCommand())
        if status == 'On Verify':
            self.UI.betButton.setEnabled(False)
            status = 'На верификации'
        elif status == 'Active':
            status = "Активен"
        elif status == 'Blocked':
            self.UI.betButton.setEnabled(False)
            self.UI.moneyButton.setEnabled(False)
            status = 'Заблокирован'
        self.UI.welcomeLabel.setText(self.UI.welcomeLabel.text() + login + "!")
        self.UI.statusLabel.setText(self.UI.statusLabel.text() + status)
        self.UI.balanceLabel.setText(self.UI.balanceLabel.text() + str(balance) + " у.е")

        self.UI.exitButton.clicked.connect(lambda: self.exitToMain())
    
    def exitToMain(self):
        self.UI.Facade.execute(CleanCommand())
        self.UI.FirstMenuUI()

class FirstMenuUIController(BaseController):
    def __init__(self, UI) -> None:
        super().__init__(UI)
    
    def execute(self):
        self.UI.InputButton.clicked.connect(lambda: self.tryToAuthorize())
        self.UI.RegistrateButton.clicked.connect(lambda: self.UI.RegistrateUI())
    
    def tryToAuthorize(self):
        login = self.UI.loginEdit.text()
        password = self.UI.passwordEdit.text()

        errorCode, role = self.UI.Facade.execute(AuthorizeCommand(), login, password)
        if (errorCode == OK):
            if role == "Player":
                self.UI.MainMenuUI()
            elif role == "Manager":
                self.UI.ManagerMainUI()
            elif role == "Analyzer":
                self.UI.statMainUI()

class RegistrateUIController(BaseController):

    def __init__(self, UI) -> None:
        super().__init__(UI)
    
    def execute(self):
        self.UI.goButton.clicked.connect(lambda: self.tryToRegistrate())

    def tryToRegistrate(self):
        surname = self.UI.surnameEdit.text()
        name = self.UI.nameEdit.text()
        dateBirth = self.UI.dateEdit.date().toString(Qt.ISODate).replace('-', '.')
        email = self.UI.emailEdit.text()
        passport = self.UI.passportEdit.text()
        telephone = self.UI.telephoneEdit.text()
        login = self.UI.loginEdit.text()
        password = self.UI.passwordEdit.text()
        errorCode = self.UI.Facade.execute(RegistrateCommand(), surname, name, dateBirth, email, passport, telephone, login, password)
        if (errorCode == OK):
            self.UI.FirstMenuUI()

class MainManagerUIController(BaseController):
    def __init__(self, UI) -> None:
        super().__init__(UI)
    
    def execute(self):
        self.UI.verificateButton.clicked.connect(lambda: self.UI.verifyMenuUI())
        self.UI.exitButton.clicked.connect(lambda: self.UI.FirstMenuUI())

class StatMainUIController(BaseController):
    def __init__(self, UI) -> None:
        super().__init__(UI)
    
    def execute(self):
        self.UI.exitButton.clicked.connect(lambda: self.UI.FirstMenuUI())
        self.UI.addMatchButton.clicked.connect(lambda: self.UI.addMatchUI())
        self.UI.checkLineButton.clicked.connect(lambda: self.UI.checkLineUI())

class AddMatchUIController(BaseController):
    def __init__(self, UI) -> None:
        super().__init__(UI)
        self.curTeam = 0
    
    def execute(self):
        self.UI.teamTable.setColumnWidth(0, 70)
        self.UI.teamTable.setColumnWidth(1, 450)
        self.UI.teamTable.setColumnWidth(2, 330)
        
        self.UI.addButton.clicked.connect(lambda: self.addMatch())
        self.createTable('%')
        self.UI.teamTable.clicked.connect(lambda: self.addTeam())
        self.UI.searchButton.clicked.connect(lambda: self.searchAcc())
    
    def createTable(self, teamName):
        errorCode, teams = self.UI.Facade.execute(ViewTeamsCommand(), teamName)

        if errorCode == OK:
            N = len(teams)
            self.UI.teamTable.setRowCount(N)
            for i, el in enumerate(teams):
                self.UI.teamTable.setItem(i, 0, QtWidgets.QTableWidgetItem(str(el[0])))
                self.UI.teamTable.setItem(i, 1, QtWidgets.QTableWidgetItem(str(el[1])))
                self.UI.teamTable.setItem(i, 2, QtWidgets.QTableWidgetItem(str(el[2])))
        else:
            print(errorCode)
    
    def addTeam(self):
        curRow = self.UI.teamTable.selectedItems()[0].row()
        id = self.UI.teamTable.item(curRow, 0).text()
        if self.curTeam == 0:
            self.UI.id1Team.setValue(int(id))
            self.curTeam += 1
        else:
            self.UI.id2Team.setValue(int(id))
            self.curTeam -= 1

    def searchAcc(self):
        teamName = self.UI.searchEdit.text()
        if len(teamName) == 0:
            self.createTable("%")
        else:
            self.createTable("%" + teamName + "%")

    def addMatch(self):
        id1Team = self.UI.id1Team.value()
        id2Team = self.UI.id2Team.value()

        p1 = self.UI.p1SpinBox.value()
        p2 = self.UI.p2SpinBox.value()
        p3 = self.UI.p3SpinBox.value()

        dateMatch = self.UI.dateEdit.date().toString(Qt.ISODate).replace('-', '.')
        timeMatch = self.UI.timeEdit.time().toString("hh:mm")

        errorCode, _ = self.UI.Facade.execute(AddGameCommand(), id1Team, id2Team, p1, p2, p3, dateMatch, timeMatch)
        if errorCode == OK:
            self.UI.statMainUI()
        else:
            print(errorCode)

class LineAnaliticUIController(BaseController):
    
    def __init__(self, UI) -> None:
        super().__init__(UI)
    
    def execute(self):
        self.UI.gameTable.setColumnWidth(0, 20)
        self.UI.gameTable.setColumnWidth(1, 230)
        self.UI.gameTable.setColumnWidth(2, 400)
        self.UI.gameTable.setColumnWidth(3, 400)
        self.UI.gameTable.setColumnWidth(4, 120)
        self.UI.gameTable.setColumnWidth(5, 120)
        self.UI.gameTable.setColumnWidth(6, 100)
        self.UI.gameTable.setColumnWidth(7, 100)
        self.UI.gameTable.setColumnWidth(8, 105)

        self.createTable('%')

        self.UI.changeStatusButton.clicked.connect(lambda: self.changeStatus())
        self.UI.firstGoalButton.clicked.connect(lambda: self.addGoal(1))
        self.UI.secondGoalButton.clicked.connect(lambda: self.addGoal(2))
        self.UI.searchButton.clicked.connect(lambda: self.searchByTeam())
        self.UI.gameTable.clicked.connect(lambda: self.readCoefs())
        self.UI.exitButton.clicked.connect(lambda: self.UI.statMainUI())
        self.UI.coefButton.clicked.connect(lambda: self.editCoefs())
    
    def readCoefs(self):
        curRow = self.UI.gameTable.selectedItems()[0].row()
        p1 = float(self.UI.gameTable.item(curRow, 6).text())
        x = float(self.UI.gameTable.item(curRow, 7).text())
        p2 = float(self.UI.gameTable.item(curRow, 8).text())

        p1, x, p2 = self.UI.Facade.execute(FindProbs(), p1, x, p2)

        self.UI.p1Spin.setValue(p1)
        self.UI.xSpin.setValue(x)
        self.UI.p2Spin.setValue(p2)

    def createTable(self, teamName):
        errorCode, games = self.UI.Facade.execute(ViewGamesAnalyze(), teamName)
        if errorCode == OK:
            N = len(games)
            self.UI.gameTable.setRowCount(N)
            for i, el in enumerate(games):
                self.UI.gameTable.setItem(i, 0, QtWidgets.QTableWidgetItem(str(el[0])))
                self.UI.gameTable.setItem(i, 1, QtWidgets.QTableWidgetItem(str(el[1]) + " " + str(el[2])))
                self.UI.gameTable.setItem(i, 2, QtWidgets.QTableWidgetItem(str(el[3])))               
                self.UI.gameTable.setItem(i, 3, QtWidgets.QTableWidgetItem(str(el[4])))
                status = str(el[5])     
                self.UI.gameTable.setItem(i, 4, QtWidgets.QTableWidgetItem(status))
                if status == "Live":
                    self.UI.gameTable.item(i, 4).setForeground(QBrush(QColor(255, 0, 0)))
                self.UI.gameTable.setItem(i, 5, QtWidgets.QTableWidgetItem(str(el[6])))
                self.UI.gameTable.setItem(i, 6, QtWidgets.QTableWidgetItem(str(round(el[7], 2))))
                self.UI.gameTable.setItem(i, 7, QtWidgets.QTableWidgetItem(str(round(el[8], 2))))
                self.UI.gameTable.setItem(i, 8, QtWidgets.QTableWidgetItem(str(round(el[9], 2))))
        else:
            print(errorCode)

    def changeStatus(self):
        curRow = self.UI.gameTable.selectedItems()[0].row()
        curStatus = self.UI.gameTable.item(curRow, 4).text()
        id = self.UI.gameTable.item(curRow, 0).text()


        errorCode, _ = self.UI.Facade.execute(ChangeGameStatus(), int(id))
        if (errorCode == OK):
            if (curStatus == 'Plain'):
                self.UI.gameTable.item(curRow, 4).setForeground(QBrush(QColor(255, 0, 0)))
                self.UI.gameTable.item(curRow, 4).setText("Live")
            elif (curStatus == 'Live'):
                self.UI.gameTable.removeRow(curRow)

    def addGoal(self, team):
        curRow = self.UI.gameTable.selectedItems()[0].row()
        curResult = self.UI.gameTable.item(curRow, 5).text()
        id = self.UI.gameTable.item(curRow, 0).text()
        curStatus = self.UI.gameTable.item(curRow, 4).text()

        if curStatus == 'Live':
            tmpIndex = curResult.find(':')

            if team == 1:
                curResult = str(int(curResult[:tmpIndex]) + 1) + curResult[tmpIndex:]
            elif team == 2:
                curResult = curResult[:tmpIndex] + ":" + str(int(curResult[tmpIndex + 1:]) + 1)
            
            self.UI.Facade.execute(ChangeGameResult(), int(id), curResult)

            self.UI.gameTable.item(curRow, 5).setText(curResult)
        else:
            print("Матч ещё не начался :(")

    def searchByTeam(self):
        teamName = self.UI.searchEdit.text()
        if len(teamName) == 0:
            self.createTable("%")
        else:
            self.createTable("%" + teamName + "%")
    
    def editCoefs(self):
        curRow = self.UI.gameTable.selectedItems()[0].row()
        id = self.UI.gameTable.item(curRow, 0).text()

        p1 = self.UI.p1Spin.value()
        x = self.UI.xSpin.value()
        p2 = self.UI.p2Spin.value()

        errorCode, _ = self.UI.Facade.execute(EditCoefCommand(), id, p1, x, p2)
        if errorCode == OK:
            self.UI.checkLineUI()
        else:
            print(errorCode)
