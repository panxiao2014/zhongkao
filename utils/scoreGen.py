#中考成绩规则：
#语，数，外：满分150
#物理：满分70
#化学：满分50
#体育：满分60
#道法，历史，生物，地理:
#  80-100: 20
#  70-79:  16
#  60-69:  12
#  0-59:   8
#满分: 710

import random
import numpy as np
import pandas as pd
import scipy.stats as ss


MeanRange = 10
ScaleRange = 4
SkewRange = 0

ScoreControl = {
    "语文": {
        "Max": 145,
        "Min": 30,
        "Mean": 110,
        "Scale": 15,
        "Skew": 0
    },

    "数学": {
        "Max": 150,
        "Min": 40,
        "Mean": 105,
        "Scale": 5,
        "Skew": 0
    },

    "英语": {
        "Max": 148,
        "Min": 30,
        "Mean": 120,
        "Scale": 6,
        "Skew": 0
    },

    "物理": {
        "Max": 70,
        "Min": 20,
        "Mean": 50,
        "Scale": 7,
        "Skew": 1
    },

    "化学": {
        "Max": 50,
        "Min": 20,
        "Mean": 35,
        "Scale": 4,
        "Skew": 0
    },

    "体育": {
        "Max": 60,
        "Min": 30,
        "Mean": 48,
        "Scale": 14,
        "Skew": 0
    },

    "道法": {
        "Max": 100,
        "Min": 30,
        "Mean": 85,
        "Scale": 15,
        "Skew": 0
    },

    "历史": {
        "Max": 100,
        "Min": 20,
        "Mean": 75,
        "Scale": 15,
        "Skew": 0
    },

    "生物": {
        "Max": 100,
        "Min": 20,
        "Mean": 71,
        "Scale": 18,
        "Skew": 0
    },

    "地理": {
        "Max": 100,
        "Min": 20,
        "Mean": 78,
        "Scale": 19,
        "Skew": 0
    }
}

class ScoreGen:
    def __init__(self, stuNumber):
        self.stuNumber = stuNumber
        return
    
    def scoreGen(self, course):
        scores = ss.pearson3.rvs(loc=random.randint(ScoreControl[course]["Mean"]-MeanRange, ScoreControl[course]["Mean"]+MeanRange), 
                                 scale=random.randint(ScoreControl[course]["Scale"]-ScaleRange, ScoreControl[course]["Scale"]+ScaleRange), 
                                 skew=random.randint(ScoreControl[course]["Skew"]-SkewRange, ScoreControl[course]["Skew"]+SkewRange),  
                                size=self.stuNumber)
        
        dfCourse = pd.DataFrame({course: scores})
        dfCourse[course] = dfCourse[course].astype(int)
        dfCourse[course] = np.where(dfCourse[course]<ScoreControl[course]["Min"], ScoreControl[course]["Min"], dfCourse[course])
        dfCourse[course] = np.where(dfCourse[course]>ScoreControl[course]["Max"], ScoreControl[course]["Max"], dfCourse[course])

        if(course == "道法" or course == "历史" or course == "生物" or course == "地理"):
            dfCourse[course] = np.where((dfCourse[course]>=80) & (dfCourse[course]<=100), 20,
                                        np.where((dfCourse[course]>=70) & (dfCourse[course]<=79), 16,
                                        np.where((dfCourse[course]>=60) & (dfCourse[course]<=69), 12, 8)))
        
        return dfCourse
          
    
    def scoreChinese(self):        
        return self.scoreGen("语文")
    
    
    def scoreMath(self):
        return self.scoreGen("数学")
    

    def scoreEnglish(self):
        return self.scoreGen("英语")
    

    def scorePhysics(self):
        return self.scoreGen("物理")
    

    def scoreChemistry(self):
        return self.scoreGen("化学")


    def scorePE(self):
        return self.scoreGen("体育")
    

    def scorePolitics(self):
        return self.scoreGen("道法")
    

    def scoreHistory(self):
        return self.scoreGen("历史")
    

    def scoreBiology(self):
        return self.scoreGen("生物")
    

    def scoreGeography(self):
        return self.scoreGen("地理")