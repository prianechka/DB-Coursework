from db.baseRepo import BaseRepo
import sys
sys.path.append("/home/prianechka/Education/BMSTU/DB-CourseWork/DB-Coursework/src/")
from errors import *

class AnalyzerRepo(BaseRepo):
    def __init__(self):
        super().__init__()
        self.cur = self.connection.cursor()
        self.execute('SET ROLE Analyzist;')
    
    def viewTeams(self, teamName):
        executeString = f"SELECT * FROM BK.viewTeams('{teamName}')"

        return self.execute(executeString)
    
    def addGame(self, id1Team, id2Team, p1, p2, p3, dateMatch, timeMatch):
        executeString = f"CALL BK.addGame({id1Team}, {id2Team}, {p1}, {p2}, {p3}, '{dateMatch}', '{timeMatch}')"

        return self.execute(executeString)
    
    def viewGamesAnalyze(self, teamName):
        executeString = f"SELECT * FROM BK.viewGamesAnalyze('{teamName}')"

        return self.execute(executeString)
    
    def changeGameStatus(self, id):
        executeString = f"CALL BK.changeGameState({id});"

        return self.execute(executeString)

    def changeGameResult(self, id, result):
        executeString = f"CALL BK.changeGameResult({id}, '{result}');"

        return self.execute(executeString)
    
    def changeGameCoef(self, id, w1, x, w2):
        executeString = f"CALL BK.changeGameCoef({id}, {w1}, {x}, {w2});"

        return self.execute(executeString)