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
        self.dfStudents = pd.DataFrame(stuNames)
        self.stuNumber = self.dfStudents.shape[0]
        self.scoreGen = ScoreGen(self.stuNumber)
        return
    

    def printAll(self):
        print(self.dfStudents)
        return
    

    def appendMyself(self, myDict):
        myDf = pd.DataFrame(myDict)
        print(myDf)
        self.dfStudents = pd.concat([self.dfStudents, myDf], ignore_index = True) 
        return
    
    
    def generateScores(self):
        dfChinese = self.scoreGen.scoreChinese()
        self.dfStudents = pd.concat([self.dfStudents, dfChinese], axis=1)

        dfMath = self.scoreGen.scoreMath()
        self.dfStudents = pd.concat([self.dfStudents, dfMath], axis=1)

        dfEnglish = self.scoreGen.scoreEnglish()
        self.dfStudents = pd.concat([self.dfStudents, dfEnglish], axis=1)

        dfPhysics = self.scoreGen.scorePhysics()
        self.dfStudents = pd.concat([self.dfStudents, dfPhysics], axis=1)

        dfChemistry = self.scoreGen.scoreChemistry()
        self.dfStudents = pd.concat([self.dfStudents, dfChemistry], axis=1)

        dfPE = self.scoreGen.scorePE()
        self.dfStudents = pd.concat([self.dfStudents, dfPE], axis=1)

        dfPolitics = self.scoreGen.scorePolitics()
        self.dfStudents = pd.concat([self.dfStudents, dfPolitics], axis=1)

        dfHistory = self.scoreGen.scoreHistory()
        self.dfStudents = pd.concat([self.dfStudents, dfHistory], axis=1)
    
        dfBiology = self.scoreGen.scoreBiology()
        self.dfStudents = pd.concat([self.dfStudents, dfBiology], axis=1)

        dfGeography = self.scoreGen.scoreGeography()
        self.dfStudents = pd.concat([self.dfStudents, dfGeography], axis=1)

        self.dfStudents["总分"] = self.dfStudents[["语文", "数学", "英语", "物理", "化学", "体育", "道法", "历史", "生物", "地理"]].sum(axis=1)
        return
    
    
    def showScoreHist(self, courseName):
        plt.hist(self.dfStudents[courseName], bins=30, histtype="bar", edgecolor='black', linewidth=1.2)
        plt.xlabel("{}得分".format(courseName), fontproperties=fontP)
        plt.ylabel('人数', fontproperties=fontP)
        plt.show()
        return