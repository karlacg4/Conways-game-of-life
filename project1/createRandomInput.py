import random

f = open("input5.txt", "w")
w = 100
f.write("{} {}\n".format(w, w))
f.write("200\n")
for i in range(2000):
    f.write("{} {}\n".format(random.randint(0, w-1), random.randint(0, w-1)))