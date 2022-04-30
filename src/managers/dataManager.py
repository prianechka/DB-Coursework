from datetime import date
from ftplib import error_perm
from http.client import OK
from os import stat

from matplotlib import use
from BaseManager import BaseManager
import psycopg2
import sys
sys.path.append("/home/prianechka/Education/BMSTU/DB-CourseWork/src/DataBase/")
from errors import *
from datetime import date

class DataManager(BaseManager):
    def __init__(self):
        self.connection = psycopg2.connect(user="bob", password="admin", host="localhost", port="5432", database="course")
        self.cur = self.connection.cursor()
    
    def execute(self, executeString):
        errorCode = OK
        result = []
        try:
            self.cur.execute(executeString)
        except:
            errorCode = DATABASE_ERROR
            self.connection.rollback()
        else:
            self.connection.commit()
        
        try:
            result = self.cur.fetchall()
        except:
            pass
        
        return errorCode, result
    
    def executeProc(self, executeString):
        errorCode = OK
        result = []
        try:
            self.cur.execute(executeString)
            result = self.cur.fetchall()
        except:
            errorCode = DATABASE_ERROR
            self.connection.rollback()
        else:
            self.connection.commit()
        return errorCode, result

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
        executeString1 = f"CALL BK.registrate('{login}', '{password}', '{name}','{surname}', '{dateOfBirth}', '{telephone}', '{passport}', '{email}');"

        errorCode, _ = self.execute(executeString1)

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
    
    def findVerifyAccs(self, surnameString):
        executeString = (f"SELECT * FROM BK.verifyAccs('{surnameString}');")

        return self.execute(executeString)
    
    def changeStateAcc(self, id, status):
        executeString = f"CALL BK.updateStatus({id}, '{status}')"
        
        return self.execute(executeString)
    
    def viewTeams(self, teamName):
        executeString = f"SELECT * FROM BK.viewTeams('{teamName}')"

        return self.execute(executeString)
    
    def addGame(self, id1Team, id2Team, p1, p2, p3, dateMatch, timeMatch):
        executeString = f"CALL BK.addGame({id1Team}, {id2Team}, {p1}, {p2}, {p3}, '{dateMatch}', '{timeMatch}')"

        return self.execute(executeString)