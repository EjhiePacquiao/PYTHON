'''
	Student class
'''
from person import Person
class Student(Person):
    def __init__(self,idno:str,lastname:str,firstname:str,course:str,level:str)->None:
        super().__init__(lastname,firstname)
        self.idno = idno
        self.course = course
        self.level = level
    def setidno(self,idno:str)->str:
        self.idno = idno
    def setcourse(self,course:str)->str:
        self.course = course
    def setlevel(self,level:str)->str:
        self.level = level
    def getidno(self)->str:
        return self.idno
    def getcourse(self)->str:
        return self.course
    def getlevel(self)->str:
        return self.level
    def __str__(self)->str:
        return f" {self.idno:<10} {super().__str__()} {self.course.upper():<10} {self.level:>10}"