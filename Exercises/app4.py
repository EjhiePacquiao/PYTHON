#command to repeat a character in the screen
# for i in range(0,160):
	# print("-",end="")
# print()
from os import system
system("cls")
print("."*76)
#command to display a string at the center
message:str = "Hello world"
print(message.center(76,"*"))


