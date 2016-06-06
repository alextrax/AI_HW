import sys
import random
import datetime
import resource
try:
    import Queue as Q  # ver. < 3.0
except ImportError:
    import queue as Q

class node:
	def __init__(self, state):
		self.state = state
		self.up = None
		self.down = None
		self.left = None
		self.right = None
		self.steps = []

def move_up(state, n):
	state_list = state.split(',')
	index = state_list.index("0")
	if index < n: # blank at the top row
		return None
	else:
		state_list[index], state_list[index-n] = state_list[index-n], state_list[index]
		return ",".join(state_list)

def move_down(state, n):
	state_list = state.split(',')
	index = state_list.index("0")
	if (n-1) * n <= index: # blank at the bottom row
		return None
	else:
		state_list[index], state_list[index+n] = state_list[index+n], state_list[index]
		return ",".join(state_list)

def move_left(state, n):
	state_list = state.split(',')
	index = state_list.index("0")
	if index % n == 0: # blank at the left-most column
		return None
	else:
		state_list[index], state_list[index-1] = state_list[index-1], state_list[index]
		return ",".join(state_list)

def move_right(state, n):
	state_list = state.split(',')
	index = state_list.index("0")
	if (index+1) % n == 0: # blank at the right-most column
		return None
	else:
		state_list[index], state_list[index+1] = state_list[index+1], state_list[index]
		return ",".join(state_list)

def bfs(init_state, success_state, n):
	print " <-- BFS search -->"
	init_node = node(init_state)
	d = {init_state:1}
	queue = [init_node]
	max_queue_size = 1
	expended = 0
	has_answer = 0
	start = datetime.datetime.now()
	while(len(queue) > 0):
		if len(queue) > max_queue_size:
			max_queue_size = len(queue)
		current = queue.pop(0)
		if current.state == success_state:
			print "BFS Finished"
			print current.steps 
			print "steps: %d" % len(current.steps)
			end = datetime.datetime.now()
			diff = end - start
			print "elapsed time:", diff.total_seconds() * 1000, "ms"
			print "depth of stack/queue:", len(current.steps)+1
			print "max stack/queue size:", max_queue_size
			print "nodes expanded:", expended
			print "maximum memory usage:", (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1000), "(bytes on OS X, kilobytes on Linux)"
			has_answer = 1
			break
		expended += 1	
		upstate = move_up(current.state, n)
		downstate = move_down(current.state, n)
		leftstate = move_left(current.state, n)
		rightstate = move_right(current.state, n)
		if upstate != None and upstate not in d:
			d[upstate] = 1
			up_node = node(upstate)
			up_node.steps = current.steps[:]
			up_node.steps.append("UP")
			queue.append(up_node)
		if downstate != None and downstate not in d:
			d[downstate] = 1
			down_node = node(downstate)
			down_node.steps = current.steps[:]
			down_node.steps.append("DOWN")
			queue.append(down_node)
		if leftstate != None and leftstate not in d:
			d[leftstate] = 1
			left_node = node(leftstate)
			left_node.steps = current.steps[:]
			left_node.steps.append("LEFT")
			queue.append(left_node)
		if rightstate != None and rightstate not in d:
			d[rightstate] = 1
			right_node = node(rightstate)
			right_node.steps = current.steps[:]
			right_node.steps.append("RIGHT")
			queue.append(right_node)
	if has_answer == 0:
		print "No Successful Way"


def dfs(init_state, success_state, n):
	print " <-- DFS search -->"
	init_node = node(init_state)
	d = {init_state:1}
	stack = [init_node]
	max_stack_size = 1
	expended = 0
	has_answer = 0
	start = datetime.datetime.now()
	while(len(stack) > 0):
		if len(stack) > max_stack_size:
			max_stack_size = len(stack)
		current = stack.pop()
		if current.state == success_state:
			print "DFS Finished"
			print current.steps 
			print "steps: %d" % len(current.steps)
			end = datetime.datetime.now()
			diff = end - start
			print "elapsed time:", diff.total_seconds() * 1000, "ms"
			print "depth of stack/queue:", len(current.steps)+1
			print "max stack/queue size:", max_stack_size
			print "nodes expanded:", expended
			print "maximum memory usage:", (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1000), "(bytes on OS X, kilobytes on Linux)"
			has_answer = 1
			break
		expended += 1
		upstate = move_up(current.state, n)
		downstate = move_down(current.state, n)
		leftstate = move_left(current.state, n)
		rightstate = move_right(current.state, n)
		
		if rightstate != None and rightstate not in d:
			d[rightstate] = 1
			right_node = node(rightstate)
			right_node.steps = current.steps[:]
			right_node.steps.append("RIGHT")
			stack.append(right_node)
		if leftstate != None and leftstate not in d:
			d[leftstate] = 1
			left_node = node(leftstate)
			left_node.steps = current.steps[:]
			left_node.steps.append("LEFT")
			stack.append(left_node)
		if downstate != None and downstate not in d:
			d[downstate] = 1
			down_node = node(downstate)
			down_node.steps = current.steps[:]
			down_node.steps.append("DOWN")
			stack.append(down_node)
		if upstate != None and upstate not in d:
			d[upstate] = 1
			up_node = node(upstate)
			up_node.steps = current.steps[:]
			up_node.steps.append("UP")
			stack.append(up_node)
	if has_answer == 0:
		print "No Successful Way"

