import pandas as pd

class ScoreStats:
    def __init__(self):
        self.dfScore = pd.read_excel('data/score.stats.2023.xlsx')
        return