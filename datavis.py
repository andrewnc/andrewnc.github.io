#datavis.py
import numpy as np
import string
import itertools
words = {}

letter = string.ascii_lowercase
letters = set()
for i in letter:
	letters.add(str(i))

count = {}
with open("constitution.txt") as f:
	for word in f:
		for char in word:
			if char in letters:
				if char not in count.keys():
					count[str(char)] = 1
				else:
					count[str(char)] += 1

total = 0
let = []
for i in count:
	let.append(i)
	total += count[i]

let = sorted(let)


# for i in sorted(count.keys()):
# 	print "<tr><td>"+str(i) +"</td><td>"+ "{:.2f}".format(float(count[i])/float(total)*100)+"</td></tr>"



li = set()

letters = list(letters)
li_1 = itertools.permutations(letters,2)

for i in list(li_1):
	li.add(str(i))

with open("constitution.txt") as f:
	for word in f:
		for i in xrange(len(word)):
			if i != (len(word) - 1):
				tup = str((word[i],word[i+1]))
			if tup in li:
				if tup not in words.keys():
					words[tup] = 1
				else:
					words[tup] += 1
links = []
letters = sorted(letters)
for key in sorted(words.keys()):
	links.append({"source":int(letters.index(key[2])),"target":int(letters.index(key[7])),"weight":(int(words[key]))/100.})
	print "<tr><td>"+str(key[2]) + str(key[7]) +"</td><td>"+ str(int(words[key]))+"</td></tr>"


with open('data.txt','w') as f:
	for i in links:
		i = str(i)
		string.replace(i,'\'','\"')
		f.write(i + ",\n")
	# f.write(str(links))








