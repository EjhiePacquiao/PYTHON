"""
	A program that would accept two(2) integers and display the product,quotient,sum and difference
"""
from os import system

system("cls")
#input two(2) integers
try:
    value1:int = int(input("Enter first value :"))
    value2:int = int(input("Enter second value:"))
    #process the inputs
    product:int = value1*value2
    quotient:float = value1/value2
    sum:int = value1+value2
    difference:int = value1-value2

    #display the results
    print(f"the product of {value1} and {value2} is {product}")
    print(f"the quotient of {value1} and {value2} is {quotient:.4f}")
    print(f"the sum of {value1} and {value2} is {sum}")
    print(f"the difference of {value1} and {value2} is {difference}")
except:
    print("Invalid Input")
