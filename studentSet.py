import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager

from utils.studentName import StudentName
from utils.scoreGen import ScoreGen

fontP = font_manager.FontProperties()
fontP.set_family('SimHei')
fontP.set_size(14)

class StudentSet:
    def __init__(self, stuNames):
        self.scoreGen = ScoreGen()
        self.dfStudents = pd.DataFrame(stuNames)
        self.stuNumber = self.dfStudents.shape[0]
        return
    
    def printAll(self):
        print(self.dfStudents)
        return
    
    def generateScores(self):
        dfChinese = self.scoreGen.scoreChinese(self.stuNumber)
        self.dfStudents = pd.concat([self.dfStudents, dfChinese], axis=1)

        dfMath = self.scoreGen.scoreMath(self.stuNumber)
        self.dfStudents = pd.concat([self.dfStudents, dfMath], axis=1)

        dfEnglish = self.scoreGen.scoreEnglish(self.stuNumber)
        self.dfStudents = pd.concat([self.dfStudents, dfEnglish], axis=1)

        dfPhysics = self.scoreGen.scorePhysics(self.stuNumber)
        self.dfStudents = pd.concat([self.dfStudents, dfPhysics], axis=1)

        dfChemistry = self.scoreGen.scoreChemistry(self.stuNumber)
        self.dfStudents = pd.concat([self.dfStudents, dfChemistry], axis=1)
        return
    
    def showScoreHist(self, courseName):
        plt.hist(self.dfStudents[courseName], bins=30, histtype="bar", edgecolor='black', linewidth=1.2)
        plt.xlabel("{}得分".format(courseName), fontproperties=fontP)
        plt.ylabel('人数', fontproperties=fontP)
        plt.show()
        return