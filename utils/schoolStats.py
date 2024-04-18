import pandas as pd

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
    

    #根据分数排名，给出推荐填报学校：
    def recommendSchool(self, scoreRank):
        #根据学校录取位次，找到与scoreRank最接近的学校：
        closestSchool = self.dfSchools.iloc[(self.dfSchools["录取位次"] - scoreRank).abs().argsort()[:1]]
        closestSchool = self.dfSchools[self.dfSchools["录取位次"] == closestSchool["录取位次"].values[0]]
        

        #找到比最接近学校高的三个学校：
        higherSchool = self.dfSchools[self.dfSchools["录取位次"] < closestSchool["录取位次"].values[0]]
        if(len(higherSchool) < 3):
            higherSchool = higherSchool.tail(len(higherSchool)) 
        else:
            higherSchool = higherSchool.tail(3)
       

        #找到比最接近学校低的七个学校：
        lowerSchool = self.dfSchools[self.dfSchools["录取位次"] > closestSchool["录取位次"].values[0]]
        if(len(lowerSchool) < 7):
            lowerSchool = lowerSchool.head(len(lowerSchool)) 
        else:
            lowerSchool = lowerSchool.head(7)

        dfRecommendSchool = pd.concat([higherSchool, closestSchool, lowerSchool])

        return dfRecommendSchool