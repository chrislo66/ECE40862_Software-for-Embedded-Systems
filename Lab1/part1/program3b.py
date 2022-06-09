from random import randint

value = randint(0,10)
print(value)
num_guess = 0
correct = 0
while num_guess < 3 and correct == 0:
    guess = input("Enter your guess: ")
    if int(guess) == value:
        print("You win!")
        correct = 1
    else:
        num_guess += 1

if num_guess == 3 and correct == 0:
    print("You lose!")

