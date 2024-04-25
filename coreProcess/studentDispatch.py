import config.config as GlobalConfig

class StudentDispatch:
    def __init__(self, stuSet, schoolStats):
        self.stuSet = stuSet
        self.schoolStats = schoolStats
        self.dfStuForSecondRound = stuSet.dfStuForSecondRound
        self.dfSchools = schoolStats.dfSchools
        self.myName = stuSet.myName
        self.myNameTag = stuSet.myNameTag
        self.numStudentsAdmitted = 0
        print(self.dfStuForSecondRound)
        return
    

    def setupSchoolQuota(self):
        self.dfSchools["统招余额"] = self.dfSchools.apply(lambda row: row['5+2区域统招'] - row['指标到校'] - row["民办校内指标到校"] - row["全市艺体"], axis=1)
        self.dfSchools["调剂余额"] = self.dfSchools.apply(lambda row: row['5+2区域调剂'], axis=1)
        return
    

    #对学生进行投档
    #score: 当前投档分数段
    #applyOrder： 第几志愿
    #school： 当前填报的学校
    #dfGroupedStudents: 在该分数段下，当前志愿里填写该学校的学生集
    def dispatchToSchoolWithApplyOrder(self, score, applyOrder, school, dfGroupedStudents):
        print("{} {} {}: {}".format(score, GlobalConfig.OrderMap[applyOrder], school, len(dfGroupedStudents)))
        self.numStudentsAdmitted += len(dfGroupedStudents)
        return
    

    def studentsDispatch(self, dfStudents, score):
        #从第一志愿开始依次投档：
        for i in range(0, GlobalConfig.NumShoolToApply):
            #按照该分数段该志愿下学生填报的学校归类处理：
            groupSchool = dfStudents.groupby(GlobalConfig.OrderMap[i])
            for school, dfGroupedStudents in groupSchool:
                print("{} {}: {}".format(score, school, len(dfGroupedStudents)))
                #self.dispatchToSchoolWithApplyOrder(score, i, school, dfGroupedStudents)
        return
    

    def coreProcess(self):
        dfStudentsToDispatch = self.dfStuForSecondRound.copy()
        #655分以上同学统一处理：
        dfTopStudents = dfStudentsToDispatch[dfStudentsToDispatch['总分'] >= GlobalConfig.ScoreTopGate]
        self.studentsDispatch(dfTopStudents, GlobalConfig.ScoreTopGate)

        #从高分到省重线分，依次投档：
        for i in range(GlobalConfig.ScoreTopGate-1, self.stuSet.privilegeScoreGate-1, -1):
            dfStudents = dfStudentsToDispatch[dfStudentsToDispatch['总分'] == i]
            self.studentsDispatch(dfStudents, i)

        print(self.numStudentsAdmitted)
        return