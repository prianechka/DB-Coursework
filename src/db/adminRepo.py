from db.baseRepo import BaseRepo
import sys
sys.path.append("/home/prianechka/Education/BMSTU/DB-CourseWork/DB-Coursework/src/")
from errors import *

class AdminRepo(BaseRepo):
    def __init__(self):
        super().__init__()
        self.cur = self.connection.cursor()
        self.execute('SET ROLE Administrator;')
    
    def findVerifyAccs(self, surnameString):
        executeString = (f"SELECT * FROM BK.verifyAccs('{surnameString}');")

        return self.execute(executeString)
    
    def changeStateAcc(self, id, status):
        executeString = f"CALL BK.updateStatus({id}, '{status}')"
        
        return self.execute(executeString)
    
    def GetAllActiveAccs(self):
        executeString = f"SELECT * FROM BK.GetAllActiveAccs()"

        return self.execute(executeString)