print("Welcome to the birthday dictionary. We know the birthdays of: \n Albert Einstein\n Benjamin Franklin\n Ada Lovelace")
names_birth = {"Albert Einstein": "09/06/2003", "Benjamin Franklin": "01/17/1706", "Ada Lovelace": "03/25/1978"}
who = input("Who’s birthday do you want to look up? ")
print(who + "'s birthday is " + names_birth[who])