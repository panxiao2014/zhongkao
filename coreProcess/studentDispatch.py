from tabulate import tabulate
from PyInquirer import prompt
import pandas as pd
from progress.spinner import LineSpinner

import config.config as GlobalConfig
from validators.schoolVal import SchoolValidator
from validators.studentNameVal import StudentNameValidator

class StudentDispatch:
    def __init__(self, stuSet, schoolStats):
        self.stuSet = stuSet
        self.schoolStats = schoolStats
        self.dfStuForSecondRound = stuSet.dfStuForSecondRound
        self.dfSchools = schoolStats.dfSchools
        self.myName = stuSet.myName
        self.myNameTag = stuSet.myNameTag

        #一共录取的学生数：
        self.numStudentsAdmitted = 0

        #统计每个志愿录取的人数：
        self.finalAdmitStats = {}
        return
    

    def setup(self):
        #dfSchools, 增加column用于记录录取结果：
        for i in range(0, GlobalConfig.NumShoolToApply):
            self.dfSchools[GlobalConfig.OrderMap[i]] = 0

        #dfStuForSecondRound, 增加column用于记录学生最后的录取结果：
        self.dfStuForSecondRound["已经录取"] = False
        self.dfStuForSecondRound["录取志愿"] = None
        self.dfStuForSecondRound["录取学校代码"] = None

        #初始化统计数据：
        for i in range(0, GlobalConfig.NumShoolToApply):
            self.finalAdmitStats[GlobalConfig.OrderMap[i]] = 0
        return
    

    #在某一分数段，如果填报学校的人数超过学校录取余额的，则进行PK。官方规则如下：
    # 1. "成都工匠"子女，市级以上新时代好少年等优先投档
    # 2. 语，数，外总分高，优先投档
    # 3. 语，数，外，物理B卷分数总和高，优先投档
    # 4. 体育成绩高，优先投档
    # 5. 若还没有决出胜负，经研究后处理
    # 为简化，本程序只执行规则2。如果不能决出胜负，则随机选择决定
    def studentsPK(self, dfGroupedStudents, numQuotaRemain):
        dfGroupedStudents["partialTotal"] = dfGroupedStudents["语文"] + dfGroupedStudents["数学"] + dfGroupedStudents["英语"]
        dfGroupedStudents = dfGroupedStudents.sort_values(by="partialTotal", ascending=False)

        dfGroupedStudents = dfGroupedStudents.head(numQuotaRemain)
        dfGroupedStudents.drop(columns="partialTotal", inplace=True)

        return dfGroupedStudents
    

    #对学生进行投档
    #score: 当前投档分数段
    #applyOrder： 第几志愿
    #schoolCode 当前填报的学校代码
    #dfGroupedStudents: 在该分数段下，当前志愿里填写该学校的学生集
    #dfStudents: 该分数段的所有学生集
    def dispatchToSchoolWithApplyOrder(self, score, applyOrder, schoolCode, dfGroupedStudents, dfStudents):
        #1,3,5,7查看统招余额，2，4，6查看调剂余额。民办没有调剂，只看统招余额
        schoolType = self.dfSchools.loc[self.dfSchools["学校代码"]==schoolCode, "公办民办"].values[0]
        orderType = ""
        if(applyOrder % 2 == 0 or schoolType == "民办"):
            orderType = "统招"
        else:
            orderType = "调剂"
        strOrderType = "{}余额".format(orderType)
        
        numQuotaRemain = self.dfSchools.loc[self.dfSchools["学校代码"]==schoolCode, strOrderType].values[0]
        if(numQuotaRemain == 0):
            return
        
        numStuRemain = len(dfGroupedStudents)
        if(numQuotaRemain >= numStuRemain):
            #学校录取剩余名额大于填报学校的学生数，则所有学生录取:
            self.numStudentsAdmitted += numStuRemain
            self.finalAdmitStats[GlobalConfig.OrderMap[applyOrder]] += numStuRemain

            #更新学校剩余招收名额：
            self.dfSchools.loc[self.dfSchools["学校代码"]==schoolCode, strOrderType] = numQuotaRemain - numStuRemain

            #更新学生记录：
            dfStudents.loc[dfStudents["姓名"].isin(dfGroupedStudents["姓名"]), "已经录取"] = True
            self.dfStuForSecondRound.loc[self.dfStuForSecondRound["姓名"].isin(dfGroupedStudents["姓名"]), "已经录取"] = True
            self.dfStuForSecondRound.loc[self.dfStuForSecondRound["姓名"].isin(dfGroupedStudents["姓名"]), "录取志愿"] = GlobalConfig.OrderMap[applyOrder]
            self.dfStuForSecondRound.loc[self.dfStuForSecondRound["姓名"].isin(dfGroupedStudents["姓名"]), "录取学校代码"] = schoolCode

            return
        else:
            dfWinningStudents = self.studentsPK(dfGroupedStudents, numQuotaRemain)
            self.numStudentsAdmitted += numQuotaRemain
            self.finalAdmitStats[GlobalConfig.OrderMap[applyOrder]] += numQuotaRemain

            #更新学校剩余招收名额：
            self.dfSchools.loc[self.dfSchools["学校代码"]==schoolCode, strOrderType] = 0

            #更新学生记录：
            dfStudents.loc[dfStudents["姓名"].isin(dfWinningStudents["姓名"]), "已经录取"] = True
            self.dfStuForSecondRound.loc[self.dfStuForSecondRound["姓名"].isin(dfWinningStudents["姓名"]), "已经录取"] = True
            self.dfStuForSecondRound.loc[self.dfStuForSecondRound["姓名"].isin(dfWinningStudents["姓名"]), "录取志愿"] = GlobalConfig.OrderMap[applyOrder]
            self.dfStuForSecondRound.loc[self.dfStuForSecondRound["姓名"].isin(dfWinningStudents["姓名"]), "录取学校代码"] = schoolCode

        return
    

    def studentsDispatch(self, dfStudents, score):
        #从第一志愿开始依次投档：
        for i in range(0, GlobalConfig.NumShoolToApply):
            #每个志愿先排除前个志愿已经录取的学生：
            dfStudents = dfStudents[dfStudents["已经录取"] == False]
            if(len(dfStudents) == 0):
                return

            #按照该分数段该志愿下学生填报的学校归类处理：
            groupSchool = dfStudents.groupby(GlobalConfig.OrderMap[i])
            for schoolCode, dfGroupedStudents in groupSchool:
                if(schoolCode != "None"):
                    self.dispatchToSchoolWithApplyOrder(score, i, schoolCode, dfGroupedStudents, dfStudents)
        return
    

    def coreProcess(self):
        print("\n")
        bar = LineSpinner('开始投档，请稍后。。。')

        #655分以上同学统一处理：
        dfTopStudents = self.dfStuForSecondRound[self.dfStuForSecondRound['总分'] >= GlobalConfig.ScoreTopGate]
        self.studentsDispatch(dfTopStudents, GlobalConfig.ScoreTopGate)

        bar.next()

        #从高分到省重线分，依次投档：
        for i in range(GlobalConfig.ScoreTopGate-1, self.stuSet.privilegeScoreGate-1, -1):
            dfStudents = self.dfStuForSecondRound[self.dfStuForSecondRound['总分'] == i]
            self.studentsDispatch(dfStudents, i)
            bar.next()

        return
    

    #查看录取概况：
    def displayGeneralStats(self):
        print("第二批次一共录取学生数： " + GlobalConfig.bcolors.YELLO + str(self.numStudentsAdmitted) + GlobalConfig.bcolors.ENDC + "名")
        print("滑档的学生共有： " + GlobalConfig.bcolors.YELLO + str(len(self.dfStuForSecondRound)- self.numStudentsAdmitted) + GlobalConfig.bcolors.ENDC + "名")
        return
    

    #查看各志愿的录取统计信息：
    def displayEachOrderStats(self):
        print("各志愿录取人数如下：")
        print(GlobalConfig.bcolors.YELLO + tabulate({"填报志愿": self.finalAdmitStats.keys(), "录取人数": self.finalAdmitStats.values()}, showindex="never", headers="keys", tablefmt="double_grid") + GlobalConfig.bcolors.ENDC)
        return
    

    #查看学校录取结果：
    def displaySchoolAdmitResult(self):
        questions = [
            {
                'type': 'input',
                'name': 'inputSchool',
                'message': "请输入您想要查看学校的代码：",
                'validate': SchoolValidator
            }
        ]

        schoolCode = prompt(questions)['inputSchool']
        schoolName = self.schoolStats.getSchoolNameByCode(schoolCode)
        schoolPlanQuota = self.dfSchools.loc[self.dfSchools["学校代码"]==schoolCode, "第二批次招收名额"].values[0]
        schoolPlanQuotaStr = GlobalConfig.bcolors.YELLO + schoolName + GlobalConfig.bcolors.ENDC + "第二批次计划招收学生" + GlobalConfig.bcolors.YELLO + str(schoolPlanQuota) + GlobalConfig.bcolors.ENDC + "名"

        dfStuAdmit = (self.dfStuForSecondRound.loc[self.dfStuForSecondRound["录取学校代码"] == schoolCode]).copy()
        dfStuAdmit = dfStuAdmit.sort_values(by="总分", ascending=False)
        dfStuAdmit = dfStuAdmit[["姓名", "性别", "类型", "总分", "录取志愿", "选取策略"]]

        print("\n")
        print(schoolPlanQuotaStr)
        print("实际录取学生" + GlobalConfig.bcolors.YELLO + str(len(dfStuAdmit)) + GlobalConfig.bcolors.ENDC+ "名。录取名单如下：")
        print(GlobalConfig.bcolors.CYAN + tabulate(dfStuAdmit, showindex="never", headers="keys", tablefmt="rounded_grid") + GlobalConfig.bcolors.ENDC)
        return


    #查看考生信息：
    def displayStudentInfo(self):
        questions = [
            {
                'type': 'input',
                'name': 'inputName',
                'message': "请输入您想要查看考生的姓名：",
                'validate': StudentNameValidator
            }
        ]

        stuName = ""
        inputName = prompt(questions)['inputName']
        if(inputName == self.stuSet.myName):
            stuName = inputName + self.stuSet.myNameTag
        else:
            stuName = inputName

        dfStu = self.dfStuForSecondRound[self.dfStuForSecondRound["姓名"]==stuName].head(1)
        dfStuBase = dfStu[["姓名", "性别", "类型", "总分", "选取策略"]]
        
        print("考生基本信息：")
        print(GlobalConfig.bcolors.CYAN + tabulate(dfStuBase, showindex="never", headers="keys", tablefmt="rounded_outline") + GlobalConfig.bcolors.ENDC)
        print("\n")

        print("填报的志愿：")
        applyTable = []
        for i in range(0, GlobalConfig.NumShoolToApply):
            schoolCode = dfStu.iloc[0][GlobalConfig.OrderMap[i]]
            if(schoolCode == "None"):
                applyTable.append([GlobalConfig.OrderMap[i], "", ""])
            else:
                schoolName = self.dfSchools[self.dfSchools["学校代码"]==schoolCode]["学校名称"].iloc[0]
                applyTable.append([GlobalConfig.OrderMap[i], schoolCode, schoolName])

        print(GlobalConfig.bcolors.CYAN + tabulate(applyTable, showindex="never", tablefmt="rounded_grid") + GlobalConfig.bcolors.ENDC)
        print("\n")

        print("录取结果：")
        if(dfStu.iloc[0]["已经录取"] == False):
            print(GlobalConfig.bcolors.CYAN + "遭遇滑档，录取失败" + GlobalConfig.bcolors.ENDC)
        else:
            admitOrder = dfStu.iloc[0]["录取志愿"]
            admitCode = dfStu.iloc[0]["录取学校代码"]
            admitName = self.dfSchools[self.dfSchools["学校代码"]==admitCode]["学校名称"].iloc[0]
            admitTable = [[admitOrder, admitCode, admitName]]
            admitHeaders = ["录取志愿", "学校代码", "学校名称"]
            print(GlobalConfig.bcolors.CYAN + tabulate(admitTable, showindex="never", headers=admitHeaders, tablefmt="rounded_grid") + GlobalConfig.bcolors.ENDC)
        return