'''
8.5 Open the file mbox-short.txt and read it line by line. When you find a line
that starts with 'From ' like the following line:
From stephen.marquard@uct.ac.za Sat Jan  5 09:14:16 2008
You will parse the From line using split() and print out the second word in the
line (i.e. the entire address of the person who sent the message). Then print
out a count at the end.
Hint: make sure not to include the lines that start with 'From:'.

'''

file_name = input("Enter file name: ")
file_handel = open(file_name)
count = 0
for lines in file_handel:
    line = lines.strip()
    if not line.startswith("From "):
        continue
    else:
        count = count + 1
        words = line.split()
        print(words[1])

print("There are", count, "lines in the file with 'Form' as the first word")
