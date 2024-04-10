from PyInquirer import prompt
from examples import custom_style_2

import config.config as GlobalConfig
from utils.studentName import StudentName
from validators.nameVal import NameValidator
from validators.genderVal import GenderValidator
from utils.scoreStats import ScoreStats
from utils.schoolStats import SchoolStats
from studentSet import StudentSet

stuNameData = StudentName()
scoreStats = ScoreStats()
schoolStats = SchoolStats()

stuNames = stuNameData.cerateStudentNames(GlobalConfig.StudentTotal)
stuSet = StudentSet(stuNames)

questions = [
    {
        'type': 'input',
        'name': '姓名',
        'message': '请输入你的名字：',
        'validate': NameValidator
    }
]

mySelf = prompt(questions)

questions = [
    {
        'type': 'input',
        'name': '性别',
        'message': '请输入你的性别：',
        'validate': GenderValidator
    }
]

mySelf.update(prompt(questions))

questions = [
    {
        'type': 'list',
        'name': 'chooseScoreGenType',
        'message': '请选择本次中考成绩产生方式:',
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

stuSet.showScoreCount()

