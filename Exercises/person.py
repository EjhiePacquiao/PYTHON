'''
	Person class
'''
class Person:
    def __init__(self,lastname:str,firstname:str)->None:
        self.lastname = lastname
        self.firstname = firstname
    def setlastname(self,lastname:str)->None: 
        self.lastname = lastname
    def setfirstname(self,firstname:str)->None: 
        self.firstname = firstname
    def getlastname(self)->None:
        return self.lastname
    def getfirstname(self)->None: 
        return self.firstname
    def __str__(self)->str:
        return f"{self.lastname.upper():<15} {self.firstname.upper():<15}"