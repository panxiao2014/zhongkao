#中考成绩规则：
#语，数，外：满分150
#物理：满分70
#化学：满分50
#体育：满分60
#道法，历史，生物，地理：20, 16, 12, 8, 0
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
        "Scale": 40,
        "Skew": 0
    },

    "英语": {
        "Max": 148,
        "Min": 30,
        "Mean": 120,
        "Scale": 30,
        "Skew": 0
    },

    "物理": {
        "Max": 70,
        "Min": 20,
        "Mean": 50,
        "Scale": 30,
        "Skew": 0
    },

    "化学": {
        "Max": 50,
        "Min": 20,
        "Mean": 35,
        "Scale": 20,
        "Skew": 0
    }
}

class ScoreGen:
    def __init__(self):
        return
    
    def scoreGen(self, course, stuNumber):
        scores = ss.pearson3.rvs(loc=random.randint(ScoreControl[course]["Mean"]-MeanRange, ScoreControl[course]["Mean"]+MeanRange), 
                                 scale=random.randint(ScoreControl[course]["Scale"]-ScaleRange, ScoreControl[course]["Scale"]+ScaleRange), 
                                 skew=random.randint(ScoreControl[course]["Skew"]-SkewRange, ScoreControl[course]["Skew"]+SkewRange),  
                                size=stuNumber)
        
        dfCourse = pd.DataFrame({course: scores})
        dfCourse[course] = dfCourse[course].astype(int)
        dfCourse[course] = np.where(dfCourse[course]<ScoreControl[course]["Min"], ScoreControl[course]["Min"], dfCourse[course])
        dfCourse[course] = np.where(dfCourse[course]>ScoreControl[course]["Max"], ScoreControl[course]["Max"], dfCourse[course])
        
        return dfCourse
          
    
    def scoreChinese(self, stuNumber):        
        return self.scoreGen("语文", stuNumber)
    
    
    def scoreMath(self, stuNumber):
        return self.scoreGen("数学", stuNumber)
    

    def scoreEnglish(self, stuNumber):
        return self.scoreGen("英语", stuNumber)
    

    def scorePhysics(self, stuNumber):
        return self.scoreGen("物理", stuNumber)
    

    def scoreChemistry(self, stuNumber):
        return self.scoreGen("化学", stuNumber)
