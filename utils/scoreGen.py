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
import pandas as pd
import warnings

from PyInquirer import prompt
from validators.scoreVal import ScoreValidator150
from validators.scoreVal import ScoreValidator70
from validators.scoreVal import ScoreValidator50
from validators.scoreVal import ScoreValidator60
from validators.scoreVal import ScoreValidator20
import config.config as GlobalConfig



class ScoreGen:
    def __init__(self, stuNumber, dfStudents):
        self.stuNumber = stuNumber

        warnings.simplefilter(action='ignore', category=UserWarning)
        self.dfScoreStats = pd.read_excel('data/score.stats.2023.xlsx', dtype={"学校代码": str})
        warnings.resetwarnings()

        self.dfStudents = dfStudents
        return
    

    #根据一分一段表，生成每个学生的中考总分：
    def generateScoresForAllStudents(self):
        stuIndex = 0
        for index, row in self.dfScoreStats.iterrows():
            score = row["分数"]
            stuNumber = row["人数"]
            
            startIdx = stuIndex
            endIdx = startIdx + stuNumber - 1

            self.dfStudents.loc[startIdx:endIdx, '总分'] = score
            stuIndex = endIdx + 1

            if(score == GlobalConfig.ScoreBottomGate):
                break
        
        return

    

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
                'message': '请输入您的语文得分(0-150)：',
                'validate': ScoreValidator150
            }
        ]

        myScore.update(prompt(questions))

        questions = [
            {
                'type': 'input',
                'name': '数学',
                'message': '请输入您的数学得分(0-150)：',
                'validate': ScoreValidator150
            }
        ]

        myScore.update(prompt(questions))

        questions = [
            {
                'type': 'input',
                'name': '英语',
                'message': '请输入您的英语得分(0-150)：',
                'validate': ScoreValidator150
            }
        ]

        myScore.update(prompt(questions))

        questions = [
            {
                'type': 'input',
                'name': '物理',
                'message': '请输入您的物理得分(0-70)：',
                'validate': ScoreValidator70
            }
        ]

        myScore.update(prompt(questions))

        questions = [
            {
                'type': 'input',
                'name': '化学',
                'message': '请输入您的化学得分(0-50)：',
                'validate': ScoreValidator50
            }
        ]

        myScore.update(prompt(questions))

        questions = [
            {
                'type': 'input',
                'name': '体育',
                'message': '请输入您的体育得分(0-60)：',
                'validate': ScoreValidator60
            }
        ]

        myScore.update(prompt(questions))

        questions = [
            {
                'type': 'input',
                'name': '道法',
                'message': '请输入您的道法得分(20, 16, 12, 8)：',
                'validate': ScoreValidator20
            }
        ]

        myScore.update(prompt(questions))

        questions = [
            {
                'type': 'input',
                'name': '历史',
                'message': '请输入您的历史得分(20, 16, 12, 8)：',
                'validate': ScoreValidator20
            }
        ]

        myScore.update(prompt(questions))

        questions = [
            {
                'type': 'input',
                'name': '生物',
                'message': '请输入您的生物得分(20, 16, 12, 8)：',
                'validate': ScoreValidator20
            }
        ]

        myScore.update(prompt(questions))

        questions = [
            {
                'type': 'input',
                'name': '地理',
                'message': '请输入您的地理得分(20, 16, 12, 8)：',
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