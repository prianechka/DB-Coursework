def singleton(class_):
    instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance

@singleton
class SessionHolder():
    def __init__(self) -> None:
        self.sessionInfo = {"currentRole" : "UnAuthorized"}

    def foldSessionInfo(self):
        ''' self.sessionInfo = {"currentRole" : "UnAuthorized", "userLogin" : "", "userWebID" : -1, "userAccountID" : -1,
                            "userStatus" : "", "userBalance" : -1, "userMaxBet" : -1}
        '''
        self.sessionInfo = {"currentRole" : "UnAuthorized"}

    def getRole(self):
        return self.sessionInfo["currentRole"]
    
    def setRole(self, role):
        if role in ['Blocked', 'Active', 'On Verify']:
            self.sessionInfo['currentRole'] = role
    
    def getUserLogin(self):
        return self.sessionInfo["userLogin"]
    
    def setUserLogin(self, login):
        self.sessionInfo["userLogin"] = login
    
    def getUserWebID(self):
        return self.sessionInfo["userWebID"]
    
    def setUserWebID(self, webID):
        self.sessionInfo["userWebID"] = webID
    
    def getUserAccID(self):
        return self.sessionInfo["userWebID"]
    
    def setUserAccID(self, accID):
        self.sessionInfo["userAccountID"] = accID
    
    def getUserStatus(self):
        return self.sessionInfo["userStatus"]
    
    def setUserStatus(self, status):
        self.sessionInfo["userStatus"] = status
    
    def getUserBalance(self):
        return self.sessionInfo["userBalance"]
    
    def setUserBalance(self, balance):
        self.sessionInfo["userBalance"] = balance
    
    def getUserMaxBet(self):
        return self.sessionInfo["userMaxBet"]
    
    def setUserMaxBet(self, maxBet):
        self.sessionInfo["userMaxBet"] = maxBet
    
    def getAllInfo(self):
        return self.sessionInfo
    
