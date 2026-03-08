'''
7.2 Write a program that prompts for a file name, then opens that file and
reads through the file, looking for lines of the form:
X-DSPAM-Confidence:    0.8475

file name: mbox-short.txt

'''
fname = input("Enter file name:")
fh = open(fname)
count = 0
add = 0
for line in fh:
    if not line.startswith ("X-DSPAM-Confidence:"):
        continue
    count += 1
    char = line.find(':')
    numb = line[char+1:]
    num = numb.strip()
    add += float(num)
print("Average spam confidence:", add/count)