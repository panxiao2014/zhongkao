import pandas as pd
import numpy as np
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
        #按照2023年公布的省重线和一份一段表，重点线553对应的人数为14537
        self.numSecondRoundStuQuota = 14537
        return
    

    def setupStats(self):
        #根据学校的录取位次排序：
        self.dfSchools = self.dfSchools.sort_values(by="录取位次", ascending=True)

        #去掉没有录取位次记录的学校：
        self.dfSchools = self.dfSchools[self.dfSchools["录取位次"] != 0]

        #增加column用于跟踪投档名额：
        self.dfSchools["统招余额"] = self.dfSchools.apply(lambda row: row['5+2区域统招'] - row['指标到校'] - row["民办校内指标到校"] - row["全市艺体"], axis=1)
        self.dfSchools["调剂余额"] = self.dfSchools.apply(lambda row: row['5+2区域调剂'], axis=1)
        self.dfSchools["第二批次招收名额"] = self.dfSchools["统招余额"] + self.dfSchools["调剂余额"]

        GlobalConfig.LstSchoolCode = self.dfSchools["学校代码"].tolist()
        return
    

    def getSecondRoundStuQuota(self):
        return self.numSecondRoundStuQuota
    

    #返回一个精简的学校信息，便于打印：
    def briefSchoolInfo(self, dfShoolInfo):
        return dfShoolInfo[["学校代码", "学校名称", "公办民办", "录取位次", "录取分数线", "录取平均分", "投档等级"]]
    


    def getRecommendSchools_orig(self, scoreRank, dfSchools):
        dfLowSchool = pd.DataFrame()

        #根据2023录取结果，录取位次可以查到的最大值为14537，并且有超过20个学校都是这个值
        lowestAdmitRank = 14537

        #medium和low档次最多选四个不同录取位次的学校：
        maxShoolLevels = 4
        schoolLevel = 0

        #找到录取位次大于等于scoreRank的学校
        dfClosestSchool = dfSchools[dfSchools["录取位次"] >= scoreRank]

        #由于公布数据的一些差异，有可能有低分的排名已经超过了可查学校录取数据的最高录取位次，此时直接返回录取位次排名倒数的学校：
        if(len(dfClosestSchool) == 0):
            dfClosestSchool = dfSchools[dfSchools["录取位次"] == lowestAdmitRank]
            dfHigherSchool = dfSchools[dfSchools["录取位次"] < lowestAdmitRank].tail(1)
            return {"high": dfHigherSchool, "medium": dfClosestSchool, "low": dfLowSchool}
        
        #找到所有录取位次大于等于scoreRank的学校中，录取位次与scoreRank最接近的学校：
        dfClosestSchool = dfClosestSchool[dfClosestSchool["录取位次"] == dfClosestSchool.iloc[0]["录取位次"]]
        
        #找到比最接近学校排名低的学校：
        dfLowerSchool = dfSchools[dfSchools["录取位次"] > dfClosestSchool["录取位次"].values[0]]
        if(len(dfLowerSchool) != 0):
            groupShool = dfLowerSchool.groupby("录取位次")
            for admitRank, group in groupShool:
                dfLowSchool = pd.concat([dfLowSchool, group], ignore_index=True)
                schoolLevel += 1
                if(schoolLevel == maxShoolLevels):
                    break

        #找到比最接近学校排名高的学校：
        dfHigherSchool = dfSchools[dfSchools["录取位次"] < dfClosestSchool["录取位次"].values[0]]
        if(len(dfHigherSchool) != 0):
            dfHigherSchool = dfHigherSchool[dfHigherSchool["录取位次"] == dfHigherSchool.iloc[-1]["录取位次"]]

        return {"high": dfHigherSchool, "medium": dfClosestSchool, "low": dfLowSchool}


    def getRecommendSchools(self, scoreRank, dfSchools):
        #取到投档等级的最高和最低级：
        applyTopLevel = dfSchools["投档等级"].min()
        applyBottomLevel = dfSchools["投档等级"].max()

        #找到录取位次大于等于scoreRank的学校
        dfClosestSchool = dfSchools[dfSchools["录取位次"] >= scoreRank]

        #由于公布数据的一些差异，有可能有低分的排名已经超过了可查学校录取数据的最高录取位次，此时直接返回录取位次排名倒数的学校：
        if(len(dfClosestSchool) == 0):
            #根据2023录取结果，录取位次可以查到的最大值为14537，并且有超过20个学校都是这个值
            lowestAdmitRank = 14537
            dfClosestSchool = dfSchools[dfSchools["录取位次"] == lowestAdmitRank]
        
        #找到匹配学校的投档等级：
        matchApplyLevel = dfClosestSchool.iloc[0]["投档等级"]
        
        #找到投档等级为matchApplyLevel的学校：
        dfClosestSchool = dfSchools[dfSchools["投档等级"] == matchApplyLevel]

        #找到比matchApplyLevel高一个档次的学校：
        if(matchApplyLevel == applyTopLevel):
            dfHigherSchool = pd.DataFrame()
        else:
            higherLevel = dfSchools[dfSchools["投档等级"] < matchApplyLevel]["投档等级"].max()
            dfHigherSchool = dfSchools[dfSchools["投档等级"] == higherLevel]

        #找到比matchApplyLevel低档次的学校，最多找maxShoolLevels个档次：
        if(matchApplyLevel == applyBottomLevel):
            dfLowerSchool = pd.DataFrame()
        else:
            maxLowShoolLevels = 4
            schoolLevel = 0

            lowerLevel = dfSchools[dfSchools["投档等级"] > matchApplyLevel]["投档等级"].min()
            dfLowerSchool = dfSchools[dfSchools["投档等级"] == lowerLevel]
            schoolLevel += 1

            while(schoolLevel < maxLowShoolLevels):
                if(lowerLevel == applyBottomLevel):
                    break

                lowerLevel = dfSchools[dfSchools["投档等级"] > lowerLevel]["投档等级"].min()
                dfTemp = dfSchools[dfSchools["投档等级"] == lowerLevel]
                dfLowerSchool = pd.concat([dfLowerSchool, dfTemp], ignore_index=True)
                schoolLevel += 1

        return {"high": dfHigherSchool, "medium": dfClosestSchool, "low": dfLowerSchool}      
        




    #根据分数排名，给出推荐填报学校：
    def recommendApplySchools(self, scoreRank):
        dfSchoolPublic = self.dfSchools[self.dfSchools["公办民办"]=="公办"]
        dfSchoolPrivate = self.dfSchools[self.dfSchools["公办民办"]=="民办"]

        dictRecommendSchoolPublic = self.getRecommendSchools(scoreRank, dfSchoolPublic)
        dictRecommendSchoolPrivate = self.getRecommendSchools(scoreRank, dfSchoolPrivate)
        return {"公办": dictRecommendSchoolPublic, "民办": dictRecommendSchoolPrivate}
    

    def displayRecommendSchools(self, dictRecommendSchools):
        dictSchoolPublic = dictRecommendSchools["公办"]
        dictSchoolPrivate = dictRecommendSchools["民办"]

        print(GlobalConfig.bcolors.PINK + "=================高段学校===============：" + GlobalConfig.bcolors.ENDC)
        if(len(dictSchoolPublic["high"]) != 0):
            print(GlobalConfig.bcolors.PINK + "公办：" + GlobalConfig.bcolors.ENDC)
            print(GlobalConfig.bcolors.PINK + tabulate(self.briefSchoolInfo(dictSchoolPublic["high"]), showindex="never", headers="keys", tablefmt="heavy_outline") + GlobalConfig.bcolors.ENDC)
            print("\n")
        if(len(dictSchoolPrivate["high"]) != 0):
            print(GlobalConfig.bcolors.PINK + "民办：" + GlobalConfig.bcolors.ENDC)
            print(GlobalConfig.bcolors.PINK + tabulate(self.briefSchoolInfo(dictSchoolPrivate["high"]), showindex="never", headers="keys", tablefmt="heavy_outline") + GlobalConfig.bcolors.ENDC)
            print("\n")

        print(GlobalConfig.bcolors.BLUE + "=================匹配学校===============：" + GlobalConfig.bcolors.ENDC)
        print(GlobalConfig.bcolors.BLUE + "公办：" + GlobalConfig.bcolors.ENDC)
        print(GlobalConfig.bcolors.BLUE + tabulate(self.briefSchoolInfo(dictSchoolPublic["medium"]), showindex="never", headers="keys", tablefmt="heavy_outline") + GlobalConfig.bcolors.ENDC)
        print("\n")
        print(GlobalConfig.bcolors.BLUE + "民办：" + GlobalConfig.bcolors.ENDC)
        print(GlobalConfig.bcolors.BLUE + tabulate(self.briefSchoolInfo(dictSchoolPrivate["medium"]), showindex="never", headers="keys", tablefmt="heavy_outline") + GlobalConfig.bcolors.ENDC)
        print("\n")

        print(GlobalConfig.bcolors.CYAN + "=================低段学校===============：" + GlobalConfig.bcolors.ENDC)
        if(len(dictSchoolPublic["low"]) != 0):
            print(GlobalConfig.bcolors.CYAN + "公办：" + GlobalConfig.bcolors.ENDC)
            print(GlobalConfig.bcolors.CYAN + tabulate(self.briefSchoolInfo(dictSchoolPublic["low"]), showindex="never", headers="keys", tablefmt="heavy_outline") + GlobalConfig.bcolors.ENDC)
            print("\n")
        if(len(dictSchoolPrivate["low"]) != 0):
            print(GlobalConfig.bcolors.CYAN + "民办：" + GlobalConfig.bcolors.ENDC)
            print(GlobalConfig.bcolors.CYAN + tabulate(self.briefSchoolInfo(dictSchoolPrivate["low"]), showindex="never", headers="keys", tablefmt="heavy_outline") + GlobalConfig.bcolors.ENDC)

        print("\n")
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
    

    def getSchoolNameByCode(self,schoolCode):
        return self.dfSchools.loc[self.dfSchools["学校代码"]==schoolCode, "学校名称"].values[0]

        