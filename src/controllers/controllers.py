from datetime import datetime
from re import L
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QBrush
from errors import *
from facade.command import *
from managers.AnalyzeManager import AnalyzerManager
from PyQt5.QtWidgets import QMessageBox

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
    
    def searchAcc(self):
        surname = self.UI.surnameEdit.text()
        if len(surname) == 0:
            self.createTable("%")
        else:
            self.createTable(surname + "%")
    
    def activateAcc(self):
        curRow = self.UI.playersTable.selectedItems()[0].row()
        id = self.UI.playersTable.item(curRow, 0).text()
        errorCode, _ = self.UI.Facade.execute(ChangeStatusAccCommand(), id, "Active")

        if errorCode == OK:
            self.UI.playersTable.removeRow(curRow)
    
    def blockAcc(self):
        curRow = self.UI.playersTable.selectedItems()[0].row()
        id = self.UI.playersTable.item(curRow, 0).text()
        errorCode, _ = self.UI.Facade.execute(ChangeStatusAccCommand(), id, "Blocked")

        if errorCode == OK:
            self.UI.playersTable.removeRow(curRow)

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
        self.UI.balanceLabel.setText(self.UI.balanceLabel.text() + str(round(balance, 2)) + " у.е")

        self.UI.exitButton.clicked.connect(lambda: self.exitToMain())
        self.UI.betButton.clicked.connect(lambda: self.UI.BetUI())
        self.UI.moneyButton.clicked.connect(lambda: self.UI.donateUI())
        self.UI.historyButton.clicked.connect(lambda: self.UI.checkHistoryUI())
    
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
            elif role == "Admin":
                self.UI.ManagerMainUI()
            elif role == "Analyzer":
                self.UI.statMainUI()

class RegistrateUIController(BaseController):

    def __init__(self, UI) -> None:
        super().__init__(UI)
    
    def execute(self):
        self.UI.goButton.clicked.connect(lambda: self.tryToRegistrate())
        self.UI.exitButton.clicked.connect(lambda: self.UI.FirstMenuUI())

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
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        if (errorCode == OK):
            msgBox.setWindowTitle("Успех!")
            msgBox.setText("Регистрация прошла успешно!")
            msgBox.exec()
            self.UI.FirstMenuUI()
        else:
            msgBox.setWindowTitle("Ошибка!")

            if (errorCode == BAD_SURNAME):
                msgBox.setText("Фамилия не должна быть пустой")
            elif (errorCode == BAD_NAME):
                msgBox.setText("Имя не должно быть пустым")
            elif (errorCode == BAD_EMAIL):
                msgBox.setText("Электронная почта введена неправильно!")
            elif (errorCode == BAD_PASSPORT):
                msgBox.setText("Вы неправильно ввели свой паспорт! \n Серия и номер должны быть написаны слитно")
            elif (errorCode == BAD_TELEPHONE):
                msgBox.setText("Вы неправильно ввели свой номер телефона!")
            elif (errorCode == BAD_LOGIN):
                msgBox.setText("Длина логина должна быть не меньше 6 символов")
            elif (errorCode == BAD_PASSWORD):
                msgBox.setText("Длина пароля должна быть не меньше 6 символов")
            elif (errorCode == LOGIN_IS_OCCUPED):
                msgBox.setText("К сожалению, логин уже занят. Выберите другой.")
            
            msgBox.exec()

class MainManagerUIController(BaseController):
    def __init__(self, UI) -> None:
        super().__init__(UI)
    
    def execute(self):
        self.UI.verificateButton.clicked.connect(lambda: self.UI.verifyMenuUI())
        self.UI.exitButton.clicked.connect(lambda: self.UI.FirstMenuUI())
        self.UI.bunButton.clicked.connect(lambda: self.UI.bunPlayersUI())

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
        self.UI.dateEdit.setDateTime(QtCore.QDateTime.currentDateTime())
        self.UI.timeEdit.setDateTime(QtCore.QDateTime.currentDateTime())
        self.UI.teamTable.setColumnWidth(0, 70)
        self.UI.teamTable.setColumnWidth(1, 450)
        self.UI.teamTable.setColumnWidth(2, 330)
        
        self.UI.addButton.clicked.connect(lambda: self.addMatch())
        self.createTable('%')
        self.UI.teamTable.clicked.connect(lambda: self.addTeam())
        self.UI.searchButton.clicked.connect(lambda: self.searchAcc())
        self.UI.exitButton.clicked.connect(lambda: self.UI.statMainUI())
    
    def createTable(self, teamName):
        errorCode, teams = self.UI.Facade.execute(ViewTeamsCommand(), teamName)

        if errorCode == OK:
            N = len(teams)
            self.UI.teamTable.setRowCount(N)
            for i, el in enumerate(teams):
                self.UI.teamTable.setItem(i, 0, QtWidgets.QTableWidgetItem(str(el[0])))
                self.UI.teamTable.setItem(i, 1, QtWidgets.QTableWidgetItem(str(el[1])))
                self.UI.teamTable.setItem(i, 2, QtWidgets.QTableWidgetItem(str(el[2])))
    
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
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Critical)
            msgBox.setWindowTitle("Возникли проблемы")
            if errorCode == BAD_TEAMS:
                msgBox.setText("Выбранные команды не должны совпадать!")
            elif errorCode == BAD_TIME:
                msgBox.setText("Матч нельзя назначить на раньше, чем сейчас!")
            elif errorCode == BAD_COEFS:
                msgBox.setText("Сумма вероятностей не равна 100%!")
            msgBox.exec()

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

        self.UI.p1Spin.setValue(round(p1, 2))
        self.UI.xSpin.setValue(round(x, 2))
        self.UI.p2Spin.setValue(round(p2, 2))

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
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Critical)
            msgBox.setWindowTitle("Возникли проблемы")
            msgBox.setText("Матч ещё не начался!")
            msgBox.exec()

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
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Critical)
            msgBox.setWindowTitle("Возникли проблемы")
            msgBox.setText("Сумма вероятностей не равна 100%!")
            msgBox.exec()

