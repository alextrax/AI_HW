#!/usr/bin/env python
#coding:utf-8

from random import randint
from BaseAI import BaseAI
import math
import time

#vecIndex = [UP, DOWN, LEFT, RIGHT] 
DEFAULT_DEPTH = 8
MAX_VALUE = 2**32 - 1
TIME_LIMIT = 0.2

class PlayerAI(BaseAI):
    def getNewTileValue(self):
        possibility = 0.9
        possibleNewTileValue = [2, 4]
        if randint(0,99) < 100 * possibility: 
            return possibleNewTileValue[0] 
        else: 
            return possibleNewTileValue[1];

    def MaxTile(self, grid):
        return grid.getMaxTile()

    def EmptyTile(self, grid):
        return len(grid.getAvailableCells())   

    def SameValue(self, grid):
        count = 0
        for i in xrange(grid.size - 1):
            for j in xrange(grid.size - 1):
                if grid.map[i][j] == grid.map[i][j+1]:
                    count +=  math.log(grid.map[i][j], 2) if grid.map[i][j] > 0 else 1
                if grid.map[i][j] == grid.map[i+1][j]:
                    count +=  math.log(grid.map[i][j], 2) if grid.map[i][j] > 0 else 1
        return count

    def Monotonic(self, grid):
        mono_row = 0
        mono_col = 0
        for i in xrange(grid.size-1):
            # non_increasing: LR
            if all(x>=y for x, y in zip(grid.map[i], grid.map[i][1:])):
                mono_row += 1

            # non_decreasing: LR    
            elif all(x<=y for x, y in zip(grid.map[i], grid.map[i][1:])):
                mono_row -= 1 

            # non_increasing: UD
            if all(x>=y for x, y in zip(grid.map[:][i], grid.map[1:][i])):
                mono_col += 1    
 
            # non_increasing: UD
            elif all(x<=y for x, y in zip(grid.map[:][i], grid.map[1:][i])):
                mono_col -= 1 
        return abs(mono_row) + abs(mono_col)


    def MixHeuristic(self, grid):
        empty_weight = 3.0
        max_weight = 1.0
        same_weight = 1.0
        mono_weight = 1.0
        empty_count =  len(grid.getAvailableCells()) * empty_weight
        max_tile = grid.getMaxTile() * max_weight
        same_count = self.SameValue(grid) * same_weight
        mono = self.Monotonic(grid) * mono_weight
        #print empty_count, max_tile, same_count, mono
        return empty_count + max_tile + same_count + mono
        #return mono + empty_count + max_tile
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
            return -1, heuristic(grid)	
        if isMAX:
            v = -1
            direction = -1
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
            direction = -1
            cells = grid.getAvailableCells()
            for c in cells:
                gridCopy = grid.clone()
                if gridCopy.canInsert(c):
                    gridCopy.setCellValue(c, self.getNewTileValue())
                    v = min(v, self.search(gridCopy, depth - 1, alpha, beta, True, heuristic)[1])
                    if v < beta:
                        beta = v
                    if beta <= alpha:
                        break # α cut-off 
            return direction, v


