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
        self.myName = ""
        #append a tag so my name know who is myself in the dataframe:
        self.myNameTag = "(mySelf)"

        #init score degrade:
        self.scoreCounts = pd.DataFrame(columns = ['分数', '人数'])
        self.scoreHighGate = 655
        self.scoreLowGate = 400
        return
    

    def printAll(self):
        print(self.dfStudents)
        return
    

    def appendMyself(self, mySelf):
        self.myName = mySelf["姓名"]
        mySelf["姓名"] = "{}{}".format(self.myName, self.myNameTag)

        #change each item in dict into list, so it can be added to the dataframe:
        mySelf["姓名"] = [mySelf["姓名"]]
        mySelf["性别"] = [mySelf["性别"]]
        mySelf["语文"] = [mySelf["语文"]]
        mySelf["数学"] = [mySelf["数学"]]
        mySelf["英语"] = [mySelf["英语"]]
        mySelf["物理"] = [mySelf["物理"]]
        mySelf["化学"] = [mySelf["化学"]]
        mySelf["体育"] = [mySelf["体育"]]
        mySelf["道法"] = [mySelf["道法"]]
        mySelf["历史"] = [mySelf["历史"]]
        mySelf["生物"] = [mySelf["生物"]]
        mySelf["地理"] = [mySelf["地理"]]
        mySelf["总分"] = [mySelf["总分"]]

        myDf = pd.DataFrame(mySelf)
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
    

    def generateScoreCount(self):
        scoreStats = self.dfStudents["总分"].value_counts().sort_index(ascending=False)

        #filter score below low gate:
        scoreStats = scoreStats[scoreStats.index >= self.scoreLowGate]

        self.scoreCounts['分数'] = scoreStats.index
        self.scoreCounts['人数'] = scoreStats.values

        #merge socres above high gate:
        self.scoreCounts.loc[self.scoreCounts['分数'].between(self.scoreHighGate, 710), '分数'] = self.scoreHighGate
        self.scoreCounts = self.scoreCounts.groupby('分数', as_index=False).agg({'人数': 'sum'})


        self.scoreCounts = self.scoreCounts.sort_values(by='分数', ascending=False)
        return
    

    def generateCumulativeScore(self):
        self.scoreCounts['累计'] = self.scoreCounts['人数'].cumsum()
        self.scoreCounts.iloc[0, self.scoreCounts.columns.get_loc('累计')] = self.scoreCounts.iloc[0, self.scoreCounts.columns.get_loc('人数')]
        return

    
    
    def showScoreHist(self, courseName):
        plt.hist(self.dfStudents[courseName], bins=30, histtype="bar", edgecolor='black', linewidth=1.2)
        plt.xlabel("{}得分".format(courseName), fontproperties=fontP)
        plt.ylabel('人数', fontproperties=fontP)
        plt.show()
        return
    

    def showScoreCount(self):
        print(self.scoreCounts)
        return