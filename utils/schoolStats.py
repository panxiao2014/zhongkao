import pandas as pd

class SchoolStats:
    def __init__(self):
        self.dfSchools = pd.read_excel('data/schools.2023.xlsx')

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