import random

class StudentName:
    def __init__(self):
        self.nameDatabase = []
        self.nameList = []

        with open('data/names.txt', 'r', encoding='utf-16') as f:
            fContent = f.readlines()
            for line in fContent:
                name,sex = line.split(',')
                self.nameDatabase.append({"name": name, "gender": sex.rstrip()})

        random.shuffle(self.nameDatabase)
        return

    def listAll(self):
        for item in self.nameList:
            print(item)

        return
    
    def cerateStudentSet(self, stuNumber):
        for i in range(0, stuNumber-1):
            self.nameList.append(self.nameDatabase[i])

        return self.nameList
    
    def addStudent(self, stuName, stuGender):
        self.nameList.append({"name": stuName, "gender": stuGender})
        return