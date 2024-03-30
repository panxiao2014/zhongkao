from PyInquirer import prompt
from examples import custom_style_2

import config.config as GlobalConfig
from utils.studentName import StudentName
from validators.genderVal import GenderValidator
from utils.scoreStats import ScoreStats

stuNameData = StudentName()
scoreStats = ScoreStats()

stuSet = stuNameData.cerateStudentSet(GlobalConfig.StudentTotal)

questions = [
    {
        'type': 'input',
        'name': 'myName',
        'message': '请输入你的名字：'
    }
]

myName = prompt(questions)

questions = [
    {
        'type': 'input',
        'name': 'myGender',
        'message': '请输入你的性别：',
        'validate': GenderValidator
    }
]

myGender = prompt(questions)

stuNameData.addStudent(myName['myName'], myGender['myGender'])

stuNameData.listAll()