from os import listdir
from os.path import isdir, join

path = "/Users/Xiaohu/Documents/reading/library"

dirs = [f for f in listdir(path) if isdir(join(path, f))]

with open("authorlist.txt", "w") as f:
	for d in dirs:
		f.write(d + "\n")
