import config.config as GlobalConfig

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
        #dfSchools, 增加column用于跟踪投档名额：
        self.dfSchools["统招余额"] = self.dfSchools.apply(lambda row: row['5+2区域统招'] - row['指标到校'] - row["民办校内指标到校"] - row["全市艺体"], axis=1)
        self.dfSchools["调剂余额"] = self.dfSchools.apply(lambda row: row['5+2区域调剂'], axis=1)

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
    def studentsPK(self, dfGroupedStudents, quotaRemain):
        dfGroupedStudents["partialTotal"] = dfGroupedStudents["语文"] + dfGroupedStudents["数学"] + dfGroupedStudents["英语"]
        dfGroupedStudents = dfGroupedStudents.sort_values(by="partialTotal", ascending=False)

        dfGroupedStudents = dfGroupedStudents.head(quotaRemain)
        dfGroupedStudents.drop(columns="partialTotal", inplace=True)
        return dfGroupedStudents
    

    #对学生进行投档
    #score: 当前投档分数段
    #applyOrder： 第几志愿
    #schoolCode 当前填报的学校代码
    #dfGroupedStudents: 在该分数段下，当前志愿里填写该学校的学生集
    def dispatchToSchoolWithApplyOrder(self, score, applyOrder, schoolCode, dfGroupedStudents):
        #1,3,5,7查看统招余额，2，4，6查看调剂余额：
        orderType = ""
        if(applyOrder % 2 == 0):
            orderType = "统招"
        else:
            orderType = "调剂"
        
        quotaRemain = self.dfSchools.loc[self.dfSchools["学校代码"]==schoolCode, "{}余额".format(orderType)].values[0]
        if(quotaRemain == 0):
            return
        
        stuRemain = len(dfGroupedStudents)

        if(quotaRemain >= stuRemain):
            #学校录取剩余名额大于填报学校的学生数，则所有学生录取:
            self.numStudentsAdmitted += stuRemain
            self.finalAdmitStats[GlobalConfig.OrderMap[applyOrder]] += stuRemain

            #更新学校剩余招收名额：
            self.dfSchools.loc[self.dfSchools["学校代码"]==schoolCode, "{}余额".format(orderType)] = quotaRemain - stuRemain

            #更新学生记录：
            dfGroupedStudents["已经录取"] = True
            self.dfStuForSecondRound.loc[self.dfStuForSecondRound["姓名"].isin(dfGroupedStudents["姓名"]), "已经录取"] = True
            self.dfStuForSecondRound.loc[self.dfStuForSecondRound["姓名"].isin(dfGroupedStudents["姓名"]), "录取志愿"] = GlobalConfig.OrderMap[applyOrder]
            self.dfStuForSecondRound.loc[self.dfStuForSecondRound["姓名"].isin(dfGroupedStudents["姓名"]), "录取学校代码"] = schoolCode

            return
        else:
            dfWinningStudents = self.studentsPK(dfGroupedStudents, quotaRemain)
            self.numStudentsAdmitted += quotaRemain
            self.finalAdmitStats[GlobalConfig.OrderMap[applyOrder]] += quotaRemain

            #更新学校剩余招收名额：
            self.dfSchools.loc[self.dfSchools["学校代码"]==schoolCode, "{}余额".format(orderType)] = 0

            #更新学生记录：
            dfWinningStudents["已经录取"] = True
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
                    self.dispatchToSchoolWithApplyOrder(score, i, schoolCode, dfGroupedStudents)
        return
    

    def coreProcess(self):
        dfStudentsToDispatch = self.dfStuForSecondRound.copy()
        #655分以上同学统一处理：
        dfTopStudents = dfStudentsToDispatch[dfStudentsToDispatch['总分'] >= GlobalConfig.ScoreTopGate]
        self.studentsDispatch(dfTopStudents, GlobalConfig.ScoreTopGate)

        #从高分到省重线分，依次投档：
        for i in range(GlobalConfig.ScoreTopGate-1, self.stuSet.privilegeScoreGate-1, -1):
            dfStudents = dfStudentsToDispatch[dfStudentsToDispatch['总分'] == i]
            self.studentsDispatch(dfStudents, i)
        return