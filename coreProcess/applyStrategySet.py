import random
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
    def strategyModerate1(self, index, scoreRank, recommendSchools):
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
    

    #大众型
    def strategyModerate(self, index, stuType, scoreRank, recommendSchools, dfMediumSchoolPublic):
        mediumSchoolCode = dfMediumSchoolPublic["学校代码"].values[0]
        lstLowSchoolCode = ["", "", ""]

        dfLowSchool = recommendSchools["low"]
        dfLowSchoolPublic = dfLowSchool[dfLowSchool["公办民办"] == "公办"]

        #查看低段公办学校推荐名单里包含了多少不同录取位次的学校：
        lowSchoolGroup = dfLowSchoolPublic.groupby('录取位次')
        lowSchoolGroupSize = lowSchoolGroup.size()

        if(lowSchoolGroupSize >= 3):
            lstItem = 0
            for admitRank, group in lowSchoolGroup:
                lstLowSchoolCode[lstItem] = group.sample(n = 1)["学校代码"].values[0]
                lstItem += 1
                if(lstItem == 3):
                    break
        elif(lowSchoolGroupSize == 1):
            dfLowSchoolPublic = dfLowSchoolPublic.sample(n = 3)
            lstItem = 0
            for index, row in dfLowSchoolPublic.iterrows():
                lstLowSchoolCode[lstItem] = row["学校代码"]
                lstItem += 1
        else:
            #如果低段公办学校只有两种不同的录取位次，则要从一种中选出两所学校，另一种中选出一所：
            lstItem = 0
            for admitRank, group in lowSchoolGroup:
                if(lstItem == 3):
                    break

                if(len(group) >= 2):
                    for index, row in group.sample(n = 2).iterrows():
                        lstLowSchoolCode[lstItem] = row["学校代码"]
                        lstItem += 1
                        if(lstItem == 3):
                            break
                else:
                    lstLowSchoolCode[lstItem] = group["学校代码"].values[0]
                    lstItem += 1
                    if(lstItem == 3):
                        break

        if(stuType == "统招"):
            self.dfStuForSecondRound.at[index, GlobalConfig.OrderMap[0]] = mediumSchoolCode
            self.dfStuForSecondRound.at[index, GlobalConfig.OrderMap[1]] = mediumSchoolCode
            self.dfStuForSecondRound.at[index, GlobalConfig.OrderMap[2]] = lstLowSchoolCode[0]
            self.dfStuForSecondRound.at[index, GlobalConfig.OrderMap[3]] = lstLowSchoolCode[0]
            self.dfStuForSecondRound.at[index, GlobalConfig.OrderMap[4]] = lstLowSchoolCode[1]
            self.dfStuForSecondRound.at[index, GlobalConfig.OrderMap[5]] = lstLowSchoolCode[1]
            self.dfStuForSecondRound.at[index, GlobalConfig.OrderMap[6]] = lstLowSchoolCode[2]
        else:
            self.dfStuForSecondRound.at[index, GlobalConfig.OrderMap[0]] = "None"
            self.dfStuForSecondRound.at[index, GlobalConfig.OrderMap[1]] = mediumSchoolCode
            self.dfStuForSecondRound.at[index, GlobalConfig.OrderMap[2]] = "None"
            self.dfStuForSecondRound.at[index, GlobalConfig.OrderMap[3]] = lstLowSchoolCode[0]
            self.dfStuForSecondRound.at[index, GlobalConfig.OrderMap[4]] = "None"
            self.dfStuForSecondRound.at[index, GlobalConfig.OrderMap[5]] = lstLowSchoolCode[1]
            self.dfStuForSecondRound.at[index, GlobalConfig.OrderMap[6]] = "None"   

        
        self.strategyStats["大众型"]["使用次数"] += 1
        self.dfStuForSecondRound.at[index, "选取策略"] = "大众型"
        return
    

    #进取型：
    def strategyAgressive(self, index, stuType, scoreRank, recommendSchools, dfHighSchoolPublic, dfMediumSchoolPublic):
        highSchoolCode = dfHighSchoolPublic["学校代码"].values[0]
        mediumSchoolCode = dfMediumSchoolPublic["学校代码"].values[0]

        dfLowSchool = recommendSchools["low"]
        dfLowSchoolPublic = dfLowSchool[dfLowSchool["公办民办"] == "公办"]

        return
    

    def applySchool(self, index, scoreRank, recommendSchools):
        #统招还是调剂：
        stuType = self.dfStuForSecondRound.at[index, "类型"]

        dfMediumSchool = recommendSchools["medium"]
        dfMediumSchoolPublic = dfMediumSchool[dfMediumSchool["公办民办"] == "公办"].sample(n = 1)

        dfHighSchool = recommendSchools["high"]
        if(len(dfHighSchool) != 0):
            dfHighSchoolPublic = dfHighSchool[dfHighSchool["公办民办"] == "公办"]
            if(len(dfHighSchoolPublic) != 0):
                dfHighSchoolPublic = dfHighSchoolPublic.sample(n = 1)
                gap = (scoreRank - dfHighSchoolPublic["录取位次"].values[0]) / dfHighSchoolPublic["第二批次招收名额"].values[0]
                if(gap <= GlobalConfig.StrategyHighGap):
                    tossCoin = random.randint(1, 100)
                    if(tossCoin <= GlobalConfig.StrategyHighPercent):
                        isRich = random.randint(0, 1)
                        if(isRich == 1):
                            pass
                            #self.strategyAgressiveRich(index, scoreRank, recommendSchools)
                        else:
                            pass
                            self.strategyAgressive(index, stuType, scoreRank, recommendSchools, dfHighSchoolPublic, dfMediumSchoolPublic)
                            return


        self.strategyModerate(index, stuType, scoreRank, recommendSchools, dfMediumSchoolPublic)
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