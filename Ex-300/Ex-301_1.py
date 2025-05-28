import re

name = input("Enter file name: ")
hand = open(name)

#sum1 = 0
numlist = list()
for line in hand:
    line = line.rstrip()
    stuff = re.findall('[0-9]+',line)
    for num in stuff:
        num = num.rstrip()
        if len(num) <= 0: continue
        num = int(num)
        numlist.append(num)
    #sum1 = sum1 + num
    #print(stuff)

print(numlist)
print(len(numlist))
print(sum(numlist))
#print(sum3)
#print(sum1)
