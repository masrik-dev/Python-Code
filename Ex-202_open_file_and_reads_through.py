'''
Open file and reads through the file.

'''

fname = input("Enter file name:")
fh = open(fname)
f = fh.read()
final = f.upper().rstrip()
print(final)