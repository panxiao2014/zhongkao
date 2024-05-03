import sys
import time
from os import system, name
from PyInquirer import prompt
from examples import custom_style_2

import config.config as GlobalConfig
from utils.studentName import StudentName
from validators.nameVal import NameValidator
from validators.genderVal import GenderValidator
from validators.schoolVal import SchoolValidator
from utils.schoolStats import SchoolStats
from utils.studentSet import StudentSet
from coreProcess.schoolApply import SchoolApply
from coreProcess.studentDispatch import StudentDispatch


#############clear screen and show the banner:##################
if name == 'nt':
    _ = system('cls')
else:
    _ = system('clear')

with open("config/banner.txt", encoding="utf8") as f:
    print(GlobalConfig.bcolors.GREEN + f.read() + GlobalConfig.bcolors.ENDC)
################################################################


#初始化学生，生成学生姓名，性别，类型（统招或调剂）
stuNameData = StudentName()
stuNames = stuNameData.cerateStudentNames(GlobalConfig.StudentTotal)
stuSet = StudentSet(stuNames)
stuSet.categorizeStudent()
#stuSet.showStudents()

GlobalConfig.StuNameLst = [d["姓名"] for d in stuNames]

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

GlobalConfig.StuNameLst.append(stuSet.myName+stuSet.myNameTag)

#显示我的成绩及排名：
stuSet.displayMyScoreAndRank()

#获取重高线：
schoolStats = SchoolStats()
schoolStats.setupStats()
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
#dictRecommendSchool = schoolStats.recommendSchool(stuSet.getMyScoreRank())
dictRecommendSchools = schoolStats.recommendApplySchools(stuSet.getMyScoreRank())
print("\n")
print("根据您的总分排名，我们向您推荐以下学校：")
#schoolStats.displayRecommendSchool(dictRecommendSchool)
schoolStats.displayRecommendSchools(dictRecommendSchools)
print("其他学校信息，请参考<<schools.2023.xlsx>>。")

#开始填报志愿：
time.sleep(1)
print("\n")
print(GlobalConfig.bcolors.BOLD + "开始填报志愿，请依次输入学校代码。按回车键继续。。。：" + GlobalConfig.bcolors.ENDC)
input()

dictMyApply = {}
confirmed = False

while(confirmed == False):
    dictMyApply = {}
    print("\n")

    for i in range(GlobalConfig.NumShoolToApply):
        questions = [
            {
                'type': 'input',
                'name': GlobalConfig.OrderMap[i],
                'message': "{}：".format(GlobalConfig.OrderMap[i]),
                'validate': SchoolValidator
            }
        ]

        dictMyApply.update(prompt(questions))

    schoolStats.displaySchoolApplied(dictMyApply)

    print("\n")
    questions = [
        {
            'type': 'list',
            'name': 'confirmOrNot',
            'message': '请确认以上信息是否正确',
            'choices': [
                '不改了，继续吧',
                '重新填报'
            ]
        }
    ]
    if(prompt(questions)["confirmOrNot"] == "重新填报"):
        confirmed = False
    else:
        confirmed = True

#保存我的填报志愿：
stuSet.saveMyApplying(dictMyApply)

#进入学生填报志愿阶段：
schoolApply = SchoolApply(stuSet, schoolStats)
schoolApply.coreProcess()

print("\n")

#投档环节：
studentDispatch = StudentDispatch(stuSet, schoolStats)
studentDispatch.setup()
studentDispatch.coreProcess()

#更新策略统计：
schoolApply.updateStrategyStats(studentDispatch)

#显示我的录取结果：
print("\n")
print(GlobalConfig.bcolors.BOLD + "投档结束。按回车键查看录取结果。。。" + GlobalConfig.bcolors.ENDC)
input()
stuSet.displayMyFinalResult(schoolStats)

#查看其他统计结果：
input()
isOver = False
while(isOver == False):
    questions = [
        {
            'type': 'list',
            'name': 'chooseStats',
            'message': '请选择您接下来的操作:',
            'choices': [
                '查看录取概况',
                '查看各志愿录取统计',
                '查看各学校录取结果',
                '查看考生信息',
                '查看一分一段表',
                '查看填报志愿策略分析结果',
                '不玩了，结束'
            ]
        }
    ]

    myChoice = prompt(questions)["chooseStats"]
    if(myChoice == "不玩了，结束"):
        isOver = True
    elif(myChoice == "查看录取概况"):
        print("\n")
        studentDispatch.displayGeneralStats()
        print("\n")
    elif(myChoice == "查看各志愿录取统计"):
        print("\n")
        studentDispatch.displayEachOrderStats()
        print("\n")
    elif(myChoice == "查看各学校录取结果"):
        print("\n")
        studentDispatch.displaySchoolAdmitResult()
        print("\n")
    elif(myChoice == "查看考生信息"):
        print("\n")
        studentDispatch.displayStudentInfo()
        print("\n")
    elif(myChoice == "查看一分一段表"):
        print("\n")
        stuSet.showScoreCount()
        print("\n")
    elif(myChoice == "查看填报志愿策略分析结果"):
        print("\n")
        schoolApply.showStrategyStats()
        print("\n")

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

