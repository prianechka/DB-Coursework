from command import *

class Facade():
    def __init__(self):
        pass

    def execute(self, command, *args):
        return command.execute(*args)