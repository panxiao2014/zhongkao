#中考成绩规则：
#语，数，外：满分150
#物理：满分70
#化学：满分50
#体育：满分60
#道法，历史，生物，地理：20, 16, 12, 8, 0
#满分: 710

import random
import numpy as np
import pandas as pd
import scipy.stats as ss

MaxScore = 149
MinScore = 30

MeanRange = 10
ScaleRange = 4
SkewRange = 1

ChineseMean = 110
ChineseScale = 15
ChineseSkew = -1

MathMean = 115
MathScale = 30
MathSkew = -2

class ScoreGen:
    def __init__(self):
        return
    
    def scoreChinese(self, stuNumber):
        scores = ss.pearson3.rvs(loc=random.randint(ChineseMean-MeanRange, ChineseMean+MeanRange), 
                                 scale=random.randint(ChineseScale-ScaleRange, ChineseScale+ScaleRange), 
                                 skew=random.randint(ChineseSkew-SkewRange, ChineseSkew+SkewRange),  
                                size=stuNumber)
        
        dfChinese = pd.DataFrame({"语文": scores})
        dfChinese["语文"] = dfChinese["语文"].astype(int)
        dfChinese["语文"] = np.where(dfChinese["语文"]<MinScore, MinScore, dfChinese["语文"])
        dfChinese["语文"] = np.where(dfChinese["语文"]>MaxScore, MaxScore, dfChinese["语文"])
        
        return dfChinese
    
    
    def scoreMath(self, stuNumber):
        scores = ss.pearson3.rvs(loc=random.randint(MathMean-MeanRange, MathMean+MeanRange), 
                                 scale=random.randint(MathScale-ScaleRange, MathScale+ScaleRange), 
                                 skew=random.randint(MathSkew-SkewRange, MathSkew+SkewRange),  
                                size=stuNumber)
        
        dfChinese = pd.DataFrame({"数学": scores})
        dfChinese["数学"] = dfChinese["数学"].astype(int)
        dfChinese["数学"] = np.where(dfChinese["数学"]<MinScore, MinScore, dfChinese["数学"])
        dfChinese["数学"] = np.where(dfChinese["数学"]>MaxScore, MaxScore, dfChinese["数学"])
        
        return dfChinese
