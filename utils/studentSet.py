import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager
from tabulate import tabulate
from progress.spinner import LineSpinner
import random


import config.config as GlobalConfig
from utils.scoreGen import ScoreGen
from utils.schoolStats import SchoolStats

fontP = font_manager.FontProperties()
fontP.set_family('SimHei')
fontP.set_size(14)

class StudentSet:
    def __init__(self, stuNames):
        #所有报考学生的记录：
        self.dfStudents = pd.DataFrame(stuNames)

        #报考学生总数：
        self.stuNumber = self.dfStudents.shape[0]

        #参加第二批次填报志愿的学生:
        self.stuForSecondRoundNum = 0
        self.dfStuForSecondRound = pd.DataFrame()

        self.scoreGen = ScoreGen(self.stuNumber)

        self.myName = ""
        #append a tag so my name know who is myself in the dataframe:
        self.myNameTag = "(mySelf)"
        self.myTotalScore = 0
        self.myScoreRank = 0

        #init score degrade:
        self.dfScoreCounts = pd.DataFrame(columns = ['分数', '人数'])

        #重高线
        self.privilegeScoreGate = 0
        return
    

    #学生分类：统招或调剂
    def categorizeStudent(self):
        numLocalStudent = GlobalConfig.StudentTotal - GlobalConfig.EdgeStudentTotal
        numEdgeStudent = GlobalConfig.EdgeStudentTotal

        lst1 = ['统招' for _ in range(numLocalStudent)]
        lst2 = ['调剂' for _ in range(numEdgeStudent)]

        catList = lst1 + lst2
        random.shuffle(catList)
        self.dfStudents['类型'] = catList
        return
    

    def showStudents(self):
        print(self.dfStudents)
        return
    

    def getStuForSecondRoundNum(self):
        return self.stuForSecondRoundNum
    

    def appendMyself(self, mySelf):
        self.myName = mySelf["姓名"]
        mySelf["姓名"] = "{}{}".format(self.myName, self.myNameTag)
        mySelf["类型"] = "统招"
        self.myTotalScore = mySelf["总分"]

        #获取自己的得分排名：
        scoreLevel = self.myTotalScore
        if(scoreLevel > GlobalConfig.ScoreTopGate):
            scoreLevel = GlobalConfig.ScoreTopGate
        if(scoreLevel < GlobalConfig.ScoreLowGate):
            scoreLevel = GlobalConfig.ScoreLowGate
        self.myScoreRank = self.dfScoreCounts.loc[self.dfScoreCounts["分数"] == scoreLevel, "累计"].values[0]  

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
    

    def getMyTotalScore(self):
        return self.myTotalScore
    

    def generateScoreCount(self):
        scoreStats = self.dfStudents["总分"].value_counts().sort_index(ascending=False)

        #filter score below low gate:
        scoreStats = scoreStats[scoreStats.index >= GlobalConfig.ScoreLowGate]

        self.dfScoreCounts['分数'] = scoreStats.index
        self.dfScoreCounts['人数'] = scoreStats.values

        #merge socres above high gate:
        self.dfScoreCounts.loc[self.dfScoreCounts['分数'].between(GlobalConfig.ScoreTopGate, 710), '分数'] = GlobalConfig.ScoreTopGate
        self.dfScoreCounts = self.dfScoreCounts.groupby('分数', as_index=False).agg({'人数': 'sum'})


        self.dfScoreCounts = self.dfScoreCounts.sort_values(by='分数', ascending=False)
        return
    

    def generateCumulativeScore(self):
        self.dfScoreCounts['累计'] = self.dfScoreCounts['人数'].cumsum()
        self.dfScoreCounts.iloc[0, self.dfScoreCounts.columns.get_loc('累计')] = self.dfScoreCounts.iloc[0, self.dfScoreCounts.columns.get_loc('人数')]
        return
    

    def generateEachAndTotalScores(self):
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
     
    
    def generateScores(self):
        print("\n")
        bar = LineSpinner('中考成绩统计中，请稍后。。。')

        #generate each student's score, including each subject and total score:
        self.generateEachAndTotalScores()

        #generate score count:
        self.generateScoreCount()

        #generate cumulative count for each score:
        self.generateCumulativeScore()

        #check score distribution until we got a good one:
        isGoodScoreDistribution = self.scoreGen.isGoodScoreDistribution(self.dfScoreCounts[["分数", "累计"]].copy())
        while(isGoodScoreDistribution != True):
            self.dfStudents = self.dfStudents.drop(["语文", "数学", "英语", "物理", "化学", "体育", "道法", "历史", "生物", "地理", "总分"], axis=1)
            del self.dfScoreCounts
            self.dfScoreCounts = pd.DataFrame(columns = ['分数', '人数'])

            self.generateEachAndTotalScores()
            self.generateScoreCount()
            self.generateCumulativeScore()

            isGoodScoreDistribution = self.scoreGen.isGoodScoreDistribution(self.dfScoreCounts[["分数", "累计"]].copy())

            bar.next()     
        return
    
    
    
    def showScoreHist(self, courseName):
        plt.hist(self.dfStudents[courseName], bins=30, histtype="bar", edgecolor='black', linewidth=1.2)
        plt.xlabel("{}得分".format(courseName), fontproperties=fontP)
        plt.ylabel('人数', fontproperties=fontP)
        plt.show()
        return
    

    def showScoreCount(self):
        print(tabulate(self.dfScoreCounts, showindex="never", headers="keys", tablefmt="double_grid"))
        return
    

    def generateMyScore(self, scoreType):
        if(scoreType == "电脑随机生成"):
            return self.scoreGen.genMyScoreAuto()
        elif(scoreType == "手动输入"):
            return self.scoreGen.genMyScoreManual()
        else:
            print("Unknow score gen type: {}".format(scoreType))

    
    def getMyScoreRank(self):
        return self.myScoreRank


    def displayMyScoreAndRank(self):
        myData = self.dfStudents.loc[self.dfStudents["姓名"] == (self.myName + self.myNameTag)]
        myData = myData.drop('姓名', axis=1)
        myData = myData.drop('性别', axis=1)
        myData = myData.drop('类型', axis=1)

        print("\n")
        print("{}同学, 您本次中考的成绩为：".format(self.myName))
        print(GlobalConfig.bcolors.YELLO + tabulate(myData, showindex="never", headers="keys", tablefmt="double_grid") + GlobalConfig.bcolors.ENDC)

        totalScore = myData.iloc[0]["总分"]
        if(totalScore > GlobalConfig.ScoreTopGate):
            totalScore = GlobalConfig.ScoreTopGate
        if(totalScore < GlobalConfig.ScoreLowGate):
            totalScore = GlobalConfig.ScoreLowGate

        print("\n")
        print(GlobalConfig.bcolors.YELLO + "{}".format(totalScore) + GlobalConfig.bcolors.ENDC + "分的累计人数为： " + GlobalConfig.bcolors.YELLO + "{}".format(self.myScoreRank) + GlobalConfig.bcolors.ENDC + "人")
        return
    

    #获取重高线：在一份一段表中，累计人数达到第二批所有需要通过考试录取的名额总数时，对应的分数即为重点线
    def getPrivilegeScoreGate(self, schoolStats):
        secondRoundStuQuota = schoolStats.getSecondRoundStuQuota()
        dfScoreCountTemp = self.dfScoreCounts[self.dfScoreCounts["累计"] >= secondRoundStuQuota]
        
        self.privilegeScoreGate = dfScoreCountTemp["分数"].max()
        return self.privilegeScoreGate
    

    def displayPrivilegeScoreGate(self):
        print("\n")
        print("本次中考5+2区域省级示范性普高指导线为：" + GlobalConfig.bcolors.YELLO + "{}".format(self.privilegeScoreGate) + GlobalConfig.bcolors.ENDC)


    def trimDownStudents(self):
        dfTemp = self.dfStudents.copy()
        dfTemp = dfTemp.sort_values(by='总分', ascending=False)

        #去掉省重线以下的学生：
        dfTemp = dfTemp[dfTemp["总分"] >= self.privilegeScoreGate]

        #去掉统招生中，拿到市指标的学生:
        myName = "{}{}".format(self.myName, self.myNameTag)
        dfStuWithCityQuota = dfTemp[(dfTemp["姓名"] != myName) & (dfTemp["类型"] == "统招")].sample(n=GlobalConfig.CityQuotaTotal)
        dfTemp.drop(dfStuWithCityQuota.index, inplace=True)

        #去掉艺体生：
        dfTalentStudentQuota = dfTemp[(dfTemp["姓名"] != myName)].sample(n=GlobalConfig.TalentQuotaTotal)
        dfTemp.drop(dfTalentStudentQuota.index, inplace=True)


        self.dfStuForSecondRound = dfTemp.copy()
        self.stuForSecondRoundNum = self.dfStuForSecondRound.shape[0]
        return