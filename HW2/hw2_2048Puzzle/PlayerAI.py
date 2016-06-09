#!/usr/bin/env python
#coding:utf-8

from random import randint
from BaseAI import BaseAI
import math
import time

#vecIndex = [UP, DOWN, LEFT, RIGHT] 
DEFAULT_DEPTH = 8
MAX_VALUE = 2**32 - 1
TIME_LIMIT = 0.4

class PlayerAI(BaseAI):
    def MaxTile(self, grid):
        return grid.getMaxTile()

    def EmptyTile(self, grid):
        return len(grid.getAvailableCells())   

    def SameValue(self, grid):
        count = 0
        for i in xrange(grid.size - 1):
            for j in xrange(grid.size - 1):
                if grid.map[i][j] == grid.map[i][j+1]:
                    count += 1
                if grid.map[i][j] == grid.map[i+1][j]:
                    count += 1
        return count

    def MixHeuristic(self, grid):
        empty_weight = 1.0
        max_weight = 1.0
        same_weight = 1.0
        empty_count =  len(grid.getAvailableCells())
        max_tile = grid.getMaxTile()
        same_count = self.SameValue(grid)
        return empty_count + max_tile + same_count
        #return len(grid.getAvailableCells()) + \
        #       math.log(grid.getMaxTile(), 2) + \
        #       self.SameValue(grid) 

    def getMove(self, grid):
        #moves = grid.getAvailableMoves()
        #return moves[randint(0,len(moves)-1)]
        start = time.time()
        depth = 0
        while (time.time() - start) < TIME_LIMIT:
            depth += 1
            d, v = self.search(grid, depth, -1, MAX_VALUE, True, self.MixHeuristic)
        print depth  
        print time.time() - start  
        return d

    def search(self, grid, depth, alpha, beta, isMAX, heuristic):
        moves = grid.getAvailableMoves()
        if depth == 0 or moves == None:
            return 4, heuristic(grid)	
        if isMAX:
            v = -1
            direction = 4
            for m in moves:
                gridCopy = grid.clone()
                if gridCopy.move(m):
                    v = max(v, self.search(gridCopy, depth - 1, alpha, beta, False, heuristic)[1])
                    if alpha < v:
                        direction = m
                        alpha = v
                    if beta <= alpha:
                        break # β cut-off 
            return direction, v
        else:
            v = MAX_VALUE
            direction = 4
            for m in moves:
                gridCopy = grid.clone()
                if gridCopy.move(m):
                    v = min(v, self.search(gridCopy, depth - 1, alpha, beta, True, heuristic)[1])
                    if v < beta:
                        direction = m
                        beta = v
                    if beta <= alpha:
                        break # α cut-off 
            return direction, v


