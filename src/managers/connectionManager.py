from BaseManager import BaseManager
from dataManager import DataManager
from validateManager import ValidateRegistrateManager, ValidateGameManager
from sessionHolder import SessionHolder
from AnalyzeManager import AnalyzerManager
import sys
sys.path.append("/home/prianechka/Education/BMSTU/DB-CourseWork/src/DataBase/")
from errors import *

class ConnectionManager(BaseManager):
    def __init__(self):
        self.holder = SessionHolder()
    
    def TryToAuthorize(self, login, password):
        errorCode, role, login = DataManager().tryToAuthorize(login, password)
        if errorCode == OK:
            self.holder.setRole(role)
            self.holder.setUserLogin(login)
            if role == "Player":
                self.UpdateUserConnectInfo(login)
        return errorCode, role
    
    def TryToRegistrate(self, surname, name, dateOfBirth, email, passport, telephone, login, password):
        errorCode = ValidateRegistrateManager().validate(surname, name, email, passport, telephone, login, password)
        if (errorCode == OK):
            errorCode = DataManager().findLogins(login)
            if (errorCode == OK):
                errorCode = DataManager().makeRegistrate(surname, name, dateOfBirth, email, passport, telephone, login, password)
        return errorCode

    def GetLogin(self):
        return self.holder.getUserLogin()
    
    def GetRole(self):
        return self.holder.getRole()
    
    def GetBaseUserInfo(self):
        return self.holder.getUserStatus(), self.holder.getUserBalance()
    
    def UpdateUserConnectInfo(self, login):
        errorCode, webUserID, accountID, userStatus, balance, maxBet = DataManager().getUserInfo(login)
        if errorCode == OK:
            self.holder.setUserWebID(webUserID)
            self.holder.setUserAccID(accountID)
            self.holder.setUserStatus(userStatus)
            self.holder.setUserBalance(balance)
            self.holder.setUserMaxBet(maxBet)
    
    def foldUserInfo(self):
        self.holder.foldSessionInfo()
    
    def findVerifyAccs(self, surnameString):
        return DataManager().findVerifyAccs(surnameString)
    
    def changeStateAcc(self, id, status):
        return DataManager().changeStateAcc(id, status)
    
    def viewTeams(self, teamName):
        return DataManager().viewTeams(teamName)
    
    def addGame(self, id1Team, id2Team, p1, p2, p3, dateMatch, timeMatch):
        errorCode = ValidateGameManager().validate(id1Team, id2Team, p1, p2, p3, dateMatch, timeMatch)

        if errorCode == OK:
            p1, p2, p3 = AnalyzerManager().createCoefs(p1, p2, p3)
            return DataManager().addGame(id1Team, id2Team, p1, p2, p3, dateMatch, timeMatch)