class betUIController(BaseController):

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

        self.UI.searchButton.clicked.connect(lambda: self.searchByTeam())
        self.UI.backButton.clicked.connect(lambda: self.UI.MainMenuUI())
        self.UI.updateButton.clicked.connect(lambda: self.UI.BetUI())
        self.UI.betButton.clicked.connect(lambda: self.makeBet())

        self.UI.gameTable.clicked.connect(lambda: self.updateBetCoef())
        self.UI.p1Radio.clicked.connect(lambda: self.updateBetCoef())
        self.UI.xRadio.clicked.connect(lambda: self.updateBetCoef())
        self.UI.p2Radio.clicked.connect(lambda: self.updateBetCoef())

        balance, maxbet = self.UI.Facade.execute(GetUserBetInfoCommand())   

        self.UI.balanceLabel.setText("Ваш баланс: " + str(round(balance, 2)))
        self.UI.maxBetLabel.setText("Максимальная ставка: " + str(maxbet))
        self.UI.sumBox.setMaximum(maxbet)

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
        
    def searchByTeam(self):
        teamName = self.UI.searchEdit.text()
        if len(teamName) == 0:
            self.createTable("%")
        else:
            self.createTable("%" + teamName + "%")
    
    def updateBetCoef(self):
        try:
            curRow = self.UI.gameTable.selectedItems()[0].row()
            
            if self.UI.p1Radio.isChecked():
                k = self.UI.gameTable.item(curRow, 6).text()
            elif self.UI.xRadio.isChecked():
                k = self.UI.gameTable.item(curRow, 7).text()
            elif self.UI.p2Radio.isChecked():
                k = self.UI.gameTable.item(curRow, 8).text()
            else:
                k = ""
            self.UI.cfLabel.setText("Коэффициент: " + k)
        except:
            pass
    
    def makeBet(self):
        try:
            curRow = self.UI.gameTable.selectedItems()[0].row()
            id = int(self.UI.gameTable.item(curRow, 0).text())
            size = float(self.UI.sumBox.value())

            if self.UI.p1Radio.isChecked():
                k = float(self.UI.gameTable.item(curRow, 6).text())
                betPredict = 1

            elif self.UI.xRadio.isChecked():
                k = float(self.UI.gameTable.item(curRow, 7).text())
                betPredict = 0

            elif self.UI.p2Radio.isChecked():
                k = float(self.UI.gameTable.item(curRow, 8).text())
                betPredict = 2
            else:
                return
            
            msgBox = QMessageBox()

            errorCode, _ = self.UI.Facade.execute(MakeBetCommand(), id, betPredict, size, k)
            if errorCode == OK:
                errorCode = self.UI.Facade.execute(UpdateUserConnectionInfoCommand())
                
            if errorCode == OK:
                msgBox.setIcon(QMessageBox.Information)
                msgBox.setWindowTitle("Успех!")
                msgBox.setText("Ставка прошла успешно!")
                msgBox.exec()
                self.UI.BetUI()
            else:
                msgBox.setIcon(QMessageBox.Critical)
                msgBox.setWindowTitle("Что-то пошло не так")
                msgBox.setText("Возникла ошибка при совершении ставки. \nВозможно, вам не хватает средств")
                msgBox.exec()
        
        except Exception as e:
            print(e)

class DonateController(BaseController):
    def __init__(self, UI) -> None:
        super().__init__(UI)
    
    def execute(self):
        self.UI.donateButton.clicked.connect(lambda: self.donate())
        self.UI.exitButton.clicked.connect(lambda: self.UI.MainMenuUI())
    
    def donate(self):
        value = float(self.UI.sumBox.value())
        errorCode, _ = self.UI.Facade.execute(DonateCommand(), value)

        msgBox = QMessageBox()

        if errorCode == OK:
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setWindowTitle("Успех!")
            msgBox.setText("Баланс успешно пополнен!")
            msgBox.exec()
            self.UI.MainMenuUI()
        else:
            msgBox.setIcon(QMessageBox.Critical)
            msgBox.setWindowTitle("Что-то пошло не так")
            msgBox.setText("Возникла ошибка при совершении ставки. \nВозможно, вам не хватает средств")
            msgBox.exec()

