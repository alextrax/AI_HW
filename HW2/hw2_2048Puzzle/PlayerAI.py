#!/usr/bin/env python
#coding:utf-8

from random import randint
from BaseAI import BaseAI
import math
import time

#vecIndex = [UP, DOWN, LEFT, RIGHT] 
DEFAULT_DEPTH = 4
MAX_VALUE = 2**16 
MIN_VALUE = -(2**16)
TIME_LIMIT = 0.9
DEBUG = True

empty_weight = 12.0
max_weight = 1.0
smooth_weight = -1.0
mono_weight = 3.0
edge_weight = 6.0

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

    def OnEdge(self, grid, value):
        score = 0
        for i in xrange(grid.size):
            for j in xrange(grid.size):
                if grid.map[i][j] == value:
                    if i == 0 or i == (grid.size-1):
                        score += 1
                    if j == 0 or j == (grid.size-1):
                        score += 1
        return score                

    def EmptyTile(self, grid):
        return len(grid.getAvailableCells())   

    def Smoothness(self, grid):
        score_diff = 0
        score_val = 0
        for i in xrange(grid.size-1):
            for j in xrange(grid.size):                
                if grid.map[i][j] == grid.map[i+1][j]:
                    score_val +=  math.log(grid.map[i][j], 2) if grid.map[i][j] > 0 else 0
                
                if grid.map[i][j] > 0 and grid.map[i+1][j] > 0:
                    score_diff += abs(math.log(grid.map[i][j], 2) - math.log(grid.map[i+1][j], 2)) if grid.map[i][j] != grid.map[i+1][j] else 0
        
        for i in xrange(grid.size):
            for j in xrange(grid.size-1):
                if grid.map[i][j] == grid.map[i][j+1]:
                    score_val +=  math.log(grid.map[i][j], 2) if grid.map[i][j] > 0 else 0

                if grid.map[i][j] > 0 and grid.map[i][j+1] > 0:
                    score_diff += abs(math.log(grid.map[i][j], 2) - math.log(grid.map[i][j+1], 2)) if grid.map[i][j] != grid.map[i][j+1] else 0
                
        return score_diff, score_val

    def Monotonic(self, grid):
        mono_up = 0
        mono_dn = 0
        mono_l = 0
        mono_r = 0

        for i in xrange(grid.size):
            # non_increasing: LR
            if all(x>=y for x, y in zip(grid.map[i][:grid.size-1], grid.map[i][1:])):
                mono_l += 1

            # non_decreasing: LR    
            elif all(x<=y for x, y in zip(grid.map[i][:grid.size-1], grid.map[i][1:])):
                mono_r += 1 

        for i in xrange(grid.size):
            col = [row[i] for row in grid.map]
            # non_increasing: UD
            if all(x>=y for x, y in zip(col[:grid.size-1], col[1:])):
                mono_up += 1    
 
            # non_increasing: UD
            elif all(x<=y for x, y in zip(col[:grid.size-1], col[1:])):
                mono_dn += 1 
        return max(mono_l, mono_r) + max(mono_up, mono_dn)


    def MixHeuristic(self, grid):
        avail = grid.getAvailableCells()
        empty_count =  math.log(len(avail)) * empty_weight if len(avail) > 1 else 1 * empty_weight
        max_tile = grid.getMaxTile() * max_weight
        smooth_diff, smooth_val = self.Smoothness(grid) 
        smooth_diff = math.log(smooth_diff) * smooth_weight if smooth_diff > 1 else 1
        mono = self.Monotonic(grid) * mono_weight
        edge = self.OnEdge(grid, grid.getMaxTile()) * edge_weight
        #print empty_count, max_tile, smooth, mono, edge
        return empty_count + smooth_diff + smooth_val + mono + edge
        #return mono + empty_count + max_tile
        #return len(grid.getAvailableCells()) + \
        #       math.log(grid.getMaxTile(), 2) + \
        #       self.SameValue(grid) 

    def debug_heuristic(self, grid):
        avail = grid.getAvailableCells()
        empty_count =  math.log(len(avail)) * empty_weight if len(avail) > 1 else 1 * empty_weight
        max_tile = grid.getMaxTile() * max_weight
        smooth_diff, smooth_val = self.Smoothness(grid) 
        smooth_diff = math.log(smooth_diff) * smooth_weight if smooth_diff > 1 else 1 
        mono = self.Monotonic(grid) * mono_weight
        edge = self.OnEdge(grid, grid.getMaxTile()) * edge_weight
        print "empty:", empty_count, "max:", max_tile, "smooth_diff:", smooth_diff, "smooth_val:", smooth_val, "mono:", mono, "edge", edge
        print "score", empty_count + smooth_diff + smooth_val + mono + edge

    def getMove(self, grid):
        #moves = grid.getAvailableMoves()
        #return moves[randint(0,len(moves)-1)]
        if DEBUG:
            self.debug_heuristic(grid)
            print grid.getAvailableMoves()

        self.start = time.time()
        depth = DEFAULT_DEPTH
        result = 0
        while (time.time() - self.start) < TIME_LIMIT:
            depth += 1
            d, v = self.search(grid, depth, -1, MAX_VALUE, True, self.MixHeuristic)
            if d == -1 and v == -1:
                break
            else:
                result = d    
         
        if DEBUG:
            print depth  
            print "search time:",time.time() - self.start 
            debugGrid = grid.clone()
            debugGrid.move(result)
            self.debug_heuristic(debugGrid)
            if result not in grid.getAvailableMoves():
                print "direction", result, "not available"
                return 0
        return result

    def search(self, grid, depth, alpha, beta, isMAX, heuristic):
        if (time.time() - self.start) > TIME_LIMIT:
            return -1, -1
        moves = grid.getAvailableMoves()
        if moves == None:
            print "no available moves"
            return 0, heuristic(grid)
        if depth == 0:
            return 0, heuristic(grid)	
        if isMAX:
            v = MIN_VALUE
            direction = 0
            for m in moves:
                gridCopy = grid.clone()
                if gridCopy.move(m):
                    v = max(v, self.search(gridCopy, depth - 1, alpha, beta, False, heuristic)[1])
                    if alpha < v:
                        direction = m
                        alpha = v
                    if beta <= alpha:
                        #print "β cut-off ", beta , "<=", alpha
                        return direction, v
                        #break # β cut-off 
            if (time.time() - self.start) > TIME_LIMIT:
                return -1, -1            
            else:
                return direction, v
        else:
            v = MAX_VALUE
            direction = 0
            cells = grid.getAvailableCells()
            for c in cells:
                gridCopy = grid.clone()
                if gridCopy.canInsert(c):
                    gridCopy.setCellValue(c, self.getNewTileValue())
                    v = min(v, self.search(gridCopy, depth - 1, alpha, beta, True, heuristic)[1])
                    if v < beta:
                        beta = v
                    if beta <= alpha:
                        #print "α cut-off ", beta , "<=", alpha
                        return direction, v
                        #break # α cut-off 
            if (time.time() - self.start) > TIME_LIMIT:
                return -1, -1            
            else:            
                return direction, v

