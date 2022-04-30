import sys
sys.path.append("/home/prianechka/Education/BMSTU/DB-CourseWork/src/DataBase/managers")
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