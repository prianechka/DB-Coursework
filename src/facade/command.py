import sys
sys.path.append("/home/prianechka/Education/BMSTU/DB-CourseWork/DB-Coursework/src/managers")
from managers.authManager import AuthManager
from managers.player.playerManager import PlayerManager
from managers.analyzer.analyzeManager import AnalyzeManager
from managers.admin.adminManager import AdminManager


class BaseCommand():
    def __init__(self):
        pass

    def execute(self):
        pass

class AuthorizeCommand(BaseCommand):
    def __init__(self):
        super().__init__()

    def execute(self, login, password):
        return AuthManager().TryToAuthorize(login, password)

class RegistrateCommand(BaseCommand):
    def __init__(self):
        super().__init__()
    
    def execute(self, surname, name, dateOfBirth, email, passport, telephone, login, password):
        return AuthManager().TryToRegistrate(surname, name, dateOfBirth, email, passport, telephone, login, password)

class LoginCommand(BaseCommand):
    def __init__(self):
        super().__init__()
    
    def execute(self):
        return PlayerManager().GetLogin()

class UserDataCommand(BaseCommand):
    def __init__(self):
        super().__init__()
    
    def execute(self):
        return PlayerManager().GetBaseUserInfo()

class CleanCommand(BaseCommand):
    def __init__(self):
        super().__init__()
    
    def execute(self):
        return PlayerManager().foldUserInfo()

class FindVerifyCommand(BaseCommand):
    def __init__(self):
        super().__init__()
    
    def execute(self, surnameString):
        return AdminManager().findVerifyAccs(surnameString)

class ChangeStatusAccCommand(BaseCommand):
    def __init__(self):
        super().__init__()
    
    def execute(self, id, status):
        return AdminManager().changeStateAcc(id, status)

class ViewTeamsCommand(BaseCommand):
    def __init__(self):
        super().__init__()
    
    def execute(self, teamName):
        return AnalyzeManager().viewTeams(teamName)

class AddGameCommand(BaseCommand):
    def __init__(self):
        super().__init__()
    
    def execute(self, id1Team, id2Team, p1, p2, p3, dateMatch, timeMatch):
        return AnalyzeManager().addGame(id1Team, id2Team, p1, p2, p3, dateMatch, timeMatch)

class ViewGamesAnalyze(BaseCommand):
    def __init__(self):
        super().__init__()
    
    def execute(self, teamName):
        return AnalyzeManager().viewGamesAnalyze(teamName)

class ChangeGameStatus(BaseCommand):
    def __init__(self):
        super().__init__()
    
    def execute(self, id):
        return AnalyzeManager().changeGameStatus(id)

class ChangeGameResult(BaseCommand):
    def __init__(self):
        super().__init__()
    
    def execute(self, id, result):
        return AnalyzeManager().changeGameResult(id, result)

class FindProbs(BaseCommand):
    def __init__(self):
        super().__init__()
    
    def execute(self, p1, p2, p3):
        return AnalyzeManager().findProbs(p1, p2, p3)

class EditCoefCommand(BaseCommand):
    def __init__(self):
        super().__init__()
    
    def execute(self, id, p1, x, p2):
        return AnalyzeManager().changeGameCoef(id, p1, x, p2)

class GetUserBetInfoCommand(BaseCommand):
    def __init__(self):
        super().__init__()
    
    def execute(self):
        return PlayerManager().GetUserBetInfo()

class MakeBetCommand(BaseCommand):
    def __init__(self):
        super().__init__()
    
    def execute(self, choosedGameId, result, betSum, kf):
        return PlayerManager().MakeBet(choosedGameId, result, betSum, kf)

class UpdateUserConnectionInfoCommand(BaseCommand):
    def __init__(self):
        super().__init__()
    
    def execute(self):
        login = PlayerManager().GetLogin()
        return PlayerManager().UpdateUserConnectInfo(login)

class DonateCommand(BaseCommand):
    def __init__(self):
        super().__init__()
    
    def execute(self, value):
        return PlayerManager().Donate(value)

class CheckHistoryCommand(BaseCommand):
    def __init__(self):
        super().__init__()
    
    def execute(self):
        return PlayerManager().CheckHistory()

class GetAllActiveAccsCommand(BaseCommand):
    def __init__(self):
        super().__init__()
    
    def execute(self):
        return AdminManager().GetAllActiveAccs()