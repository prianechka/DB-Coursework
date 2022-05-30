from BaseManager import BaseManager
import sys
import numpy as np
import datetime as dt
sys.path.append("/home/prianechka/Education/BMSTU/DB-CourseWork/src/DataBase/")
from errors import *

EPS = 0.0001

class BaseValidateManager(BaseManager):
    def __init__(self):
        super().__init__()
    
    def validate(self, *args):
        pass

class ValidateGameManager(BaseValidateManager):
    def __init__(self):
        super().__init__()
    
    def validate(self, id1Team, id2Team, p1, p2, p3, dateMatch, timeMatch):
        errorCode = self.__checkCoeff(p1, p2, p3)
        if errorCode == OK:
            errorCode = self.__checkDateTime(dateMatch, timeMatch)
            if errorCode == OK:
                errorCode = self.__checkTeams(id1Team, id2Team)
        return errorCode
    
    def __checkCoeff(self, p1, p2, p3):
        if np.abs(np.sum([p1, p2, p3]) - 100) < EPS:
            return OK
        else:
            return BAD_COEFS
    
    def __checkTeams(self, id1Team, id2Team):
        if id1Team == id2Team:
            return BAD_TEAMS
        else:
            return OK
    
    def __checkDateTime(self, dateMatch, timeMatch):
        day = int(dateMatch[8:])
        month = int(dateMatch[5:7])
        year = int(dateMatch[:4])

        hour = int(timeMatch[:2])
        minutes = int(timeMatch[3:])

        today = dt.datetime.now()
        matchDateTime = dt.datetime(year, month, day, hour, minutes)

        delta = matchDateTime - today
        if (delta > dt.timedelta(0, 30, 0)):
            return OK
        else:
            return BAD_TIME

class ValidateRegistrateManager(BaseValidateManager):

    def __init__(self):
        super().__init__()
    
    def validate(self, surname, name, email, passport, telephone, login, password):
        errorCode = self.__checkFIO(surname, name)
        if (errorCode == 0):
            errorCode = self.__checkData(email, passport, telephone)
            if (errorCode == 0):
                errorCode = self.__checkLogPas(login, password)
        
        return errorCode

    def __checkFIO(self, surname, name):
        if (len(surname) == 0):
            return BAD_SURNAME
        elif (len(name) == 0):
            return BAD_NAME
        else:
            return OK
    
    def __checkData(self, email, passport, telephone):
        errorCode = self.__checkEmail(email)
        if (errorCode == 0):
            errorCode = self.__checkPassport(passport)
            if (errorCode == 0):
                errorCode = self.__checkTelephone(telephone)
        
        return errorCode
    
    def __checkEmail(self, email):
        errorCode = OK
        if '@' not in email:
            errorCode = BAD_EMAIL
        elif email.find('@') == 0:
            errorCode = BAD_EMAIL
        return errorCode
    
    def __checkPassport(self, passport):
        errorCode = OK
        if (len(passport) != 10):
            errorCode = BAD_PASSPORT
        try:
            passport = int(passport)
        except:
            errorCode = BAD_PASSPORT
        return errorCode
    
    def __checkTelephone(self, telephone):
        errorCode = OK
        N = len(telephone)
        if (N != 11) and (N != 12):
            errorCode = BAD_TELEPHONE
        if (N == 11):
            if (telephone[0] != '8'):
                errorCode = BAD_TELEPHONE
            else:
                try:
                    int(telephone)
                except:
                    errorCode = BAD_TELEPHONE
        
        elif (N == 12):
            if (telephone[0] != '+') and (telephone[1] != '7'):
                errorCode = BAD_TELEPHONE
            else:
                try:
                    int(telephone[1:])
                except:
                    errorCode = BAD_TELEPHONE
        return errorCode
    
    def __checkLogPas(self, login, password):
        if (len(login) < 6):
            return BAD_LOGIN
        elif (len(password) < 6):
            return BAD_PASSWORD
        else:
            return OK
    
class ValidateCoefManager(BaseValidateManager):
    def __init__(self):
        super().__init__()
    
    def validate(self, p1, p2, p3):
        if np.abs(np.sum([p1, p2, p3]) - 100) < EPS:
            return OK
        else:
            return BAD_COEFS