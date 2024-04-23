import sys
import time
from os import system, name
from PyInquirer import prompt
from examples import custom_style_2

import config.config as GlobalConfig
from utils.studentName import StudentName
from validators.nameVal import NameValidator
from validators.genderVal import GenderValidator
from utils.scoreStats import ScoreStats
from utils.schoolStats import SchoolStats
from utils.studentSet import StudentSet


#############clear screen and show the banner:##################
if name == 'nt':
    _ = system('cls')
else:
    _ = system('clear')

with open("config/banner.txt", encoding="utf8") as f:
    print(GlobalConfig.bcolors.GREEN + f.read() + GlobalConfig.bcolors.ENDC)
################################################################



stuNameData = StudentName()
scoreStats = ScoreStats()

schoolStats = SchoolStats()
schoolStats.setupStats()

#初始化学生，生成学生姓名，性别，类型（统招或调剂）
stuNames = stuNameData.cerateStudentNames(GlobalConfig.StudentTotal)
stuSet = StudentSet(stuNames)
stuSet.categorizeStudent()
#stuSet.showStudents()

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

#生成所有学生的考试成绩：
stuSet.generateScores()
stuSet.appendMyself(mySelf)


#显示我的成绩及排名：
stuSet.displayMyScoreAndRank()

#获取重高线：
privilegeScoreGate = stuSet.getPrivilegeScoreGate(schoolStats)
stuSet.displayPrivilegeScoreGate()

#检查自己是否可以参加第二批次志愿填报：
myTotalScore = stuSet.getMyTotalScore()
if(myTotalScore < privilegeScoreGate):
    print("\n")
    print(GlobalConfig.bcolors.GREEN + "很遗憾，您本次中考没有达到重点线，不能参加第二批次志愿填报" + GlobalConfig.bcolors.ENDC)
    input()
    sys.exit()

#去掉重高线以下，以及市指标到校生, 艺体生 （这些学生不参加第二批次投档）
stuSet.trimDownStudents()

print("\n")
print("参加第二批次网上志愿填报的学生共有：" + GlobalConfig.bcolors.YELLO + "{}".format(stuSet.getStuForSecondRoundNum()) + GlobalConfig.bcolors.ENDC + "名")

time.sleep(1)
print("\n")
print("即将进入第二批次志愿填报阶段，按回车键继续。。。")
input()


#根据自己排名列出推荐学校:
dictRecommendSchool = schoolStats.recommendSchool(stuSet.getMyScoreRank())
print("\n")
print("根据您的总分排名，我们向您推荐以下学校：")
schoolStats.displayRecommendSchool(dictRecommendSchool)


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
#stuSet.showStudents()
#stuSet.showScoreCount()

