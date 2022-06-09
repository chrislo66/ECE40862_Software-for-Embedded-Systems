class Program5:
    def __init__(self, list_num):
        self.list_num = list_num
    def equal(self, target):
        self.target = target
        found = 0
        for idx1 in range(len(self.list_num)):
            for idx2 in range(len(self.list_num)):
                if idx2 != idx1:
                    calc = self.list_num[idx1] + self.list_num[idx2]
                    if calc == int(target):
                        print("index1 = " + str(idx1) + ", " + "index2 = " + str(idx2))
                        found = 1
            break

        if found == 0:
            print("No any two numbers in the given list can sum up to your target number.")


list_num = [10,20,10,40,50,60,70]
target = input("What is your target number? ")
Program5(list_num).equal(int(target))


