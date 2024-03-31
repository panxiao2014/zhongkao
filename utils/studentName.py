import random

class StudentName:
    def __init__(self):
        self.nameDatabase = []
        self.nameList = []

        with open('data/names.txt', 'r', encoding='utf-16') as f:
            fContent = f.readlines()
            for line in fContent:
                name,sex = line.split(',')
                self.nameDatabase.append({"姓名": name, "性别": sex.rstrip()})

        random.shuffle(self.nameDatabase)
        return

    def printAll(self):
        for item in self.nameList:
            print(item)

        return
    
    def listAll(self):
        return self.nameList
    
    
    def cerateStudentNames(self, stuNumber):
        for i in range(0, stuNumber):
            self.nameList.append(self.nameDatabase[i])

        return self.nameList
    
    def addStudent(self, stuName, stuGender):
        self.nameList.append({"name": stuName, "gender": stuGender})
        return