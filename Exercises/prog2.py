'''
	A program that would accept one(1) integer value not greater than 20, compute the factorial of the value using iterative solution

	example:
	input(1..20): 5
	120
'''
from os import system

fact:int = 1
try:
    system('cls')
    n:int = int(input("Enter value (1..20):"))
    #input validation
    if n>0 and n<=20:
        for i in range(1,n+1):
            fact*=i
        print(f"The factorial of {n} is {fact}")
    else:
        print("accept only 1 to 20")
except Exception as e:
    print(f"Invalid input: {e}")