def misplaced(a, b, n):
	la = a.split(',')
	lb = b.split(',')
	return sum(la[i] != lb[i] for i in range(len(la)))

def manhattan_distance(a, b, n):
	distance = 0
	la = a.split(',')
	lb = b.split(',')
	for i in range(len(la)):
		if la[i] == '0':
			continue
		index = lb.index(la[i]) 
		ver = abs(i%n - index%n) 
		hor = abs(i/n - index/n)	
		distance = distance + ver + hor
	return distance	

def a_star(init_state, success_state, n, heuristic):
	print " <-- A* search -->"
	init_node = node(init_state)
	d = {init_state:1}
	queue = Q.PriorityQueue()
	distance = 0 + heuristic(init_state, success_state, n)
	queue.put((distance, init_node))
	max_queue_size = 1
	expended = 0
	has_answer = 0
	start = datetime.datetime.now()
	while not queue.empty():
		if queue.qsize() > max_queue_size:
			max_queue_size = queue.qsize()
		distance, current = queue.get()
		if current.state == success_state:
			print "A* Finished"
			print "Heuristic method:", heuristic.__name__
			print current.steps 
			print "steps: %d" % len(current.steps)
			end = datetime.datetime.now()
			diff = end - start
			print "elapsed time:", diff.total_seconds() * 1000, "ms"
			print "depth of stack/queue:", len(current.steps)+1
			print "max stack/queue size:", max_queue_size
			print "nodes expanded:", expended
			print "maximum memory usage:", (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1000), "(bytes on OS X, kilobytes on Linux)"
			has_answer = 1
			break
		expended += 1	
		upstate = move_up(current.state, n)
		downstate = move_down(current.state, n)
		leftstate = move_left(current.state, n)
		rightstate = move_right(current.state, n)
		if upstate != None and upstate not in d:
			d[upstate] = 1
			up_node = node(upstate)
			up_node.steps = current.steps[:]
			up_node.steps.append("UP")
			distance = len(up_node.steps) + heuristic(upstate, success_state, n)
			queue.put((distance, up_node))
		if downstate != None and downstate not in d:
			d[downstate] = 1
			down_node = node(downstate)
			down_node.steps = current.steps[:]
			down_node.steps.append("DOWN")
			distance = len(down_node.steps) + heuristic(downstate, success_state, n)
			queue.put((distance, down_node))
		if leftstate != None and leftstate not in d:
			d[leftstate] = 1
			left_node = node(leftstate)
			left_node.steps = current.steps[:]
			left_node.steps.append("LEFT")
			distance = len(left_node.steps) + heuristic(leftstate, success_state, n)
			queue.put((distance, left_node))
		if rightstate != None and rightstate not in d:
			d[rightstate] = 1
			right_node = node(rightstate)
			right_node.steps = current.steps[:]
			right_node.steps.append("RIGHT")
			distance = len(right_node.steps) + heuristic(rightstate, success_state, n)
			queue.put((distance, right_node))
	if has_answer == 0:
		print "No Successful Way"

