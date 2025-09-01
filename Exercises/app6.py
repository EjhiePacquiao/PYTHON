'''
	A program that would display the menu shown
	----- Main Menu -----
	1. Multiply
	2. Divide
	3. Add
	4. Subtract
	0. Quit/End
	---------------------
	Enter Option(0..5): <---prompt
	provide modules(function) for each operation of the menu,
	name the modules accordlingly
'''
from os import system
#
def displaymenu()->None:
    system("cls")
    print("---- Main Menu ----") # print("Main Menu.center(19,'-')")
    print("1. Multiply")
    print("2. Divide")
    print("3. Add")
    print("4. Subtract")
    print("0. Quit/End")
    print("-"*19)
    
def inputvalue()->None:
    a:int = int(input("Enter first  value:"))
    b:int = int(input("Enter Second value:"))
    return a,b
    
def multiply()->None:
    system("cls")    
    print("Multiply".center(19,"-"))
    a,b = inputvalue()
    print(f"The product of {a} and {b} is {(a*b)}")
    
def divide()->None:
    system("cls")
    print("Divide".center(19,"-"))    
    a,b = inputvalue()
    print(f"The quotient of {a} and {b} is {(a/b)}")
def add()->None:
    system("cls")
    print("Add".center(19,"-"))
    a,b = inputvalue()
    print(f"The sum of {a} and {b} is {(a+b)}")
def subtract()->None:
    system("cls")
    print("Subtract".center(19,"-"))
    a,b = inputvalue()
    print(f"The difference of {a} and {b} is {(a-b)}")
    
def quit()->None:
    print("Program ended...")

def main()->None:
    option:str = ""
    while option!="0":
        displaymenu()
        option=input("Enter option(0..5):")
        match option:
            case "1":multiply()
            case "2":divide()
            case "3":add()
            case "4":subtract()
            case "0":quit()
            case   _:print("Invalid Option")
        input("Press any key to continue...")

if __name__=="__main__": #the launcher block
    main()


