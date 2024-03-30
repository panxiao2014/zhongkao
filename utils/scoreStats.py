import pandas as pd

class ScoreStats:
    def __init__(self):
        scoreDf = pd.read_excel('data/score.stats.2023.xlsx')
        print(scoreDf)