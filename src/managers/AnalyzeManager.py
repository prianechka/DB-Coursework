from BaseManager import BaseManager
from random import random

class AnalyzerManager(BaseManager):
    def __init__(self):
        super().__init__()
    
    def createCoefs(self, p1, p2, p3):
        marge = random() / 10
        p1 /= 100
        p2 /= 100
        p3 /= 100

        p1 = 1 / (p1 + marge / 3)
        p2 = 1 / (p2 + marge / 3)
        p3 = 1 / (p3 + marge / 3)

        return p1, p2, p3