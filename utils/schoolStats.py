import pandas as pd
from tabulate import tabulate
from scipy import stats

import config.config as GlobalConfig

class SchoolStats:
    def __init__(self):
        self.dfSchools = pd.read_excel('data/schools.2023.xlsx', dtype={"学校代码": str})

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
        return
    

    def getSecondRoundStuQuota(self):
        return self.numSecondRoundStuQuota
    

    #返回一个精简的学校信息，便于打印：
    def briefSchoolInfo(self, dfShoolInfo):
        return dfShoolInfo[["学校代码", "学校名称", "公办民办", "录取位次", "录取分数线", "录取平均分"]]
    

    #根据分数排名，给出推荐填报学校：
    def recommendSchool(self, scoreRank):
        #找到录取位次大于等于scoreRank，并且与之最接近的学校：
        dfClosestSchool = self.dfSchools[self.dfSchools["录取位次"] >= scoreRank]
        dfClosestSchool = dfClosestSchool[dfClosestSchool["录取位次"] == dfClosestSchool.iloc[0]["录取位次"]]
        

        #找到比最接近学校高的五个学校：
        dfHigherSchool = self.dfSchools[self.dfSchools["录取位次"] < dfClosestSchool["录取位次"].values[0]]
        if(len(dfHigherSchool) < 5):
            dfHigherSchool = dfHigherSchool.tail(len(dfHigherSchool)) 
        else:
            dfHigherSchool = dfHigherSchool.tail(5)
       

        #找到比最接近学校低的八个学校：
        dfLowerSchool = self.dfSchools[self.dfSchools["录取位次"] > dfClosestSchool["录取位次"].values[0]]
        if(len(dfLowerSchool) < 8):
            dfLowerSchool = dfLowerSchool.head(len(dfLowerSchool)) 
        else:
            dfLowerSchool = dfLowerSchool.head(8)


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

        print("\n")
        print(GlobalConfig.bcolors.CYAN + "低段学校：")
        print(GlobalConfig.bcolors.CYAN + tabulate(self.briefSchoolInfo(dictRecommendSchool["low"]), showindex="never", headers="keys", tablefmt="heavy_outline") + GlobalConfig.bcolors.ENDC)
        return

        