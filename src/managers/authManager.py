from managers.BaseManager import BaseManager
from db.authRepo import AuthRepo
from managers.validate.validateManager import ValidateRegistrateManager
from managers.player.sessionHolder import SessionHolder
from managers.player.playerManager import PlayerManager
import sys
sys.path.append("/home/prianechka/Education/BMSTU/DB-CourseWork/DB-Coursework/src/")
from errors import *

class AuthManager(BaseManager):
    def __init__(self):
        self.holder = SessionHolder()
        self.repo = AuthRepo()
    
    def TryToAuthorize(self, login, password):
        errorCode, role, login = self.repo.tryToAuthorize(login, password)
        if errorCode == OK:
            self.holder.setRole(role)
            self.holder.setUserLogin(login)
            if role == "Player":
                PlayerManager().UpdateUserConnectInfo(login)
        return errorCode, role
    
    def TryToRegistrate(self, surname, name, dateOfBirth, email, passport, telephone, login, password):
        errorCode = ValidateRegistrateManager().validate(surname, name, email, passport, telephone, login, password)
        if (errorCode == OK):
            errorCode = self.repo.findLogins(login)
            if (errorCode == OK):
                errorCode = self.repo.makeRegistrate(surname, name, dateOfBirth, email, passport, telephone, login, password)
        return errorCode
    
    def getUserInfo(self, webUserLogin):
        webUserID = -1
        accountID = -1
        userStatus = ""
        balance = -1
        maxBet = -1
        errorCode = OK
        executeString = f"SELECT * FROM BK.getUserInfo('{webUserLogin}');"

        errorCode, result = self.execute(executeString)
        if errorCode == OK:
            if (len(result) == 0):
                errorCode = USER_NOT_FOUND
            else:
                webUserID = result[0][0]
                accountID = result[0][1]
                userStatus = result[0][2]
                balance = result[0][3]
                maxBet = result[0][4]

        return errorCode, webUserID, accountID, userStatus, balance, maxBet