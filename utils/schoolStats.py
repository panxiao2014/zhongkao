import pandas as pd

class SchoolStats:
    def __init__(self):
        self.dfSchools = pd.read_excel('data/schools.2023.xlsx')

        #第二批次所有需要通过考试录取的学生总数。包括：
        #市直属普高，公办：计划招生数
        #5+2普高，公办：计划招生数 - 指标到校数
        #5+2普高，民办：计划招生数
        self.numSecondRoundStuQuota = 0
        return
    

    def setupStats(self):
        dfCityPublic = self.dfSchools[(self.dfSchools["公办民办"]=="公办") & (self.dfSchools["学校性质"]=="市直属普高") & (self.dfSchools["级别"]=="省级示范")]
        sumStu1 = dfCityPublic["5+2区域计划"].sum()
        
        dfNormalPublic = self.dfSchools[(self.dfSchools["公办民办"]=="公办") & (self.dfSchools["学校性质"]=="5+2普高") & (self.dfSchools["级别"]=="省级示范")]
        sumStu2 = dfNormalPublic["5+2区域计划"].sum() - dfNormalPublic["指标到校"].sum()
        
        dfNormalPrivate = self.dfSchools[(self.dfSchools["公办民办"]=="民办") & (self.dfSchools["学校性质"]=="5+2普高") & (self.dfSchools["级别"]=="省级示范")]
        sumStu3 = dfNormalPrivate["5+2区域计划"].sum()
        
        self.numSecondRoundStuQuota = sumStu1 + sumStu2 + sumStu3
        return
    

    def getSecondRoundStuQuota(self):
        return self.numSecondRoundStuQuota