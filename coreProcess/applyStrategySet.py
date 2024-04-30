import config.config as GlobalConfig

class ApplyStrategySet:
    def __init__(self, stuSet, schoolStats, dfStuForSecondRound):
        self.stuSet = stuSet
        self.schoolStats = schoolStats
        self.dfStuForSecondRound = dfStuForSecondRound
        return
    

    def applySchool(self, index, scoreRank, recommendSchools):
        #统招还是调剂：
        stuType = self.dfStuForSecondRound.at[index, "类型"]

        numSchoolFilled = 0
        dfMediumSchool = recommendSchools["medium"]
        dfLowShool = recommendSchools["low"]
        while(numSchoolFilled < GlobalConfig.NumShoolToApply):
            #调剂生只能填2，4， 6志愿：
            if(stuType == "调剂" and (numSchoolFilled % 2 == 0)):
                self.dfStuForSecondRound.at[index, GlobalConfig.OrderMap[numSchoolFilled]] = "None"
                numSchoolFilled += 1
                continue

            if(len(dfMediumSchool) != 0):
                self.dfStuForSecondRound.at[index, GlobalConfig.OrderMap[numSchoolFilled]] = dfMediumSchool.iloc[0][ "学校代码"]
                dfMediumSchool = dfMediumSchool.iloc[1:]
                numSchoolFilled += 1
                continue

            if(len(dfLowShool) != 0):
                self.dfStuForSecondRound.at[index, GlobalConfig.OrderMap[numSchoolFilled]] = dfLowShool.iloc[0][ "学校代码"]
                dfLowShool = dfLowShool.iloc[1:]
                numSchoolFilled += 1
                continue
        return