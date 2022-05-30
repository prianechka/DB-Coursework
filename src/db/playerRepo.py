from db.baseRepo import BaseRepo
import sys
sys.path.append("/home/prianechka/Education/BMSTU/DB-CourseWork/DB-Coursework/src/")
from errors import *

class PlayerRepo(BaseRepo):
    def __init__(self):
        super().__init__()
        self.cur = self.connection.cursor()
        self.execute('SET ROLE Client;')

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
    
    def viewGamesAnalyze(self, teamName):
        executeString = f"SELECT * FROM BK.viewGamesAnalyze('{teamName}')"

        return self.execute(executeString)

    def makeBet(self, choosedGameId, result, accID, betSum, kf):
        executeString = f"CALL BK.MakeBet({choosedGameId}, {result}, {accID}, {betSum}, {kf});"

        return self.execute(executeString)
    
    def Donate(self, id, value):
        executeString = f"CALL BK.Donate({id}, {value});"

        return self.execute(executeString)
    
    def CheckHistory(self, id):
        executeString = f"SELECT * FROM BK.GetBetHistory({id})"

        return self.execute(executeString)