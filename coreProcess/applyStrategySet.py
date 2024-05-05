import random
import pandas as pd
from tabulate import tabulate

import config.config as GlobalConfig

#进取型策略里，填报高位学校的门限：
StrategyHighGap = 0.2
#符合进取条件的学生中，选择进取策略的比例：
StrategyHighPercent = 50
#总分排名高的学生不采取保守策略，只有低于一定排名的才采取保守：
StrategyLowRank = 300
#符合保守条件的学生中，选择保守策略的比例：
StrategyLowPercent = 50

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
    

    #进取土豪型：如果高位有民办，就填民办，否则填公立。其他志愿，选填一个民办
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
            dfSelectShools = pd.concat([dfSchoolMediumPublic.sample(n = 2), dfSchoolMediumPrivate.sample(n = 1)])
            dfSelectShools = dfSelectShools.sample(frac = 1)
            for index, row in dfSelectShools.iterrows():
                lstSchoolCode[schoolChosen] = row["学校代码"]
                schoolChosen += 1
        else:
            #如果有低段学校，则中段选一个公办，低段选一个公办，一个民办：
            lstSchoolCode[schoolChosen] = dfSchoolMediumPublic.sample(n = 1).iloc[0]["学校代码"]
            schoolChosen += 1

            lstLowSchool = ["", ""]
            publicGroup = dfSchoolLowPublic.groupby("录取位次")
            privateGroup = dfSchoolLowPrivate.groupby("录取位次")
            if(len(privateGroup) != 0):
                for rank, group in publicGroup:
                    lstLowSchool[0] = group.sample(n = 1).iloc[0]["学校代码"]
                    break

                privateGroup = dfSchoolLowPrivate.groupby("录取位次")
                for rank, group in privateGroup:
                    lstLowSchool[1] = group.sample(n = 1).iloc[0]["学校代码"]
                    break

                random.shuffle(lstLowSchool)
                lstSchoolCode[schoolChosen] = lstLowSchool[0]
                schoolChosen += 1
                lstSchoolCode[schoolChosen] = lstLowSchool[1]
            else:
                #低段没有民办，则选取两个公立
                dfSchoolLowPublic = dfSchoolLowPublic.sample(n = 2)
                for index, row  in dfSchoolLowPublic.iterrows():
                    lstSchoolCode[schoolChosen] = row["学校代码"]
                    schoolChosen += 1

        self.fillShoolCode(stuIndex, stuType, lstSchoolCode, "进取土豪型")
        return
    

    #保守型
    def strategyConservative(self, stuIndex, stuType, scoreRank, recommendSchools, dfLowSchoolPublic):
        lstSchoolCode = ["", "", "", ""]
        lstSchoolCodeLen = len(lstSchoolCode)
        schoolChosen = 0

        lowSchoolGroup = dfLowSchoolPublic.groupby("录取位次")
        lowSchoolGroupSize = lowSchoolGroup.ngroups

        #根据low school有多少不同段位的学校，决定7个志愿从各段位选取多少学校来填写：
        dictLowSchoolFillPolicy = {1: [4], 2: [1, 3], 3: [1, 1, 2], 4: [1, 1, 1, 1]}
        lstLowSchoolFill = dictLowSchoolFillPolicy[lowSchoolGroupSize]

        lstLowSchoolFillIndex = 0
        for schoolRank, group in lowSchoolGroup:
            dfSchool = group.sample(n = lstLowSchoolFill[lstLowSchoolFillIndex])
            for index, row in dfSchool.iterrows():
                lstSchoolCode[schoolChosen] = row["学校代码"]
                schoolChosen += 1

            lstLowSchoolFillIndex += 1

        self.fillShoolCode(stuIndex, stuType, lstSchoolCode, "保守型")
        return


    #保守土豪型：选一个公立，三个私立
    def strategyConservativeRich(self, stuIndex, stuType, scoreRank, recommendSchools, dfLowSchoolPublic, dfLowSchoolPrivate):
        lstSchoolCode = ["", "", "", ""]
        lstSchoolCodeLen = len(lstSchoolCode)
        schoolChosen = 0

        publicGroup = dfLowSchoolPublic.groupby("录取位次")
        for rank, group in publicGroup:
            lstSchoolCode[schoolChosen] = group.sample(n = 1).iloc[0]["学校代码"]
            schoolChosen += 1
            break

        lowSchoolGroup = dfLowSchoolPrivate.groupby("录取位次")
        lowSchoolGroupSize = lowSchoolGroup.ngroups

        #根据low school有多少不同段位的学校，决定7个志愿从各段位选取多少学校来填写：
        dictLowSchoolFillPolicy = {1: [3], 2: [1, 2], 3: [1, 1, 1], 4: [1, 1, 1]}
        lstLowSchoolFill = dictLowSchoolFillPolicy[lowSchoolGroupSize]

        lstLowSchoolFillIndex = 0
        for schoolRank, group in lowSchoolGroup:
            dfSchool = group.sample(n = lstLowSchoolFill[lstLowSchoolFillIndex])
            for index, row in dfSchool.iterrows():
                lstSchoolCode[schoolChosen] = row["学校代码"]
                schoolChosen += 1

                if(schoolChosen == lstSchoolCodeLen):
                    break

            if(schoolChosen == lstSchoolCodeLen):
                break
            lstLowSchoolFillIndex += 1

        self.fillShoolCode(stuIndex, stuType, lstSchoolCode, "保守土豪型")
        return           
    

    def applySchool(self, index, scoreRank, recommendSchools):
        #统招还是调剂：
        stuType = self.dfStuForSecondRound.at[index, "类型"]

        dictSchoolPublic = recommendSchools["公办"]
        dictSchoolPrivate = recommendSchools["民办"]

        dfHighSchoolPublic = dictSchoolPublic["high"]
        dfLowSchoolPublic = dictSchoolPublic["low"]

        #如果有高段公办学校，则有可能选择进取型：
        if(len(dfHighSchoolPublic) != 0):
            gap = (scoreRank - dfHighSchoolPublic["录取位次"].values[0]) / dfHighSchoolPublic["第二批次招收名额"].values[0]
            if(gap <= StrategyHighGap):
                tossCoin = random.randint(1, 100)
                if(tossCoin <= StrategyHighPercent):
                    isRich = random.randint(0, 1)
                    if(isRich == 1):
                        self.strategyAgressiveRich(index, stuType, scoreRank, recommendSchools, dfHighSchoolPublic)
                        return
                    else:
                        self.strategyAgressive(index, stuType, scoreRank, recommendSchools, dfHighSchoolPublic)
                        return
        
        #如果有低段公办学校，则有可能选择保守型：
        if(len(dfLowSchoolPublic) != 0 and scoreRank >= StrategyLowRank):
            tossCoin = random.randint(1, 100)
            if(tossCoin <= StrategyLowPercent):
                dfLowSchoolPrivate = dictSchoolPrivate["low"]
                if(len(dfLowSchoolPrivate) != 0):
                    #如果低段有民办，则有可能选择保守土豪型：
                    isRich = random.randint(0, 1)
                    if(isRich == 1):
                        self.strategyConservativeRich(index, stuType, scoreRank, recommendSchools, dfLowSchoolPublic, dfLowSchoolPrivate)
                        return
                    else:
                        self.strategyConservative(index, stuType, scoreRank, recommendSchools, dfLowSchoolPublic)
                        return
                else:
                    self.strategyConservative(index, stuType, scoreRank, recommendSchools, dfLowSchoolPublic)
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
            
            self.strategyStats[strategy]["有效指数"] = round(self.strategyStats[strategy]["得分"] / self.strategyStats[strategy]["使用次数"] * 100 / GlobalConfig.NumShoolToApply, 2)
            
        return
    

    #展示策略使用统计：
    def showStrategyStats(self):
        statsList = [[key, value["使用次数"], value["录取人数"], value["有效指数"]] for key, value in self.strategyStats.items()]
        print(GlobalConfig.bcolors.CYAN + tabulate(statsList, showindex="never", headers=["策略", "使用次数", "录取人数", "有效指数"], tablefmt="rounded_grid") + GlobalConfig.bcolors.ENDC)
        print("\n")
        print(GlobalConfig.bcolors.CYAN + "(*注： 有效指数为加权得分。第一志愿录取得分最高，其他志愿录取得分依次减低。指数满分为100)" + GlobalConfig.bcolors.ENDC)
        return