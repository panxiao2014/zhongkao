import pandas as pd

class SchoolStats:
    def __init__(self):
        schoolDf = pd.read_excel('data/schools.2023.xlsx')
        return