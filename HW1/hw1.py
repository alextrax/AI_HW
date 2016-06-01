import sys
import random
import datetime

class node:
	def __init__(self, state):
		self.state = state
		self.up = None
		self.down = None
		self.left = None
		self.right = None
		self.steps = []

def move_up(state, n):
	state_list = list(state)
	index = state_list.index("0")
	if index < n: # blank at the top row
		return None
	else:
		state_list[index], state_list[index-n] = state_list[index-n], state_list[index]
		return "".join(state_list)

def move_down(state, n):
	state_list = list(state)
	index = state_list.index("0")
	if (n-1) * n <= index: # blank at the bottom row
		return None
	else:
		state_list[index], state_list[index+n] = state_list[index+n], state_list[index]
		return "".join(state_list)

def move_left(state, n):
	state_list = list(state)
	index = state_list.index("0")
	if index % n == 0: # blank at the left-most column
		return None
	else:
		state_list[index], state_list[index-1] = state_list[index-1], state_list[index]
		return "".join(state_list)

def move_right(state, n):
	state_list = list(state)
	index = state_list.index("0")
	if (index+1) % n == 0: # blank at the right-most column
		return None
	else:
		state_list[index], state_list[index+1] = state_list[index+1], state_list[index]
		return "".join(state_list)

def bfs(init_state, success_state, n):
	print " <-- BFS search -->"
	init_node = node(init_state)
	d = {init_state:1}
	queue = [init_node]
	max_queue_depth = 1
	expended = 0
	has_answer = 0
	start = datetime.datetime.now()
	while(len(queue) > 0):
		if len(queue) > max_queue_depth:
			max_queue_depth = len(queue)
		current = queue.pop(0)
		if current.state == success_state:
			print "BFS Finished"
			print current.steps 
			print "steps: %d" % len(current.steps)
			end = datetime.datetime.now()
			diff = end - start
			print "elapsed time:", diff.total_seconds() * 1000, "ms"
			print "depth of stack/queue:", len(queue)
			print "max depth of stack/queue:", max_queue_depth
			print "nodes expended:", expended
			has_answer = 1
			break
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
			expended += 1
		if downstate != None and downstate not in d:
			d[downstate] = 1
			down_node = node(downstate)
			down_node.steps = current.steps[:]
			down_node.steps.append("DOWN")
			queue.append(down_node)
			expended += 1
		if leftstate != None and leftstate not in d:
			d[leftstate] = 1
			left_node = node(leftstate)
			left_node.steps = current.steps[:]
			left_node.steps.append("LEFT")
			queue.append(left_node)
			expended += 1
		if rightstate != None and rightstate not in d:
			d[rightstate] = 1
			right_node = node(rightstate)
			right_node.steps = current.steps[:]
			right_node.steps.append("RIGHT")
			queue.append(right_node)
			expended += 1		
	if has_answer == 0:
		print "No Successful Way"


def dfs(init_state, success_state, n):
	print " <-- DFS search -->"
	init_node = node(init_state)
	d = {init_state:1}
	stack = [init_node]
	max_stack_depth = 1
	expended = 0
	has_answer = 0
	start = datetime.datetime.now()
	while(len(stack) > 0):
		if len(stack) > max_stack_depth:
			max_stack_depth = len(stack)
		current = stack.pop()
		if current.state == success_state:
			print "DFS Finished"
			print current.steps 
			print "steps: %d" % len(current.steps)
			end = datetime.datetime.now()
			diff = end - start
			print "elapsed time:", diff.total_seconds() * 1000, "ms"
			print "depth of stack/queue:", len(stack)
			print "max depth of stack/queue:", max_stack_depth
			print "nodes expended:", expended
			has_answer = 1
			break
		upstate = move_up(current.state, n)
		downstate = move_down(current.state, n)
		leftstate = move_left(current.state, n)
		rightstate = move_right(current.state, n)
		if upstate != None and upstate not in d:
			d[upstate] = 1
			up_node = node(upstate)
			up_node.steps = current.steps[:]
			up_node.steps.append("UP")
			stack.append(up_node)
			expended += 1
		if downstate != None and downstate not in d:
			d[downstate] = 1
			down_node = node(downstate)
			down_node.steps = current.steps[:]
			down_node.steps.append("DOWN")
			stack.append(down_node)
			expended += 1
		if leftstate != None and leftstate not in d:
			d[leftstate] = 1
			left_node = node(leftstate)
			left_node.steps = current.steps[:]
			left_node.steps.append("LEFT")
			stack.append(left_node)
			expended += 1
		if rightstate != None and rightstate not in d:
			d[rightstate] = 1
			right_node = node(rightstate)
			right_node.steps = current.steps[:]
			right_node.steps.append("RIGHT")
			stack.append(right_node)
			expended += 1		
	if has_answer == 0:
		print "No Successful Way"

def main():
	n = int(sys.argv[1])
	success = [i for i in range(n*n)] # build success state

	init = random.sample(range(n*n), n*n)
	#init = [1,0,2,3,4,5,6,7,8]
	init = [3,1,2,6,4,5,7,8,0]
	init_state = "".join(map(str,init))
	success_state = "".join(map(str,success))
	print "init state: " + init_state
	bfs(init_state, success_state, n)
	dfs(init_state, success_state, n)

main()		