import pandas as pd
from tabulate import tabulate
from scipy import stats
import warnings

import config.config as GlobalConfig

class SchoolStats:
    def __init__(self):
        warnings.simplefilter(action='ignore', category=UserWarning)
        self.dfSchools = pd.read_excel('data/schools.2023.xlsx', dtype={"学校代码": str})
        warnings.resetwarnings()

        #第二批次所有需要通过考试录取的学生总数。包括：
        #市直属普高，公办：计划招生数
        #5+2普高，公办：计划招生数 - 指标到校数
        #民办：计划招生数 - 民办校内指标到校
        self.numSecondRoundStuQuota = 0
        return
    

    def setupStats(self):
        dfCityPublic = self.dfSchools[(self.dfSchools["公办民办"]=="公办") & (self.dfSchools["学校性质"]=="市直属普高") & (self.dfSchools["级别"]=="省级示范")]
        sumStu1 = dfCityPublic["5+2区域计划"].sum()
        
        dfNormalPublic = self.dfSchools[(self.dfSchools["公办民办"]=="公办") & (self.dfSchools["学校性质"]=="5+2普高") & (self.dfSchools["级别"]=="省级示范")]
        sumStu2 = dfNormalPublic["5+2区域计划"].sum() - dfNormalPublic["指标到校"].sum()
        
        dfNormalPrivate = self.dfSchools[(self.dfSchools["公办民办"]=="民办") & (self.dfSchools["级别"]=="省级示范")]
        sumStu3 = dfNormalPrivate["5+2区域计划"].sum() - dfNormalPrivate["民办校内指标到校"].sum()
        
        self.numSecondRoundStuQuota = sumStu1 + sumStu2 + sumStu3

        #根据学校的录取位次排序：
        self.dfSchools = self.dfSchools.sort_values(by="录取位次", ascending=True)

        #去掉没有录取位次记录的学校：
        self.dfSchools = self.dfSchools[self.dfSchools["录取位次"] != 0]

        GlobalConfig.LstSchoolCode = self.dfSchools["学校代码"].tolist()
        return
    

    def getSecondRoundStuQuota(self):
        return self.numSecondRoundStuQuota
    

    #返回一个精简的学校信息，便于打印：
    def briefSchoolInfo(self, dfShoolInfo):
        return dfShoolInfo[["学校代码", "学校名称", "公办民办", "录取位次", "录取分数线", "录取平均分"]]
    

    #根据分数排名，给出推荐填报学校：
    def recommendSchool(self, scoreRank):
        #推荐高段学校数：
        numRecommendHigh = 3
        #推荐低段学校数：
        numRecommendLow = 7

        #找到录取位次大于等于scoreRank，并且与之最接近的学校：
        dfClosestSchool = self.dfSchools[self.dfSchools["录取位次"] >= scoreRank]

        #由于公布数据的一些差异，有可能有低分的排名已经超过了可查学校录取数据的最高录取位次，此时直接返回录取位次排名倒数的10个学校：
        if(len(dfClosestSchool) == 0):
            dfClosestSchool = self.dfSchools.tail(10)
            return {"high": pd.DataFrame(), "medium": dfClosestSchool, "low": pd.DataFrame()}
        
        dfClosestSchool = dfClosestSchool[dfClosestSchool["录取位次"] == dfClosestSchool.iloc[0]["录取位次"]]
        

        #找到比最接近学校高的学校：
        dfHigherSchool = self.dfSchools[self.dfSchools["录取位次"] < dfClosestSchool["录取位次"].values[0]]
        if(len(dfHigherSchool) < numRecommendHigh):
            dfHigherSchool = dfHigherSchool.tail(len(dfHigherSchool)) 
        else:
            dfHigherSchool = dfHigherSchool.tail(numRecommendHigh)
       

        #找到比最接近学校低的学校：
        dfLowerSchool = self.dfSchools[self.dfSchools["录取位次"] > dfClosestSchool["录取位次"].values[0]]
        if(len(dfLowerSchool) < numRecommendLow):
            dfLowerSchool = dfLowerSchool.head(len(dfLowerSchool)) 
        else:
            dfLowerSchool = dfLowerSchool.head(numRecommendLow)


        return {"high": dfHigherSchool, "medium": dfClosestSchool, "low": dfLowerSchool}
    

    #显示推荐填报学校：
    def displayRecommendSchool(self, dictRecommendSchool):
        if(len(dictRecommendSchool["high"]) != 0):
            print("\n")
            print(GlobalConfig.bcolors.PINK + "高段学校：" + GlobalConfig.bcolors.ENDC)
            print(GlobalConfig.bcolors.PINK + tabulate(self.briefSchoolInfo(dictRecommendSchool["high"]), showindex="never", headers="keys", tablefmt="heavy_outline") + GlobalConfig.bcolors.ENDC)

        print("\n")
        print(GlobalConfig.bcolors.BLUE + "匹配学校：" + GlobalConfig.bcolors.ENDC)
        print(GlobalConfig.bcolors.BLUE + tabulate(self.briefSchoolInfo(dictRecommendSchool["medium"]), showindex="never", headers="keys", tablefmt="heavy_outline") + GlobalConfig.bcolors.ENDC)

        if(len(dictRecommendSchool["low"]) != 0):
            print("\n")
            print(GlobalConfig.bcolors.CYAN + "低段学校：")
            print(GlobalConfig.bcolors.CYAN + tabulate(self.briefSchoolInfo(dictRecommendSchool["low"]), showindex="never", headers="keys", tablefmt="heavy_outline") + GlobalConfig.bcolors.ENDC)
        return
    

    #显示自己填报的七个志愿：
    def displaySchoolApplied(self, dictShoolApplied):
        applyTable =[]
        for key, value in dictShoolApplied.items():
            shoolName = self.dfSchools[self.dfSchools["学校代码"]==value]["学校名称"].iloc[0]
            applyTable.append([key, value, shoolName])

        print("\n")
        print("您填报的志愿如下：")
        print(GlobalConfig.bcolors.YELLO + tabulate(applyTable, showindex="never", tablefmt="heavy_grid") + GlobalConfig.bcolors.ENDC)
        return

        