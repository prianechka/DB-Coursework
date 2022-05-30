from BaseManager import BaseManager

class AnalyzerHelper(BaseManager):
    def __init__(self):
        super().__init__()
        self.marge = 0.05
    
    def createCoefs(self, p1, p2, p3):
        p1 /= 100
        p2 /= 100
        p3 /= 100

        k1 = 1 / (p1 + self.marge / 3)
        k2 = 1 / (p2 + self.marge / 3)
        k3 = 1 / (p3 + self.marge / 3)

        return round(k1, 2), round(k2, 2), round(k3, 2)
    
    def findProbs(self, k1, k2, k3):
        p1 = 1 / k1 - self.marge / 3
        p2 = 1 / k2 - self.marge / 3
        p3 = 1 / k3 - self.marge / 3

        p1 *= 100
        p2 *= 100
        p3 *= 100

        return p1, p2, p3