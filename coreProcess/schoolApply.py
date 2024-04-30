from progress.spinner import LineSpinner
import pandas as pd

import config.config as GlobalConfig
from coreProcess.applyStrategySet import ApplyStrategySet

class SchoolApply:
    def __init__(self, stuSet, schoolStats):
        self.stuSet = stuSet
        self.schoolStats = schoolStats
        self.dfStuForSecondRound = stuSet.dfStuForSecondRound
        self.dfSchools = schoolStats.dfSchools
        self.myName = stuSet.myName
        self.myNameTag = stuSet.myNameTag
        self.privilegeScoreGate = stuSet.privilegeScoreGate
        self.applyStrategySet = None
        return
    

    def applySchoolForEachStudent(self, index, scoreRank, recommendSchools):
        self.applyStrategySet.applySchool(index, scoreRank, recommendSchools)
        return

    

    #为每个分数段的学生填报志愿：
    def applySchoolForStudents(self, score):
        dfStudents = self.dfStuForSecondRound[self.dfStuForSecondRound["总分"] == score]
        if(len(dfStudents) == 0):
            return
        
        scoreRank = self.stuSet.getScoreRank(score)
        recommendSchools = self.schoolStats.recommendSchool(scoreRank)

        for index, row in dfStudents.iterrows():
            self.applySchoolForEachStudent(index, scoreRank, recommendSchools)
        return
    

    #学生填报志愿:
    def coreProcess(self):
        #我的志愿已经填报，先把自己从df中移除：
        dfMyData = self.dfStuForSecondRound.loc[self.dfStuForSecondRound["姓名"] == (self.myName + self.myNameTag)].copy()
        self.dfStuForSecondRound = self.dfStuForSecondRound[self.dfStuForSecondRound["姓名"] != (self.myName + self.myNameTag)]
        self.applyStrategySet = ApplyStrategySet(self.stuSet, self.schoolStats, self.dfStuForSecondRound)

        print("\n")
        bar = LineSpinner('同学们填报志愿中，请稍后。。。')

        #从高分到普高线分数，依次填报志愿：
        for i in range(GlobalConfig.ScoreFull, self.privilegeScoreGate-1, -1):
            self.applySchoolForStudents(i)
            bar.next()

        #将我重新加回df:
        self.dfStuForSecondRound = pd.concat([self.dfStuForSecondRound, dfMyData])
        self.stuSet.dfStuForSecondRound = self.dfStuForSecondRound
        return