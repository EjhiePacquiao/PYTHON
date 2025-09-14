'''
    Pacquiao, Ejhie
    Center
'''

from os import system
from studentlist import StudentList
from student import Student

slist = StudentList(10)

def displaymenu()->None:
    system('cls')
    for i in range(1,5): print(" "*73)    
    print("       MAIN MENU        ".center(73," "))
    print(" -----------------------".center(73," "))
    print(" 1. ADD STUDENT         ".center(73," "))
    print(" 2. FIND STUDENT        ".center(73," "))
    print(" 3. DELETE STUDENT      ".center(73," "))
    print(" 4. UPDATE STUDENT      ".center(73," "))
    print(" 5. DISPLAY ALL STUDENT ".center(73," "))
    print(" 0. QUIT/END            ".center(73," "))
    print(" -----------------------".center(73," "))


def addstudent()->None:
    system('cls')
    for i in range(1,5): print(" "*73)
    print("Add Student".center(73))
    print("----------------------".center(73))

    # IDNO numbers only
    while True:
        print(" "*25, end="")
        idno = input("IDNO      : ").strip()
        if not idno.isdigit():
            print(" "*25 + "Invalid input! IDNO must be numbers only.")
            continue
        if slist.findstudent(idno):
            print(" "*25 + f"Error: A student with ID {idno} already exists. Please enter a different ID.")
            continue
        break

    # LASTNAME letters only
    while True:
        print(" "*25, end="")
        lastname = input("LASTNAME  : ").strip()
        if lastname.isalpha():
            break
        print(" "*25 + "Invalid input! LASTNAME must contain letters only.")

    # FIRSTNAME letters only
    while True:
        print(" "*25, end="")
        firstname = input("FIRSTNAME : ").strip()
        if firstname.isalpha():
            break
        print(" "*25 + "Invalid input! FIRSTNAME must contain letters only.")

    # COURSE letters only
    while True:
        print(" "*25, end="")
        course = input("COURSE    : ").strip()
        if course.isalpha():
            break
        print(" "*25 + "Invalid input! COURSE must contain letters only.")

    # LEVEL numbers only, between 1–5
    while True:
        print(" "*25, end="")
        level = input("LEVEL     : ").strip()
        if level.isdigit() and 1 <= int(level) <= 5:
            break
        print(" "*25 + "Invalid input! LEVEL must be a number between 1 and 5.")

    # Add student
    ok: bool = slist.addstudent(Student(idno, lastname, firstname, course, level))
    if ok:
        print(" "*25 + "Student added successfully.")
    else:
        print(" "*25 + "Failed to add student.")


def findstudent()->None:
    system('cls')
    print("Find Student".center(73))
    print("----------------------".center(73))
    print(" "*25, end="")
    idno = input("IDNO to find: ").strip()
    student = slist.findstudent(idno)
    if student:
        print(" "*25 + "Student found:\n")
        print(" "*25 + str(student))
    else:
        print(" "*25 + "Student not found.")


def deletestudent()->None:
    system('cls')
    print("Delete Student".center(73))
    print("----------------------".center(73))
    print(" "*25, end="")
    idno = input("IDNO to delete: ").strip()
    ok = slist.deletestudent(idno)
    if ok:
        print(" "*25 + "Student deleted successfully.")
    else:
        print(" "*25 + "Student not found. Nothing deleted.")


def updatestudent()->None:
    system('cls')
    print("Update Student".center(73))
    print("----------------------".center(73))
    print(" "*25, end="")
    idno = input("IDNO to update: ").strip()

    student = slist.findstudent(idno)
    if student is None:
        print(" "*25 + "Student not found.")
        return

    # LASTNAME
    while True:
        print(" "*25, end="")
        lastname = input(f"LASTNAME [{student.getlastname()}]: ").strip()
        if lastname == "" or lastname.isalpha():
            lastname = lastname or student.getlastname()
            break
        print(" "*25 + "Invalid input! LASTNAME must contain letters only.")

    # FIRSTNAME
    while True:
        print(" "*25, end="")
        firstname = input(f"FIRSTNAME [{student.getfirstname()}]: ").strip()
        if firstname == "" or firstname.isalpha():
            firstname = firstname or student.getfirstname()
            break
        print(" "*25 + "Invalid input! FIRSTNAME must contain letters only.")

    # COURSE
    while True:
        print(" "*25, end="")
        course = input(f"COURSE [{student.getcourse()}]: ").strip()
        if course == "" or course.isalpha():
            course = course or student.getcourse()
            break
        print(" "*25 + "Invalid input! COURSE must contain letters only.")

    # LEVEL
    while True:
        print(" "*25, end="")
        level = input(f"LEVEL [{student.getlevel()}]: ").strip()
        if level == "":
            level = student.getlevel()
            break
        if level.isdigit() and 1 <= int(level) <= 5:
            break
        print(" "*25 + "Invalid input! LEVEL must be a number between 1 and 5.")

    new_s = Student(idno, lastname, firstname, course, level)
    if slist.updatestudent(new_s):
        print(" "*25 + "Student updated successfully.")
    else:
        print(" "*25 + "Update failed.")


def displayall()->None:
    system('cls')
    print("- Student List -", end="")
    print("-"*57)
    print()

    # Header row
    header = f"{'IDNO':<10} {'LASTNAME':<15} {'FIRSTNAME':<15} {'COURSE':<10} {'LEVEL':>10}"
    print(header)
    print("-"*65)

    slist.showlist()

    print()
    print("Nothing Follows".center(73,"-"))


# main loop
def main()->None:
    option: str = ""
    while option != "0":
        displaymenu()
        print(" "*25, end="")
        option = input(" Enter Option(0 - 5):   ")
        match option:
            case "1": addstudent()
            case "2": findstudent()
            case "3": deletestudent()
            case "4": updatestudent()
            case "5": displayall()
            case "0": print("Program Ended".center(73))
            case _: print("Invalid Option".center(73))
        print(" ")
        print(" "*25, end="")
        input("press Enter to continue...")


if __name__=="__main__":
    main()
