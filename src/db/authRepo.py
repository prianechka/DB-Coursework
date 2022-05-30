from db.baseRepo import BaseRepo
import sys
sys.path.append("/home/prianechka/Education/BMSTU/DB-CourseWork/DB-Coursework/src/")
from errors import *

class AuthRepo(BaseRepo):
    def __init__(self):
        super().__init__()
        self.cur = self.connection.cursor()
        self.execute('SET ROLE bob;')

    def tryToAuthorize(self, login, password):
        errorCode = 0
        resultRole = ""
        resultLogin = ""
        executeString = f"SELECT * FROM BK.auth('{login}', '{password}');"
        errorCode, result = self.execute(executeString)

        if errorCode == OK:
            if (len(result) == 0):
                errorCode = USER_NOT_FOUND
            else:
                resultRole = result[0][2]
                resultLogin = result[0][0]
        return errorCode, resultRole, resultLogin
    
    def findLogins(self, login):
        executeString = f"SELECT * FROM BK.findLogin('{login}');"
        errorCode, result = self.execute(executeString)

        if errorCode == OK:
            if (len(result) != 0):
                errorCode = LOGIN_IS_OCCUPED
        return errorCode
            
    def makeRegistrate(self, surname, name, dateOfBirth, email, passport, telephone, login, password):
        executeString = f"CALL BK.registrate('{login}', '{password}', '{name}','{surname}', '{dateOfBirth}', '{telephone}', '{passport}', '{email}');"

        errorCode, _ = self.execute(executeString)

        return errorCode