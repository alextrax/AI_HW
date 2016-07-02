#!/usr/bin/env python
#coding:utf-8

import string

ROW = "ABCDEFGHI";
COL = "123456789";

# utility function to print each sudoku
def printSudoku(sudoku):
	print "-----------------"
	for i in ROW:
		for j in COL:
			print sudoku[i + j],
		print ""	


def get_square_checklist(var):
	if var[0] == 'A' or var[0] == 'B' or var[0] == 'C':
		rowindex = ['A', 'B', 'C']
	elif var[0] == 'D' or var[0] == 'E' or var[0] == 'F':
		rowindex = ['D', 'E', 'F']
	else:	
		rowindex = ['G', 'H', 'I']

	if var[1] == '1' or var[1] == '2' or var[1] == '3':
		colindex = ['1', '2', '3']
	elif var[1] == '4' or var[1] == '5' or var[1] == '6':
		colindex = ['4', '5', '6']
	else:	
		colindex = ['7', '8', '9']	

	return ["".join((x, y)) for x in rowindex for y in colindex]

def get_availale(var, sudo):
	available = set(range(1,10))
	square = get_square_checklist(var)
	allcol = [var[0]+str(x) for x in range(1,10)]
	allrow = [x+var[1] for x in string.uppercase[:9]]
	for i in square:
		available.discard(sudo[i])

	for i in allcol:
		available.discard(sudo[i])

	for i in allrow:
		available.discard(sudo[i])		

	return available

def get_arcs(var, sudo): # return var->others and others->var
	candidate = []
	square = get_square_checklist(var)
	allcol = [var[0]+str(x) for x in range(1,10)]
	allrow = [x+var[1] for x in string.uppercase[:9]]
	for i in square:
		if i != var: #sudo[i] == 0:
			candidate.append(i)

	for i in allcol:
		if i not in candidate and i != var:
			candidate.append(i)

	for i in allrow:
		if i not in candidate and i != var:
			candidate.append(i)
	
	return [(var, x) for x in candidate], [(x, var) for x in candidate]		


def remove_inconsistant(i, j, d_avail):
	removed = False
	avail_list = list(d_avail[i])[::]
	#print i,j,avail_set
	for x in avail_list:
		if len(d_avail[j]) == 1 and list(d_avail[j])[0] == x:
			removed = True
			#print i, avail_list, j, d_avail[j]
			avail_list.remove(x)
			#print "remove", x
	d_avail[i] = set(avail_list)
	return removed

def ac3(sudo):
	queue = []
	d_avail = {}

	for i in sudo:
		if sudo[i] != 0:
			d_avail[i] = set([sudo[i]])
		else:
			queue += get_arcs(i, sudo)[0]
			queue += get_arcs(i, sudo)[1]
			d_avail[i] = get_availale(i, sudo)	

	'''
	for i in d_avail:
		if len(d_avail[i]) > 1:
			sudo[i] = d_avail[i].pop()
			d_avail[i] = set([sudo[i]])
			break
	'''

	while(len(queue) > 0):
		i,j = queue.pop(0)

		if remove_inconsistant(i, j, d_avail):
			queue += get_arcs(i, sudo)[1] # others -> i

	for x in d_avail:
		if len(d_avail[x]) != 1:
			return False
	return True	

# Reading of sudoku list from file
try:
    f = open("sudokus.txt", "r")
    sudokuList = f.read()
except:
	print "Error in reading the sudoku file."
	exit()

# 1.5 count number of sudokus solved by AC-3
num_ac3_solved = 0
for line in sudokuList.split("\n"):
	# Parse sudokuList to individual sudoku in dict, e.g. sudoku["A2"] = 1
	sudoku = {ROW[i] + COL[j]: int(line[9*i+j]) for i in range(9) for j in range(9)}
	if ac3(sudoku) == True:
		num_ac3_solved += 1

print "num_ac3_solved:",num_ac3_solved	

	# write your AC3 algorithms here, update num_ac3_solved	

# 1.6 solve all sudokus by backtracking
#for line in sudokuList.split("\n"):
	# Parse sudokuList to individual sudoku in dict, e.g. sudoku["A2"] = 1
	#sudoku = {ROW[i] + COL[j]: int(line[9*i+j]) for i in range(9) for j in range(9)}

	# write your backtracking algorithms here

	#printSudoku(sudoku)