a = [1,1,2,3,5,8,13,21,34,55,89]
print(a)
number = input("Enter number: ")
b = []
for i in range(len(a)):
    if a[i] < int(number):
        b.append(a[i])
print("The new list is " + str(b))

