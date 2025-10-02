'''
read a file "romeo.txt" and read it. then count words and list them in alphabetical order.

'''

file_name = input("Enter file name: ")
file_handel = open(file_name)
list_words = list()
for lines in file_handel:
    line = lines.rstrip()
    words = line.split()
    for word in words:
        if word in list_words:
            continue
        else:
            list_words.append(word)

list_words.sort()
print(list_words)
print("Total words number: ", len(list_words))