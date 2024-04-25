class StudentDispatch:
    def __init__(self, stuSet, schoolStats):
        self.stuSet = stuSet
        self.schoolStats = schoolStats
        self.dfStuForSecondRound = stuSet.dfStuForSecondRound
        self.dfSchools = schoolStats.dfSchools
        self.myName = stuSet.myName
        self.myNameTag = stuSet.myNameTag
        return
    

    def setupSchoolQuota(self):
        self.dfSchools["录取余额"] = self.dfSchools.apply(lambda row: row['5+2区域计划'] - row['指标到校'] - row["民办校内指标到校"] - row["全市艺体"], axis=1)
        print(self.dfSchools["录取余额"].sum())
        return
    

    def studentDispatch(self):
        return
    

    def coreProcess(self):
        return