from managers.BaseManager import BaseManager
from db.playerRepo import PlayerRepo
from managers.player.sessionHolder import SessionHolder
import sys
sys.path.append("/home/prianechka/Education/BMSTU/DB-CourseWork/DB-Coursework/src/")
from errors import *

class PlayerManager(BaseManager):
    def __init__(self):
        self.holder = SessionHolder()
        self.repo = PlayerRepo()
    
    def GetLogin(self):
        return self.holder.getUserLogin()
    
    def GetRole(self):
        return self.holder.getRole()
    
    def GetBaseUserInfo(self):
        return self.holder.getUserStatus(), self.holder.getUserBalance()
    
    def GetUserBetInfo(self):
        return self.holder.getUserBalance(), self.holder.getUserMaxBet()
    
    def foldUserInfo(self):
        self.holder.foldSessionInfo()

    def UpdateUserConnectInfo(self, login):
        errorCode, webUserID, accountID, userStatus, balance, maxBet = self.repo.getUserInfo(login)
        if errorCode == OK:
            self.holder.setUserWebID(webUserID)
            self.holder.setUserAccID(accountID)
            self.holder.setUserStatus(userStatus)
            self.holder.setUserBalance(balance)
            self.holder.setUserMaxBet(maxBet)
        return errorCode
    
    def MakeBet(self, choosedGameId, result, betSum, kf):
        accID = int(self.holder.getUserAccID())

        errorCode, res =  self.repo.makeBet(choosedGameId, result, accID, betSum, kf)

        if errorCode == OK:
            self.holder.setUserBalance(self.holder.getUserBalance() - betSum)
        
        return errorCode, res
    
    def Donate(self, value):
        id = self.holder.getUserAccID()
        
        errorCode, res =  self.repo.Donate(id, value)

        if errorCode == OK:
            self.holder.setUserBalance(self.holder.getUserBalance() + value)
        
        return errorCode, res
    
    def CheckHistory(self):
        id = self.holder.getUserAccID()

        return  self.repo.CheckHistory(id)