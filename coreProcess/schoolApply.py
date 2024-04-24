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
    

    #为每个分数段的学生填报志愿：
    def applySchoolForStudents(self, score):
        dfStudents = self.dfStuForSecondRound[self.dfStuForSecondRound["总分"] == score]
        if(len(dfStudents) == 0):
            return
        
        recommendSchools = self.schoolStats.recommendSchool(self.stuSet.getScoreRank(score))
        return
    

    #每个学生填报志愿:
    def coreProcess(self):
        #我的志愿已经填报，先把自己从df中移除：
        myData = self.dfStuForSecondRound.loc[self.dfStuForSecondRound["姓名"] == (self.myName + self.myNameTag)].copy()
        self.dfStuForSecondRound = self.dfStuForSecondRound[self.dfStuForSecondRound["姓名"] != (self.myName + self.myNameTag)]

        #从高分到普高线分数，依次填报志愿：
        for i in range(GlobalConfig.ScoreFull, self.privilegeScoreGate-1, -1):
            self.applySchoolForStudents(i)

        return