def ida_star(init_state, success_state, n, heuristic):
	print " <-- IDA* search -->"
	init_node = node(init_state)
	bound = 0 + heuristic(init_state, success_state, n)
	bound_list = [bound]
	start = datetime.datetime.now()
	while(1):
		d = {init_state:1}
		stack = [init_node]
		max_stack_size = 1
		expended = 0
		bound = min(bound_list) 
		bound_list = []

		while(len(stack) > 0):
			if len(stack) > max_stack_size:
				max_stack_size = len(stack)
			current = stack.pop()
			distance = len(current.steps) + heuristic(current.state, success_state, n)
			if distance > bound:
				bound_list.append(distance)
				continue
			
			if current.state == success_state:
				print "IDA* Finished"
				print current.steps 
				print "steps: %d" % len(current.steps)
				end = datetime.datetime.now()
				diff = end - start
				print "elapsed time:", diff.total_seconds() * 1000, "ms"
				print "depth of stack/queue:", len(current.steps)+1
				print "max stack/queue size:", max_stack_size
				print "nodes expanded:", expended
				print "maximum memory usage:", (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1000), "(bytes on OS X, kilobytes on Linux)"
				return 
			expended += 1
			upstate = move_up(current.state, n)
			downstate = move_down(current.state, n)
			leftstate = move_left(current.state, n)
			rightstate = move_right(current.state, n)

			if rightstate != None:
				if rightstate in d and d[rightstate] < len(current.steps) + 1:
					pass
				else:	
					d[rightstate] = len(current.steps) + 1
					right_node = node(rightstate)
					right_node.steps = current.steps[:]
					right_node.steps.append("RIGHT")
					stack.append(right_node)
			if leftstate != None:
				if leftstate in d and d[leftstate] < len(current.steps) + 1:
					pass
				else:
					d[leftstate] = len(current.steps) + 1
					left_node = node(leftstate)
					left_node.steps = current.steps[:]
					left_node.steps.append("LEFT")
					stack.append(left_node)
			if downstate != None:
				if downstate in d and d[downstate] < len(current.steps) + 1:
					pass
				else:
					d[downstate] = len(current.steps) + 1
					down_node = node(downstate)
					down_node.steps = current.steps[:]
					down_node.steps.append("DOWN")
					stack.append(down_node)
			if upstate != None:
				if upstate in d and d[upstate] < len(current.steps) + 1:
					pass
				else:
					d[upstate] = len(current.steps) + 1
					up_node = node(upstate)
					up_node.steps = current.steps[:]
					up_node.steps.append("UP")
					stack.append(up_node)
		
def check_initstate(init, n):
	for i in init:
		if i >= n*n or i < 0:
			return False
	return True		

def main():
	n = int(sys.argv[1])
	success = [i for i in range(n*n)] # build success state

	#init = random.sample(range(n*n), n*n)
	#init = [7,2,4,5,0,6,8,3,1]
	#init = [3,1,2,6,4,5,7,8,0]
	init = [0,8,7,6,5,4,3,2,1]
	'''
	init = [15, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14
,30, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29
,45, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44
,60, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59
,75, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 74, 89
,90, 76, 77, 78, 79, 80, 81, 82, 83, 84, 100, 85, 86, 87, 73
,105, 91, 92, 93, 94, 95, 96, 97, 98, 99, 101, 102, 117, 88, 104
,120, 106, 107, 108, 109, 110, 111, 112, 128, 113, 114, 115, 116, 103, 118
,135, 121, 122, 123, 124, 125, 126, 127, 143, 129, 130, 131, 132, 134, 119
,150, 136, 137, 138, 139, 140, 141, 142, 0, 145, 146, 161, 148, 133, 149
,195, 165, 166, 153, 154, 155, 156, 158, 159, 144, 160, 162, 147, 163, 164
,210, 151, 167, 168, 169, 170, 171, 157, 173, 174, 175, 176, 177, 178, 179
,181, 196, 183, 184, 199, 185, 186, 172, 188, 189, 190, 191, 192, 193, 194
,212, 152, 180, 198, 200, 201, 202, 187, 203, 204, 205, 206, 207, 208, 209
,197, 182, 211, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224]
	'''
	'''
	init = [1, 2, 3, 11, 12, 6, 7, 15
,8, 9, 10, 20, 4, 22, 5, 13
,16, 17, 18, 19, 21, 29, 14, 23
,24, 25, 26, 27, 28, 30, 31, 39
,32, 33, 34, 35, 36, 37, 46, 55
,40, 41, 42, 43, 44, 38, 47, 54
,48, 49, 50, 51, 52, 45, 53, 63
,56, 57, 58, 59, 60, 61, 0, 62]
	'''
	if check_initstate(init, n) == False:
		print "invalid initial state"
		return

	init_state = ",".join(map(str,init))
	success_state = ",".join(map(str,success))
	try:
		if sys.argv[2] == 'bfs':
			bfs(init_state, success_state, n)
		elif sys.argv[2] == 'dfs': 	
			dfs(init_state, success_state, n)
		elif sys.argv[2] == 'astar': 
			a_star(init_state, success_state, n, manhattan_distance)
		elif sys.argv[2] == 'idastar': 
			ida_star(init_state, success_state, n, manhattan_distance)	
		else:
			print "Usage: python hw1.py [degree of puzzle] [bfs/dfs/astar/idastar]"	
	except IndexError:
		print "Usage: python hw1.py [degree of puzzle] [bfs/dfs/astar/idastar]"		
main()		