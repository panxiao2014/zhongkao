from progress.spinner import LineSpinner
import pandas as pd

import config.config as GlobalConfig

class SchoolApply:
    def __init__(self, stuSet, schoolStats):
        self.stuSet = stuSet
        self.schoolStats = schoolStats
        self.dfStuForSecondRound = stuSet.dfStuForSecondRound
        self.dfSchools = schoolStats.dfSchools
        self.myName = stuSet.myName
        self.myNameTag = stuSet.myNameTag
        self.privilegeScoreGate = stuSet.privilegeScoreGate
        return
    

    def applySchoolForEachStudent(self, stuData, scoreRank, recommendSchools):
        #统招还是调剂：
        stuType = stuData["类型"]

        numSchoolFilled = 0
        dfMediumSchool = recommendSchools["medium"]
        dfLowShool = recommendSchools["low"]
        while(numSchoolFilled < GlobalConfig.NumShoolToApply):
            #调剂生只能填2，4， 6志愿：
            if(stuType == "调剂" and (numSchoolFilled % 2 == 0)):
                stuData[GlobalConfig.OrderMap[numSchoolFilled]] = "None"
                numSchoolFilled += 1
                continue

            if(len(dfMediumSchool) != 0):
                stuData[GlobalConfig.OrderMap[numSchoolFilled]] = dfMediumSchool.iloc[0][ "学校代码"]
                dfMediumSchool = dfMediumSchool.iloc[1:]
                numSchoolFilled += 1
                continue

            if(len(dfLowShool) != 0):
                stuData[GlobalConfig.OrderMap[numSchoolFilled]] = dfLowShool.iloc[0][ "学校代码"]
                dfLowShool = dfLowShool.iloc[1:]
                numSchoolFilled += 1
                continue
        return

    

    #为每个分数段的学生填报志愿：
    def applySchoolForStudents(self, score):
        dfStudents = self.dfStuForSecondRound[self.dfStuForSecondRound["总分"] == score]
        if(len(dfStudents) == 0):
            return
        
        scoreRank = self.stuSet.getScoreRank(score)
        recommendSchools = self.schoolStats.recommendSchool(scoreRank)

        for index, row in dfStudents.iterrows():
            self.applySchoolForEachStudent(row, scoreRank, recommendSchools)
        return
    

    #学生填报志愿:
    def coreProcess(self):
        #我的志愿已经填报，先把自己从df中移除：
        myData = self.dfStuForSecondRound.loc[self.dfStuForSecondRound["姓名"] == (self.myName + self.myNameTag)].copy()
        self.dfStuForSecondRound = self.dfStuForSecondRound[self.dfStuForSecondRound["姓名"] != (self.myName + self.myNameTag)]

        print("\n")
        bar = LineSpinner('同学们填报志愿中，请稍后。。。')

        #从高分到普高线分数，依次填报志愿：
        for i in range(GlobalConfig.ScoreFull, self.privilegeScoreGate-1, -1):
            self.applySchoolForStudents(i)
            bar.next()

        #将我重新加回df:
        self.dfStuForSecondRound = pd.concat([self.dfStuForSecondRound, myData])
        return