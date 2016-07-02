#!/usr/bin/env python
#coding:utf-8

import string
from copy import deepcopy

ROW = "ABCDEFGHI";
COL = "123456789";

# utility function to print each sudoku
def printSudoku(sudoku):
	print "-----------------"
	for i in ROW:
		for j in COL:
			print sudoku[i + j],
		print ""	

def outputSudoku(sudoku, f):
	f.write("-----------------\n")
	for i in ROW:
		for j in COL:
			f.write(str(sudoku[i + j])+" "),
		f.write("\n")

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
		if i != var and sudo[i] == 0:
			candidate.append(i)

	for i in allcol:
		if i not in candidate and i != var and sudo[i] == 0:
			candidate.append(i)

	for i in allrow:
		if i not in candidate and i != var and sudo[i] == 0:
			candidate.append(i)
	
	return [(var, x) for x in candidate], [(x, var) for x in candidate]		


def remove_inconsistant(i, j, d_avail):
	removed = False
	avail_list = list(d_avail[i])[::]
	for x in avail_list:
		if len(d_avail[j]) == 1 and list(d_avail[j])[0] == x:
			removed = True
			avail_list.remove(x)
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

	while(len(queue) > 0):
		i,j = queue.pop(0)

		if remove_inconsistant(i, j, d_avail):
			queue += get_arcs(i, sudo)[1] # others -> i

	for x in d_avail:
		if len(d_avail[x]) != 1:
			return False
	return True	

def getMRV(candlist, d_avail):
	#print candlist
	tmp = sorted(candlist, key=lambda x: len(d_avail[x]))
	return tmp[0]

def update_avail(d_avail, sudo): 
	for i in sudo:
		if sudo[i] == 0:
			d_avail[i] = get_availale(i, sudo)

def recursive_backtracking(sudo, candlist, d_avail):
	if len(candlist) == 0: # All variables assigned
		return sudo
	variable = getMRV(candlist, d_avail)
	avails = get_availale(variable, sudo)
	for value in avails:
		new_sudo = deepcopy(sudo)
		new_sudo[variable] = value
		new_candlist = candlist[::]
		new_candlist.remove(variable) 
		new_d_avail = deepcopy(d_avail)
		update_avail(new_d_avail, sudo)  # Forward checking
		del new_d_avail[variable]
		
		result = recursive_backtracking(new_sudo, new_candlist, new_d_avail)
		if result != None:
			return result
	return None		

def backtracking(sudo):
	d_avail = {}
	unassigned = []
	for i in sudo:
		if sudo[i] == 0:
			d_avail[i] = get_availale(i, sudo)
			unassigned.append(i)

	return recursive_backtracking(sudo, unassigned, d_avail)


def evaluate(var, sudo):
	available = set(range(1,10))
	square = get_square_checklist(var)
	allcol = [var[0]+str(x) for x in range(1,10)]
	allrow = [x+var[1] for x in string.uppercase[:9]]
	for i in square:
		if i != var:
			available.discard(sudo[i])

	for i in allcol:
		if i != var:
			available.discard(sudo[i])

	for i in allrow:
		if i != var:
			available.discard(sudo[i])		

	return available

def evaluate_sudoku(sudo):
	for i in sudo:
		if len(evaluate(i, sudo)) != 1:
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
solvable = []
i = 0
for line in sudokuList.split("\n"):
	# Parse sudokuList to individual sudoku in dict, e.g. sudoku["A2"] = 1
	sudoku = {ROW[i] + COL[j]: int(line[9*i+j]) for i in range(9) for j in range(9)}
	i += 1
	if ac3(sudoku) == True:
		num_ac3_solved += 1
		solvable.append(i)
		

print "num_ac3_solved:",num_ac3_solved, solvable	

	# write your AC3 algorithms here, update num_ac3_solved	

# 1.6 solve all sudokus by backtracking
success = 0
fail = 0
f = open('output_cw2952.txt','w')
for line in sudokuList.split("\n"):
	# Parse sudokuList to individual sudoku in dict, e.g. sudoku["A2"] = 1
	sudoku = {ROW[i] + COL[j]: int(line[9*i+j]) for i in range(9) for j in range(9)}

	# write your backtracking algorithms here
	sudoku = backtracking(sudoku)
	if evaluate_sudoku(sudoku) == True:
		success += 1
	else:
		fail += 1	
	printSudoku(sudoku)
	outputSudoku(sudoku, f)
print "Success:",success,", Fail:", fail	