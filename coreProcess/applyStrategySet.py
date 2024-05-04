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
    

    #将选取的学校进行填报，并更新策略统计：
    def fillShoolCode(self, stuIndex, stuType, lstSchoolCode, strStrategy):
        if(stuType == "统招"):
            self.dfStuForSecondRound.at[stuIndex, GlobalConfig.OrderMap[0]] = lstSchoolCode[0]
            self.dfStuForSecondRound.at[stuIndex, GlobalConfig.OrderMap[1]] = lstSchoolCode[0]
            self.dfStuForSecondRound.at[stuIndex, GlobalConfig.OrderMap[2]] = lstSchoolCode[1]
            self.dfStuForSecondRound.at[stuIndex, GlobalConfig.OrderMap[3]] = lstSchoolCode[1]
            self.dfStuForSecondRound.at[stuIndex, GlobalConfig.OrderMap[4]] = lstSchoolCode[2]
            self.dfStuForSecondRound.at[stuIndex, GlobalConfig.OrderMap[5]] = lstSchoolCode[2]
            self.dfStuForSecondRound.at[stuIndex, GlobalConfig.OrderMap[6]] = lstSchoolCode[3]
        else:
            self.dfStuForSecondRound.at[stuIndex, GlobalConfig.OrderMap[0]] = "None"
            self.dfStuForSecondRound.at[stuIndex, GlobalConfig.OrderMap[1]] = lstSchoolCode[0]
            self.dfStuForSecondRound.at[stuIndex, GlobalConfig.OrderMap[2]] = "None"
            self.dfStuForSecondRound.at[stuIndex, GlobalConfig.OrderMap[3]] = lstSchoolCode[1]
            self.dfStuForSecondRound.at[stuIndex, GlobalConfig.OrderMap[4]] = "None"
            self.dfStuForSecondRound.at[stuIndex, GlobalConfig.OrderMap[5]] = lstSchoolCode[2]
            self.dfStuForSecondRound.at[stuIndex, GlobalConfig.OrderMap[6]] = "None"
        
        self.strategyStats[strStrategy]["使用次数"] += 1
        self.dfStuForSecondRound.at[stuIndex, "选取策略"] = strStrategy
        return      
    

    #大众型
    def strategyModerate(self, stuIndex, stuType, recommendSchools):
        lstSchoolCode = ["", "", "", ""]
        lstSchoolCodeLen = len(lstSchoolCode)
        schoolChosen = 0

        dfSchoolMedium = recommendSchools["公办"]["medium"]
        dfSchoolLow = recommendSchools["公办"]["low"]

        if(len(dfSchoolLow) == 0):
            #没有低段学校推荐，则在匹配段直接选出四个学校：
            dfSchoolMedium = dfSchoolMedium.sample(n = lstSchoolCodeLen)
            schoolChosen = 0
            for index, row in dfSchoolMedium.iterrows():
                lstSchoolCode[schoolChosen] = row["学校代码"]
                schoolChosen += 1
        else:
            dfSchoolMedium = dfSchoolMedium.sample(n = 1)
            lstSchoolCode[0] = dfSchoolMedium.iloc[0]["学校代码"]
            schoolChosen += 1

            lowSchoolGroup = dfSchoolLow.groupby("录取位次")
            lowSchoolGroupSize = lowSchoolGroup.ngroups

            #根据low school有多少不同段位的学校，决定3到7志愿从各段位选取多少学校来填写：
            dictLowSchoolFillPolicy = {1: [3], 2: [1, 2], 3: [1, 1, 1], 4: [1, 1, 1]}
            lstLowSchoolFill = dictLowSchoolFillPolicy[lowSchoolGroupSize]

            lstLowSchoolFillIndex = 0
            for schoolRank, group in lowSchoolGroup:
                dfSchool = group.sample(n = lstLowSchoolFill[lstLowSchoolFillIndex])
                for index, row in dfSchool.iterrows():
                    lstSchoolCode[schoolChosen] = row["学校代码"]
                    schoolChosen += 1
                        
                lstLowSchoolFillIndex += 1
                if(schoolChosen == lstSchoolCodeLen):
                    break

        self.fillShoolCode(stuIndex, stuType, lstSchoolCode, "大众型")
        return
    

    #进取型：
    def strategyAgressive(self, stuIndex, stuType, scoreRank, recommendSchools, dfHighSchoolPublic):
        lstSchoolCode = ["", "", "", ""]
        lstSchoolCodeLen = len(lstSchoolCode)
        schoolChosen = 0

        #选取高位公办学校：
        lstSchoolCode[0] = dfHighSchoolPublic.sample(n = 1).iloc[0]["学校代码"]
        schoolChosen += 1

        dfSchoolMedium = recommendSchools["公办"]["medium"]
        dfSchoolLow = recommendSchools["公办"]["low"]

        if(len(dfSchoolLow) == 0):
            dfSchoolMedium = dfSchoolMedium.sample(n = lstSchoolCodeLen-1)
            for index, row in dfSchoolMedium.iterrows():
                lstSchoolCode[schoolChosen] = row["学校代码"]
                schoolChosen += 1
        else:
            dfSchoolMedium = dfSchoolMedium.sample(n = 1)
            lstSchoolCode[1] = dfSchoolMedium.iloc[0]["学校代码"]
            schoolChosen += 1

            lowSchoolGroup = dfSchoolLow.groupby("录取位次")
            lowSchoolGroupSize = lowSchoolGroup.ngroups

            #根据low school有多少不同段位的学校，决定3到7志愿从各段位选取多少学校来填写：
            dictLowSchoolFillPolicy = {1: [2], 2: [1, 1], 3: [1, 1], 4: [1, 1]}
            lstLowSchoolFill = dictLowSchoolFillPolicy[lowSchoolGroupSize]

            lstLowSchoolFillIndex = 0
            for schoolRank, group in lowSchoolGroup:
                dfSchool = group.sample(n = lstLowSchoolFill[lstLowSchoolFillIndex])
                for index, row in dfSchool.iterrows():
                    lstSchoolCode[schoolChosen] = row["学校代码"]
                    schoolChosen += 1
                        
                lstLowSchoolFillIndex += 1
                if(schoolChosen == lstSchoolCodeLen):
                    break

        self.fillShoolCode(stuIndex, stuType, lstSchoolCode, "进取型")
        return
    

    #进取土豪型：
    def strategyAgressiveRich(self, stuIndex, stuType, scoreRank, recommendSchools, dfHighSchoolPublic):
        lstSchoolCode = ["", "", "", ""]
        lstSchoolCodeLen = len(lstSchoolCode)
        schoolChosen = 0

        dfHighSchoolPrivate = recommendSchools["民办"]["high"]
        #如果高段有民办，则选民办，否则选公立:
        if(len(dfHighSchoolPrivate) != 0):
            lstSchoolCode[0] = dfHighSchoolPrivate.sample(n = 1).iloc[0]["学校代码"]
        else:
            lstSchoolCode[0] = dfHighSchoolPublic.sample(n = 1).iloc[0]["学校代码"]
        schoolChosen += 1

        dfSchoolMediumPublic = recommendSchools["公办"]["medium"]
        dfSchoolMediumPrivate = recommendSchools["民办"]["medium"]
        dfSchoolLowPublic = recommendSchools["公办"]["low"]
        dfSchoolLowPrivate = recommendSchools["民办"]["low"]

        if(len(dfSchoolLowPublic) == 0):
            #如果没有低段学校，则中段选取一个民办，两个公办：
            lstSchoolCode[schoolChosen] = dfSchoolMediumPrivate.sample(n = 1).iloc[0]["学校代码"]
            schoolChosen += 1

            dfSchoolMediumPublic = dfSchoolMediumPublic.sample(n = 2)
            for index, row in dfSchoolMediumPublic.iterrows():
                lstSchoolCode[schoolChosen] = row["学校代码"]
                schoolChosen += 1
        else:
            #如果有低段学校，则中段选一个公办，低段选一个公办，一个民办：
            lstSchoolCode[schoolChosen] = dfSchoolMediumPublic.sample(n = 1).iloc[0]["学校代码"]
            schoolChosen += 1

            lstSchoolCode[schoolChosen] = dfSchoolLowPublic.sample(n = 1).iloc[0]["学校代码"]
            schoolChosen += 1

            lstSchoolCode[schoolChosen] = dfSchoolLowPrivate.sample(n = 1).iloc[0]["学校代码"]
            schoolChosen += 1

        print("{}: {}".format(scoreRank, lstSchoolCode))

        self.fillShoolCode(stuIndex, stuType, lstSchoolCode, "进取土豪型")
        return
    

    def applySchool(self, index, scoreRank, recommendSchools):
        #统招还是调剂：
        stuType = self.dfStuForSecondRound.at[index, "类型"]

        dictSchoolPublic = recommendSchools["公办"]
        dictSchoolPrivate = recommendSchools["民办"]

        #如果有高段公办学校，则有可能选择进取型：
        dfHighSchoolPublic = dictSchoolPublic["high"]
        if(len(dfHighSchoolPublic) != 0):
            gap = (scoreRank - dfHighSchoolPublic["录取位次"].values[0]) / dfHighSchoolPublic["第二批次招收名额"].values[0]
            if(gap <= GlobalConfig.StrategyHighGap):
                tossCoin = random.randint(1, 100)
                if(tossCoin <= GlobalConfig.StrategyHighPercent):
                    isRich = random.randint(0, 1)
                    if(isRich == 1):
                        self.strategyAgressiveRich(index, stuType, scoreRank, recommendSchools, dfHighSchoolPublic)
                    else:
                        self.strategyAgressive(index, stuType, scoreRank, recommendSchools, dfHighSchoolPublic)
                        return

        self.strategyModerate(index, stuType, recommendSchools)
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