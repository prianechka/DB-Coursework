import sys
from controllers.controllers import *
sys.path.append("./facade")
sys.path.append("./controllers")
sys.path.append("./managers")
from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtCore import Qt
from tabulate import tabulate
from facade.Facade import Facade
from facade.command import *
from errors import *

class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        self.sizeX = 800
        self.sizeY = 600
        QtWidgets.QWidget.__init__(self)
        self.FirstMenuUI()
        self.Facade = Facade()
        self.controller = BaseController(self)
    
    def FirstMenuUI(self):
        uic.loadUi("./ui/first.ui", self)
        self.controller = FirstMenuUIController(self)
        self.controller.execute()
    
    def BetUI(self):
        uic.loadUi("./ui/betUI.ui", self)
        self.controller = betUIController(self)
        self.controller.execute()

    def RegistrateUI(self):
        uic.loadUi("./ui/registrate.ui", self)
        self.controller = RegistrateUIController(self)
        self.controller.execute()
    
    def MainMenuUI(self):
        uic.loadUi("./ui/mainMenu.ui", self)
        self.controller = MainMenuUIController(self)
        self.controller.execute()
    
    def ManagerMainUI(self):
        uic.loadUi("./ui/managerMain.ui", self)
        self.controller = MainManagerUIController(self)
        self.controller.execute()

    def verifyMenuUI(self):
        uic.loadUi("./ui/verify.ui", self)
        self.controller = VerifyUIController(self)
        self.controller.execute()
    
    def statMainUI(self):
        uic.loadUi("./ui/statMain.ui", self)
        self.controller = StatMainUIController(self)
        self.controller.execute()
    
    def addMatchUI(self):
        uic.loadUi("./ui/addMatch.ui", self)
        self.controller = AddMatchUIController(self)
        self.controller.execute()
    
    def checkLineUI(self):
        uic.loadUi("./ui/lineAnaliticUI.ui", self)
        self.controller = LineAnaliticUIController(self)
        self.controller.execute()
    
    def donateUI(self):
        uic.loadUi("./ui/donate.ui", self)
        self.controller = DonateController(self)
        self.controller.execute()
    
    def checkHistoryUI(self):
        uic.loadUi("./ui/checkHistory.ui", self)
        self.controller = CheckHistoryController(self)
        self.controller.execute()

app = QtWidgets.QApplication(sys.argv)
window = MyWindow()
window.show()
sys.exit(app.exec_())
