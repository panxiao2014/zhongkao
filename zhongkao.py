from PyInquirer import prompt
from examples import custom_style_2

import config.config as GlobalConfig
from utils.studentName import StudentName
from validators.nameVal import NameValidator
from validators.genderVal import GenderValidator
from validators.scoreVal import ScoreValidator150
from validators.scoreVal import ScoreValidator70
from validators.scoreVal import ScoreValidator50
from validators.scoreVal import ScoreValidator60
from validators.scoreVal import ScoreValidator20
from utils.scoreStats import ScoreStats
from utils.schoolStats import SchoolStats
from studentSet import StudentSet

stuNameData = StudentName()
scoreStats = ScoreStats()
schoolStats = SchoolStats()

stuNames = stuNameData.cerateStudentNames(GlobalConfig.StudentTotal)

stuSet = StudentSet(stuNames)
stuSet.generateScores()
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
# stuSet.showScoreHist("总分")

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
        'type': 'input',
        'name': '语文',
        'message': '请输入你的语文得分(0-150)：',
        'validate': ScoreValidator150
    }
]

mySelf.update(prompt(questions))

questions = [
    {
        'type': 'input',
        'name': '数学',
        'message': '请输入你的数学得分(0-150)：',
        'validate': ScoreValidator150
    }
]

mySelf.update(prompt(questions))

questions = [
    {
        'type': 'input',
        'name': '英语',
        'message': '请输入你的英语得分(0-150)：',
        'validate': ScoreValidator150
    }
]

mySelf.update(prompt(questions))

questions = [
    {
        'type': 'input',
        'name': '物理',
        'message': '请输入你的物理得分(0-70)：',
        'validate': ScoreValidator70
    }
]

mySelf.update(prompt(questions))

questions = [
    {
        'type': 'input',
        'name': '化学',
        'message': '请输入你的化学得分(0-50)：',
        'validate': ScoreValidator50
    }
]

mySelf.update(prompt(questions))

questions = [
    {
        'type': 'input',
        'name': '体育',
        'message': '请输入你的体育得分(0-60)：',
        'validate': ScoreValidator60
    }
]

mySelf.update(prompt(questions))

questions = [
    {
        'type': 'input',
        'name': '道法',
        'message': '请输入你的道法得分(20, 16, 12, 8)：',
        'validate': ScoreValidator20
    }
]

mySelf.update(prompt(questions))

questions = [
    {
        'type': 'input',
        'name': '历史',
        'message': '请输入你的历史得分(20, 16, 12, 8)：',
        'validate': ScoreValidator20
    }
]

mySelf.update(prompt(questions))

questions = [
    {
        'type': 'input',
        'name': '生物',
        'message': '请输入你的生物得分(20, 16, 12, 8)：',
        'validate': ScoreValidator20
    }
]

mySelf.update(prompt(questions))

questions = [
    {
        'type': 'input',
        'name': '地理',
        'message': '请输入你的地理得分(20, 16, 12, 8)：',
        'validate': ScoreValidator20
    }
]

mySelf.update(prompt(questions))

mySelf["语文"] = int(mySelf["语文"])
mySelf["数学"] = int(mySelf["数学"])
mySelf["英语"] = int(mySelf["英语"])
mySelf["物理"] = int(mySelf["物理"])
mySelf["化学"] = int(mySelf["化学"])
mySelf["体育"] = int(mySelf["体育"])
mySelf["道法"] = int(mySelf["道法"])
mySelf["历史"] = int(mySelf["历史"])
mySelf["生物"] = int(mySelf["生物"])
mySelf["地理"] = int(mySelf["地理"])

mySelf["总分"] = mySelf["语文"] + mySelf["数学"] + mySelf["英语"] + mySelf["物理"] + mySelf["化学"] + mySelf["体育"]\
                   + mySelf["道法"] + mySelf["历史"] + mySelf["生物"] + mySelf["地理"]

stuSet.appendMyself(mySelf)

stuSet.printAll()

#generate score count:
stuSet.generateScoreCount()
stuSet.showScoreCount()

