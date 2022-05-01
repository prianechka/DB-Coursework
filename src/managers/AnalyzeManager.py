from matplotlib.pyplot import margins
from BaseManager import BaseManager
from random import random

class AnalyzerManager(BaseManager):
    def __init__(self):
        super().__init__()
        self.marge = 0.05
    
    def createCoefs(self, p1, p2, p3):
        p1 /= 100
        p2 /= 100
        p3 /= 100

        p1 = 1 / (p1 + self.marge / 3)
        p2 = 1 / (p2 + self.marge / 3)
        p3 = 1 / (p3 + self.marge / 3)

        return round(p1, 2), round(p2, 2), round(p3, 2)
    
    def findProbs(self, p1, p2, p3):
        p1 = 1 / p1 - self.marge / 3
        p2 = 1 / p2 - self.marge / 3
        p3 = 1 / p3 - self.marge / 3

        p1 *= 100
        p2 *= 100
        p3 *= 100

        return p1, p2, p3