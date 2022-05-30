import sys
sys.path.append("/home/prianechka/Education/BMSTU/DB-CourseWork/DB-Coursework/src/managers")
from managers.connectionManager import ConnectionManager


class BaseCommand():
    def __init__(self):
        pass

    def execute(self):
        pass

class AuthorizeCommand(BaseCommand):
    def __init__(self):
        super().__init__()

    def execute(self, login, password):
        return ConnectionManager().TryToAuthorize(login, password)

class RegistrateCommand(BaseCommand):
    def __init__(self):
        super().__init__()
    
    def execute(self, surname, name, dateOfBirth, email, passport, telephone, login, password):
        return ConnectionManager().TryToRegistrate(surname, name, dateOfBirth, email, passport, telephone, login, password)

class LoginCommand(BaseCommand):
    def __init__(self):
        super().__init__()
    
    def execute(self):
        return ConnectionManager().GetLogin()

class UserDataCommand(BaseCommand):
    def __init__(self):
        super().__init__()
    
    def execute(self):
        return ConnectionManager().GetBaseUserInfo()

class CleanCommand(BaseCommand):
    def __init__(self):
        super().__init__()
    
    def execute(self):
        return ConnectionManager().foldUserInfo()

class FindVerifyCommand(BaseCommand):
    def __init__(self):
        super().__init__()
    
    def execute(self, surnameString):
        return ConnectionManager().findVerifyAccs(surnameString)

class ChangeStatusAccCommand(BaseCommand):
    def __init__(self):
        super().__init__()
    
    def execute(self, id, status):
        return ConnectionManager().changeStateAcc(id, status)

class ViewTeamsCommand(BaseCommand):
    def __init__(self):
        super().__init__()
    
    def execute(self, teamName):
        return ConnectionManager().viewTeams(teamName)

class AddGameCommand(BaseCommand):
    def __init__(self):
        super().__init__()
    
    def execute(self, id1Team, id2Team, p1, p2, p3, dateMatch, timeMatch):
        return ConnectionManager().addGame(id1Team, id2Team, p1, p2, p3, dateMatch, timeMatch)

class ViewGamesAnalyze(BaseCommand):
    def __init__(self):
        super().__init__()
    
    def execute(self, teamName):
        return ConnectionManager().viewGamesAnalyze(teamName)

class ChangeGameStatus(BaseCommand):
    def __init__(self):
        super().__init__()
    
    def execute(self, id):
        return ConnectionManager().changeGameStatus(id)

class ChangeGameResult(BaseCommand):
    def __init__(self):
        super().__init__()
    
    def execute(self, id, result):
        return ConnectionManager().changeGameResult(id, result)

class FindProbs(BaseCommand):
    def __init__(self):
        super().__init__()
    
    def execute(self, p1, p2, p3):
        return ConnectionManager().findProbs(p1, p2, p3)

class EditCoefCommand(BaseCommand):
    def __init__(self):
        super().__init__()
    
    def execute(self, id, p1, x, p2):
        return ConnectionManager().changeGameCoef(id, p1, x, p2)

class GetUserBetInfoCommand(BaseCommand):
    def __init__(self):
        super().__init__()
    
    def execute(self):
        return ConnectionManager().GetUserBetInfo()

class MakeBetCommand(BaseCommand):
    def __init__(self):
        super().__init__()
    
    def execute(self, choosedGameId, result, betSum, kf):
        return ConnectionManager().MakeBet(choosedGameId, result, betSum, kf)

class UpdateUserConnectionInfoCommand(BaseCommand):
    def __init__(self):
        super().__init__()
    
    def execute(self):
        login = ConnectionManager().GetLogin()
        return ConnectionManager().UpdateUserConnectInfo(login)

class DonateCommand(BaseCommand):
    def __init__(self):
        super().__init__()
    
    def execute(self, value):
        return ConnectionManager().Donate(value)

class CheckHistoryCommand(BaseCommand):
    def __init__(self):
        super().__init__()
    
    def execute(self):
        return ConnectionManager().CheckHistory()

class GetAllActiveAccsCommand(BaseCommand):
    def __init__(self):
        super().__init__()
    
    def execute(self):
        return ConnectionManager().GetAllActiveAccs()