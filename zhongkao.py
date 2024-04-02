from PyInquirer import prompt
from examples import custom_style_2

import config.config as GlobalConfig
from utils.studentName import StudentName
from validators.genderVal import GenderValidator
from utils.scoreStats import ScoreStats
from utils.schoolStats import SchoolStats
from studentSet import StudentSet

stuNameData = StudentName()
scoreStats = ScoreStats()
schoolStats = SchoolStats()

stuNames = stuNameData.cerateStudentNames(GlobalConfig.StudentTotal)

stuSet = StudentSet(stuNames)
stuSet.generateScores()
stuSet.showScoreHist("语文")
stuSet.showScoreHist("数学")
stuSet.showScoreHist("英语")
stuSet.showScoreHist("物理")
stuSet.showScoreHist("化学")
stuSet.showScoreHist("体育")
stuSet.showScoreHist("道法")
stuSet.showScoreHist("历史")
stuSet.showScoreHist("生物")
stuSet.showScoreHist("地理")
stuSet.showScoreHist("总分")
#stuSet.printAll()

# questions = [
#     {
#         'type': 'input',
#         'name': 'myName',
#         'message': '请输入你的名字：'
#     }
# ]

# myName = prompt(questions)

# questions = [
#     {
#         'type': 'input',
#         'name': 'myGender',
#         'message': '请输入你的性别：',
#         'validate': GenderValidator
#     }
# ]

# myGender = prompt(questions)