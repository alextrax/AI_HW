Name: Chih-Sheng Wang
UNI: cw2952
e-mail: cw2952@columbia.edu


#How to run program:
MiniMax: 
	python GameManager.py minimax
Alpha-Beta pruning: 
	python GameManager.py ab

#Performance:
	Alpha-Beta: (50 runs)
		4096: 1/50  (2%)
		2048: 24/50 (48%)
		1024: 21/50 (42%)
		512:  4/50	(8%)
	Pure Minimax: (20 runs)
		2048: 7/20 (35%)
		1024: 9/20 (45%)
		512:  4/20 (20%)	

#Optimizations:
	1) Hash table to record row/column based heuristic value and avoid recalculation
	2) Iterative Deepen Search to fully utilitize the one second searching time		

#Heuristic:
	1) Empty tiles number
	2) Max tile value
	3) Monotonic
	4) Keep max tile at the corner
	5) Smoothness: difference between adjecent tiles
