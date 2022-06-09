number = input("How many Fibonacci numbers of would you like to generate? ")
list = [1,1]
while len(list) < int(number):
    list.append(list[-1] + list[-2])
print("The Fibonacci Sequence is: " + ", ".join(repr(element) for element in list))