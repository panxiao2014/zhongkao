#根据score.stats.2023.xlsx，只模拟考分500及以上的学生。500以下无法达到重高线，没有模拟的必要：
StudentTotal = 20385
ScoreBottomGate = 500

#调剂生数量没有资料。根据5+2区域公布的调剂指标，暂定为低于指标总数4630：
EdgeStudentTotal = 3000

#市直属指标到校总数：
CityQuotaTotal = 1732

#艺体生总数：
TalentQuotaTotal = 1744

#所有考生姓名：
StuNameLst = []

#所有学校的代码：
LstSchoolCode = []

ScoreTopGate = 655  #655及以上得分合并统计总人数


#填报志愿数：
NumShoolToApply = 7
OrderMap = {0: "第一志愿", 1: "第二志愿", 2: "第三志愿", 3: "第四志愿", 4: "第五志愿", 5: "第六志愿", 6: "第七志愿"}

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