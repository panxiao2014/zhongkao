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

from PyInquirer import prompt
from validators.scoreVal import ScoreValidator150
from validators.scoreVal import ScoreValidator70
from validators.scoreVal import ScoreValidator50
from validators.scoreVal import ScoreValidator60
from validators.scoreVal import ScoreValidator20

MeanRange = 10
ScaleRange = 4
SkewRange = 0

#based on 2023 score stats, define score and number of students as high score students:
HighScoreGate = 620
HighScoreStudents = 4000
HighScoretudentsVariance = 200

ScoreControl = {
    "语文": {
        "Max": 145,
        "Min": 30,
        "Mean": 119,
        "Scale": 30,
        "Skew": -2
    },

    "数学": {
        "Max": 150,
        "Min": 40,
        "Mean": 111,
        "Scale": 30,
        "Skew": -1
    },

    "英语": {
        "Max": 148,
        "Min": 30,
        "Mean": 120,
        "Scale": 30,
        "Skew": -1
    },

    "物理": {
        "Max": 70,
        "Min": 20,
        "Mean": 55,
        "Scale": 7,
        "Skew": -1
    },

    "化学": {
        "Max": 50,
        "Min": 20,
        "Mean": 55,
        "Scale": 4,
        "Skew": -1
    },

    "体育": {
        "Max": 60,
        "Min": 30,
        "Mean": 48,
        "Scale": 14,
        "Skew": -1
    },

    "道法": {
        "Max": 100,
        "Min": 30,
        "Mean": 85,
        "Scale": 15,
        "Skew": -1
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
        "Skew": -1
    },

    "地理": {
        "Max": 100,
        "Min": 20,
        "Mean": 78,
        "Scale": 19,
        "Skew": -1
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
    

    def genMyScoreAuto(self):
        myScore = {}
        myScore["语文"] = random.randint(115, 130)
        myScore["数学"] = random.randint(110, 125)
        myScore["英语"] = random.randint(125, 140)
        myScore["物理"] = random.randint(58, 69)
        myScore["化学"] = random.randint(39, 49)
        myScore["体育"] = random.randint(50, 60)
        myScore["道法"] = random.choice([20, 16])
        myScore["历史"] = random.choice([20, 16])
        myScore["生物"] = random.choice([20, 16])
        myScore["地理"] = random.choice([20, 16])
        myScore["总分"] = myScore["语文"] + myScore["数学"] + myScore["英语"] + myScore["物理"] + myScore["化学"] + myScore["体育"]\
                + myScore["道法"] + myScore["历史"] + myScore["生物"] + myScore["地理"]
        return myScore
    

    def genMyScoreManual(self):
        myScore = {}

        questions = [
            {
                'type': 'input',
                'name': '语文',
                'message': '请输入你的语文得分(0-150)：',
                'validate': ScoreValidator150
            }
        ]

        myScore.update(prompt(questions))

        questions = [
            {
                'type': 'input',
                'name': '数学',
                'message': '请输入你的数学得分(0-150)：',
                'validate': ScoreValidator150
            }
        ]

        myScore.update(prompt(questions))

        questions = [
            {
                'type': 'input',
                'name': '英语',
                'message': '请输入你的英语得分(0-150)：',
                'validate': ScoreValidator150
            }
        ]

        myScore.update(prompt(questions))

        questions = [
            {
                'type': 'input',
                'name': '物理',
                'message': '请输入你的物理得分(0-70)：',
                'validate': ScoreValidator70
            }
        ]

        myScore.update(prompt(questions))

        questions = [
            {
                'type': 'input',
                'name': '化学',
                'message': '请输入你的化学得分(0-50)：',
                'validate': ScoreValidator50
            }
        ]

        myScore.update(prompt(questions))

        questions = [
            {
                'type': 'input',
                'name': '体育',
                'message': '请输入你的体育得分(0-60)：',
                'validate': ScoreValidator60
            }
        ]

        myScore.update(prompt(questions))

        questions = [
            {
                'type': 'input',
                'name': '道法',
                'message': '请输入你的道法得分(20, 16, 12, 8)：',
                'validate': ScoreValidator20
            }
        ]

        myScore.update(prompt(questions))

        questions = [
            {
                'type': 'input',
                'name': '历史',
                'message': '请输入你的历史得分(20, 16, 12, 8)：',
                'validate': ScoreValidator20
            }
        ]

        myScore.update(prompt(questions))

        questions = [
            {
                'type': 'input',
                'name': '生物',
                'message': '请输入你的生物得分(20, 16, 12, 8)：',
                'validate': ScoreValidator20
            }
        ]

        myScore.update(prompt(questions))

        questions = [
            {
                'type': 'input',
                'name': '地理',
                'message': '请输入你的地理得分(20, 16, 12, 8)：',
                'validate': ScoreValidator20
            }
        ]

        myScore.update(prompt(questions))

        myScore["语文"] = int(myScore["语文"])
        myScore["数学"] = int(myScore["数学"])
        myScore["英语"] = int(myScore["英语"])
        myScore["物理"] = int(myScore["物理"])
        myScore["化学"] = int(myScore["化学"])
        myScore["体育"] = int(myScore["体育"])
        myScore["道法"] = int(myScore["道法"])
        myScore["历史"] = int(myScore["历史"])
        myScore["生物"] = int(myScore["生物"])
        myScore["地理"] = int(myScore["地理"])

        myScore["总分"] = myScore["语文"] + myScore["数学"] + myScore["英语"] + myScore["物理"] + myScore["化学"] + myScore["体育"]\
                        + myScore["道法"] + myScore["历史"] + myScore["生物"] + myScore["地理"]
        return myScore
    

    def isGoodScoreDistribution(self, dfTotalScore):
        numHighScoreStudents = dfTotalScore.loc[dfTotalScore["分数"]==HighScoreGate, "累计"].values[0]
        return (numHighScoreStudents <= (HighScoreStudents+HighScoretudentsVariance) and numHighScoreStudents >= (HighScoreStudents-HighScoretudentsVariance))