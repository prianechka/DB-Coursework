import imp
from managers.BaseManager import BaseManager
from managers.validate.validateManager import ValidateCoefManager, ValidateGameManager
from managers.analyzer.analyzerHelper import AnalyzerHelper
from db.analyzerRepo import AnalyzerRepo
import sys
sys.path.append("/home/prianechka/Education/BMSTU/DB-CourseWork/DB-Coursework/src/")
from errors import *

class AnalyzeManager(BaseManager):
    def __init__(self):
        self.repo = AnalyzerRepo()

    def viewTeams(self, teamName):
        return self.repoviewTeams(teamName)
    
    def addGame(self, id1Team, id2Team, p1, p2, p3, dateMatch, timeMatch):
        errorCode = ValidateGameManager().validate(id1Team, id2Team, p1, p2, p3, dateMatch, timeMatch)

        if errorCode == OK:
            p1, p2, p3 = AnalyzerHelper().createCoefs(p1, p2, p3)
            return self.repo.addGame(id1Team, id2Team, p1, p2, p3, dateMatch, timeMatch)
        else:
            return errorCode, []
    
    def viewGamesAnalyze(self, teamName):
        return self.repo.viewGamesAnalyze(teamName)
    
    def changeGameStatus(self, id):
        return self.repo.changeGameStatus(id)
    
    def changeGameResult(self, id, result):
        return self.repo.changeGameResult(id, result)

    def changeGameCoef(self, id, p1, x, p2):
        errorCode = ValidateCoefManager().validate(p1, x, p2)

        if errorCode == OK:
            p1, x, p2 = AnalyzerHelper().createCoefs(p1, x, p2)
            return self.repo.changeGameCoef(id, p1, x, p2)
        else:
            return errorCode, []
        
    def findProbs(self, p1, p2, p3):
        return AnalyzerHelper().findProbs(p1, p2, p3)
    
    def viewTeams(self, teamName):
        return self.repo.viewTeams(teamName)
    
    def addGame(self, id1Team, id2Team, p1, p2, p3, dateMatch, timeMatch):
        errorCode = ValidateGameManager().validate(id1Team, id2Team, p1, p2, p3, dateMatch, timeMatch)

        if errorCode == OK:
            k1, k2, k3 = AnalyzerHelper().createCoefs(p1, p2, p3)
            return self.repo.addGame(id1Team, id2Team, k1, k2, k3, dateMatch, timeMatch)
        else:
            return errorCode, []
    
    def viewGamesAnalyze(self, teamName):
        return self.repo.viewGamesAnalyze(teamName)
    
    def changeGameStatus(self, id):
        return self.repo.changeGameStatus(id)
    
    def changeGameResult(self, id, result):
        return self.repo.changeGameResult(id, result)

    def changeGameCoef(self, id, p1, x, p2):
        errorCode = ValidateCoefManager().validate(p1, x, p2)

        if errorCode == OK:
            p1, x, p2 = AnalyzerHelper().createCoefs(p1, x, p2)
            return self.repo.changeGameCoef(id, p1, x, p2)
        else:
            return errorCode, []
        
    def findProbs(self, p1, p2, p3):
        return AnalyzerHelper().findProbs(p1, p2, p3)
    
