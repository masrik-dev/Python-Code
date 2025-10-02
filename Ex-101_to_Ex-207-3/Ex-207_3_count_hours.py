name = input("Enter file name: ")
if len(name) < 1:
    name = "mbox-short.txt"
handle = open(name)

counts = dict()
lst = list()
for line in handle:
    line = line.rstrip()
    if not line.startswith("From "):
        continue
    words = line.split()
    word = words[5]
    w = word.split(":")
    h = w[0]
    for h in lst:
        if h in lst:
            continue
        else:
            lst.append(h)
    counts[h] = counts.get(h,0)+1

print(counts, lst)

# Bad code: lst is not working