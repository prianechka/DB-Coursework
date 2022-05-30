from managers.BaseManager import BaseManager
from db.adminRepo import AdminRepo

import sys
sys.path.append("/home/prianechka/Education/BMSTU/DB-CourseWork/DB-Coursework/src/")
from errors import *


class AdminManager(BaseManager):
    def __init__(self):
        self.repo = AdminRepo()

    def findVerifyAccs(self, surnameString):
        return self.repo.findVerifyAccs(surnameString)
    
    def changeStateAcc(self, id, status):
        return self.repo.changeStateAcc(id, status)
    
    def GetAllActiveAccs(self):
        return self.repo.GetAllActiveAccs()