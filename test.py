#!/usr/bin/env python3
import re
import sys
import itertools

def needToUpdate(one, two):
	#one="v2.0.0"
	#two="v3"
	cleanedValue = re.sub(r'[a-zA-Z]',"",one.strip())
	split=cleanedValue.split(".")
	cleanedValueTwo = re.sub(r'[a-zA-Z]',"",two.strip())
	splitTwo=cleanedValueTwo.split(".")
	
	try:
		numericOne=list(map(int,split))
		numericTwo=list(map(int,splitTwo))
	except ValueError:
		return False
		#sys.exit(1)

	#print(f"{one} -> {two}")
	#print(f"----------")
	#print(f"{split}")
	#print(f"{splitTwo}")
	#print(f"{list(itertools.zip_longest(split, splitTwo))}")
	#print(f"{list(itertools.zip_longest(numericOne, numericTwo))}")


	# go through each value
	# from FIRST to last 
	# if ever there is a number greater than STOP and YES it must
	# be out of date
	# OTherwise move on
	currentResult=False
	for i in list(itertools.zip_longest(numericOne, numericTwo)):
		a, b=i
		if a != None and b != None:
			if a < b:
				print(f"version {one} is lower than {two}")
				currentResult=True
				break
	return currentResult


a=needToUpdate("v2.0.0","v3")
b=needToUpdate("v4.0.0","v3")
c=needToUpdate("v3.0.0","v3")
d=needToUpdate("v2.3.5","v3.0.0")
e=needToUpdate("abc","v3.0.0")
print(f"a = {a}")
print(f"b = {b}")
print(f"c = {c}")
print(f"d = {d}")
print(f"e = {e}")