class PlayerAIMiniMax(PlayerAI):
    def getMove(self, grid):
        #moves = grid.getAvailableMoves()
        #return moves[randint(0,len(moves)-1)]
        if DEBUG:
            self.debug_heuristic(grid)

        self.start = time.time()
        depth = 0
        result = 0
        while (time.time() - self.start) < TIME_LIMIT:
            depth += 1
            d, v = self.search(grid, depth, True, self.MixHeuristic)
            if d == -1 and v == -1:
                break
            else:
                result = d    
         
        if DEBUG:
            print depth  
            print "timd:",time.time() - self.start 
            debugGrid = grid.clone()
            debugGrid.move(result)
            self.debug_heuristic(debugGrid)
            if result not in grid.getAvailableMoves():
                print "direction", result, "not available"
                return 0

        return result
    def search(self, grid, depth, isMAX, heuristic):
        if (time.time() - self.start) > TIME_LIMIT:
            return -1, -1
        moves = grid.getAvailableMoves()
        if moves == None:
            print "no available moves"
            return 0, heuristic(grid)
        if depth == 0:
            return 0, heuristic(grid)   
        if isMAX:
            v = MIN_VALUE
            direction = 0
            for m in moves:
                gridCopy = grid.clone()
                if gridCopy.move(m):
                    val = self.search(gridCopy, depth - 1, False, heuristic)[1]
                    if val > v:
                        direction = m
                        v = val
                    
            if (time.time() - self.start) > TIME_LIMIT:
                return -1, -1            
            else:
                return direction, v
        else:
            v = MAX_VALUE
            direction = 0
            cells = grid.getAvailableCells()
            for c in cells:
                gridCopy = grid.clone()
                if gridCopy.canInsert(c):
                    gridCopy.setCellValue(c, self.getNewTileValue())
                    val = self.search(gridCopy, depth - 1, True, heuristic)[1]
                    if val < v:
                        v = val
                    
            if (time.time() - self.start) > TIME_LIMIT:
                return -1, -1            
            else:            
                return direction, v
