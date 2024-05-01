from tabulate import tabulate

import config.config as GlobalConfig

class ApplyStrategySet:
    def __init__(self, stuSet, schoolStats, dfStuForSecondRound):
        self.stuSet = stuSet
        self.schoolStats = schoolStats
        self.dfStuForSecondRound = dfStuForSecondRound
        self.strategyStats = {"大众型": {"使用次数": 0, "录取人数": 0, "得分": 0, "有效指数": 0},
                              "进取型": {"使用次数": 0, "录取人数": 0,  "得分": 0, "有效指数": 0},
                              "保守型": {"使用次数": 0, "录取人数": 0,  "得分": 0, "有效指数": 0},
                              "进取土豪型": {"使用次数": 0, "录取人数": 0,  "得分": 0, "有效指数": 0},
                              "保守土豪型": {"使用次数": 0, "录取人数": 0,  "得分": 0, "有效指数": 0}}
        
        #越在前面志愿录取的，得分越高：
        self.strategyPoints = {}
        for i in range(0, GlobalConfig.NumShoolToApply):
            self.strategyPoints[GlobalConfig.OrderMap[i]] = 7-i
        return
    

    #大众型
    def strategyModerate(self, index, scoreRank, recommendSchools):
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
        
        self.strategyStats["大众型"]["使用次数"] += 1
        self.dfStuForSecondRound.at[index, "选取策略"] = "大众型"
        return
    

    def applySchool(self, index, scoreRank, recommendSchools):
        self.strategyModerate(index, scoreRank, recommendSchools)
        return
    

    #更新策略统计结果：
    def updateStrategyStats(self, dfAdmittedStudents):
        strategyGroupSize = dfAdmittedStudents.groupby("选取策略").size()
        for index, row in strategyGroupSize.items():
            self.strategyStats[index]["录取人数"] = row

        #更新各策略得分:
        strategyGroup = dfAdmittedStudents.groupby("选取策略")
        for strategy, dfStu in strategyGroup:
            orderGroup = dfStu.groupby("录取志愿").size()
            for index, row in orderGroup.items():
                points = row * self.strategyPoints[index]
                self.strategyStats[strategy]["得分"] += points
                print("{}: {}, points {}".format(index, row, points))
            
            self.strategyStats[strategy]["有效指数"] = round(self.strategyStats[strategy]["得分"] / self.strategyStats[strategy]["使用次数"] * 100 / GlobalConfig.NumShoolToApply, 1)
            
        return
    

    #展示策略使用统计：
    def showStrategyStats(self):
        statsList = [[key, value["使用次数"], value["录取人数"], value["有效指数"]] for key, value in self.strategyStats.items()]
        print(GlobalConfig.bcolors.CYAN + tabulate(statsList, showindex="never", headers=["策略", "使用次数", "录取人数", "有效指数"], tablefmt="rounded_grid") + GlobalConfig.bcolors.ENDC)
        print("\n")
        print(GlobalConfig.bcolors.CYAN + "(*注： 有效指数为加权得分。第一志愿录取得分最高，其他志愿录取得分依次减低。指数满分为100)" + GlobalConfig.bcolors.ENDC)
        return