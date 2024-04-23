#5+2区域报名考生总数。来源于网络搜索：“2022年5+2区域约4.8万考生”
StudentTotal = 50000

#调剂生数量没有资料。根据5+2区域公布的调剂指标，暂定为低于指标总数4630：
EdgeStudentTotal = 3000

#市直属指标到校总数：
CityQuotaTotal = 1732

#所有学校的代码：
LstSchoolCode = []

#艺体生总数：
TalentQuotaTotal = 1744

ScoreTopGate = 655  #655及以上得分合并统计总人数
ScoreLowGate = 400  #400分以下忽略统计

#based on 2023 score stats, define score and number of students as high score students:
HighScoreGate = 560
HighScoreStudents = 13605
HighScoretudentsVariance = 5000

#格式化输出颜色：
class bcolors:
    PINK = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLO = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ENDC = '\033[0m'