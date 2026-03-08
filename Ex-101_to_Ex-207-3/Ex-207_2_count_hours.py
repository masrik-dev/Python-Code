'''
10.2 Write a program to read through the mbox-short.txt and figure out the
distribution by hour of the day for each of the messages. You can pull the hour
out from the 'From ' line by finding the time and then splitting the string a
second time using a colon.
From stephen.marquard@uct.ac.za Sat Jan  5 09:14:16 2008
Once you have accumulated the counts for each hour, print out the counts,
sorted by hour as shown below.
'''
# my code

name = input("Enter file: ")

if len(name) < 1:
    name = "mbox-short.txt"

handle = open(name)

counts = dict()

for line in handle:
    line = line.rstrip()
    if not line.startswith("From "):
        continue
    words = line.split()
    word = words[5]
    w = word.split(":")
    h = w[0]
    counts[h] = counts.get(h,0)+1

l = list()
for k,v in counts.items():
    tup = (k,v)
    l.append(tup)
    lst = sorted(l)
for k,v in lst:
    print("The hour: ", k, "The number of times: ", v)
print("Total number of email hours: ",len(lst))