class CheckHistoryController(BaseController):
    def __init__(self, UI) -> None:
        super().__init__(UI)
    
    def execute(self):
        self.UI.updateButton.clicked.connect(lambda: self.execute())
        self.UI.backButton.clicked.connect(lambda: self.UI.MainMenuUI())
        
        self.UI.gameTable.setColumnWidth(0, 10)
        self.UI.gameTable.setColumnWidth(1, 220)
        self.UI.gameTable.setColumnWidth(2, 400)
        self.UI.gameTable.setColumnWidth(3, 400)
        self.UI.gameTable.setColumnWidth(4, 95)
        self.UI.gameTable.setColumnWidth(5, 160)
        self.UI.gameTable.setColumnWidth(6, 105)
        self.UI.gameTable.setColumnWidth(7, 130)
        self.UI.gameTable.setColumnWidth(8, 120)

        self.createTable()

    def createTable(self):
        errorCode, games = self.UI.Facade.execute(CheckHistoryCommand())
        if errorCode == OK:
            N = len(games)
            self.UI.gameTable.setRowCount(N)
            for i, el in enumerate(games):
                self.UI.gameTable.setItem(i, 0, QtWidgets.QTableWidgetItem(str(el[0])))
                date, time = str(el[1]).split(' ')
                betDateTime = date + " " * 5 + time[:5]
                self.UI.gameTable.setItem(i, 1, QtWidgets.QTableWidgetItem(betDateTime))
                self.UI.gameTable.setItem(i, 2, QtWidgets.QTableWidgetItem(str(el[2])))               
                self.UI.gameTable.setItem(i, 3, QtWidgets.QTableWidgetItem(str(el[3])))
                choosedResult = el[4]
                if choosedResult == 1:
                    choosedResult = 'П1'
                elif choosedResult == 2:
                    choosedResult = 'П2'
                elif choosedResult == 0:
                    choosedResult = 'Х'     
                self.UI.gameTable.setItem(i, 4, QtWidgets.QTableWidgetItem(choosedResult))
                self.UI.gameTable.setItem(i, 5, QtWidgets.QTableWidgetItem(str(round(el[5], 2))))
                self.UI.gameTable.setItem(i, 6, QtWidgets.QTableWidgetItem(str(el[6])))
                result = el[7]
                if result == 0:
                    color = QColor(0, 0, 0)
                    result = "Принята"
                elif result == 1:
                    color = QColor(0, 255, 0)
                    result = "Выиграна"
                elif result == -1:
                    color = QColor(255, 0, 0)
                    result = "Проиграна"
                self.UI.gameTable.setItem(i, 7, QtWidgets.QTableWidgetItem(result))
                self.UI.gameTable.item(i, 7).setForeground(QBrush(color))
                self.UI.gameTable.setItem(i, 8, QtWidgets.QTableWidgetItem(str(round(el[8], 2))))

class BunController(BaseController):
    def __init__(self, UI) -> None:
        super().__init__(UI)
    
    def execute(self):
        self.UI.blockButton.clicked.connect(lambda: self.bun())
        self.UI.exitButton.clicked.connect(lambda: self.UI.ManagerMainUI())
        
        self.UI.playerTable.setColumnWidth(0, 10)
        self.UI.playerTable.setColumnWidth(1, 200)
        self.UI.playerTable.setColumnWidth(2, 483)
        self.UI.playerTable.setColumnWidth(3, 150)
        self.UI.playerTable.setColumnWidth(4, 150)

        self.createTable()
    
    def createTable(self):
        errorCode, players = self.UI.Facade.execute(GetAllActiveAccsCommand())
        if errorCode == OK:
            N = len(players)
            self.UI.playerTable.setRowCount(N)
            for i, el in enumerate(players):
                self.UI.playerTable.setItem(i, 0, QtWidgets.QTableWidgetItem(str(el[0])))
                self.UI.playerTable.setItem(i, 1, QtWidgets.QTableWidgetItem(str(el[1])))
                self.UI.playerTable.setItem(i, 2, QtWidgets.QTableWidgetItem(str(el[2]) + " " + str(el[3])))               
                self.UI.playerTable.setItem(i, 3, QtWidgets.QTableWidgetItem(str(el[4])))
                self.UI.playerTable.setItem(i, 4, QtWidgets.QTableWidgetItem(str(el[5])))
    
    def bun(self):
        curRow = self.UI.playerTable.selectedItems()[0].row()
        id = self.UI.playerTable.item(curRow, 0).text()
        self.UI.Facade.execute(ChangeStatusAccCommand(), id, "Blocked")

        self.execute()