import sys
from os import system, name
from PyInquirer import prompt
from examples import custom_style_2

import config.config as GlobalConfig
from utils.studentName import StudentName
from validators.nameVal import NameValidator
from validators.genderVal import GenderValidator
from utils.scoreStats import ScoreStats
from utils.schoolStats import SchoolStats
from studentSet import StudentSet


if name == 'nt':
    _ = system('cls')
else:
    _ = system('clear')

with open("data/banner.txt") as f:
    print(f.read())

stuNameData = StudentName()
scoreStats = ScoreStats()

schoolStats = SchoolStats()
schoolStats.setupStats()

stuNames = stuNameData.cerateStudentNames(GlobalConfig.StudentTotal)
stuSet = StudentSet(stuNames)

questions = [
    {
        'type': 'input',
        'name': '姓名',
        'message': '请输入您的名字：',
        'validate': NameValidator
    }
]

mySelf = prompt(questions)

questions = [
    {
        'type': 'input',
        'name': '性别',
        'message': '请输入您的性别：',
        'validate': GenderValidator
    }
]

mySelf.update(prompt(questions))

questions = [
    {
        'type': 'list',
        'name': 'chooseScoreGenType',
        'message': '请选择您本次中考成绩产生方式:',
        'choices': [
            '电脑随机生成',
            '手动输入'
        ]
    }
]

myScoreType = prompt(questions)
myScore = stuSet.generateMyScore(myScoreType["chooseScoreGenType"])

mySelf.update(myScore)

#generate all students score:
stuSet.generateScores()
stuSet.appendMyself(mySelf)

# stuSet.showScoreHist("语文")
# stuSet.showScoreHist("数学")
# stuSet.showScoreHist("英语")
# stuSet.showScoreHist("物理")
# stuSet.showScoreHist("化学")
# stuSet.showScoreHist("体育")
# stuSet.showScoreHist("道法")
# stuSet.showScoreHist("历史")
# stuSet.showScoreHist("生物")
# stuSet.showScoreHist("地理")
#stuSet.showScoreHist("总分")
#stuSet.printAll()

stuSet.displayMyScoreAndRank()

#获取重高线：
privilegeScoreGate = stuSet.getPrivilegeScoreGate(schoolStats)
stuSet.displayPrivilegeScoreGate()

#检查自己是否可以参加第二批次志愿填报：
myTotalScore = stuSet.getMyTotalScore()
if(myTotalScore < privilegeScoreGate):
    print("\n")
    print("很遗憾，您本次中考没有达到重点线，不能参加第二批次志愿填报")
    input()
    sys.exit()


stuSet.sortStudentsByScore()

stuSet.showScoreCount()

