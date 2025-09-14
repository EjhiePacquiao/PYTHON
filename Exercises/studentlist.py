'''
    StudentList
'''
from student import Student

class StudentList:
    def __init__(self, size: int) -> None: 
        self.slist = []  # data container
        self.size = size
        
    # sentinel methods
    def isempty(self) -> bool:    
        return len(self.slist) == 0
    
    def isfull(self) -> bool:     
        return len(self.slist) == self.size
    
    # utility methods
    def addstudent(self, s: Student) -> bool:
        if self.isfull():
            print("\nList is full. Cannot add student.")
            return False
        # prevent duplicate IDs
        if self.findstudent(s.getidno()):
            print(f"\nError: A student with ID {s.getidno()} already exists.")
            return False
        self.slist.append(s)
        return True
        
    def findstudent(self, idno: str):
        idno = idno.strip()
        if not self.isempty():
            for student in self.slist:
                if student.getidno() == idno:
                    return student
        return None

    def deletestudent(self, idno: str) -> bool:
        student = self.findstudent(idno)
        if student is not None:
            self.slist.remove(student)
            return True
        return False

    def updatestudent(self, s: Student) -> bool:
        student = self.findstudent(s.getidno())
        if student is not None:
            index = self.slist.index(student)
            self.slist[index] = s
            return True
        return False
        
    def showlist(self) -> None:
        if not self.isempty():
            for student in self.slist:
                print(student)
        else:
            print("No students in the list.")
