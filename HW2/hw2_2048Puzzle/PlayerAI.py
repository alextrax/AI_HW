#!/usr/bin/env python
#coding:utf-8

from random import randint
from BaseAI import BaseAI
import math
import time
import json
import sys

#vecIndex = [UP, DOWN, LEFT, RIGHT] 
DEFAULT_DEPTH = 4
MAX_VALUE = 2**16 
MIN_VALUE = -(2**16)
TIME_LIMIT = 0.2
DEBUG = True

empty_weight = 20.0
smooth_weight = -1.0
smooth_val_weight = 0 #1.0
mono_weight = 40.0
edge_weight = 150.0
snake_weight = 1.0
snake = [[10,8,7,6.5],
        [.5,.7,1,3],
        [-.5,-1.5,-1.8,-2],
        [-3.8,-3.7,-3.5,-3]]
hmap = {}
#smap = {}

class PlayerAI(BaseAI):
    def __init__(self):
        if sys.argv[2] == "H":

            try:
                with open('data.json', 'r') as fp:
                    self.smap = json.load(fp) 
            except:
                self.smap = {}
                print "failed to load data.json"   
        else:
            self.smap = {}

    def __del__(self):    
        try:
            with open('data.json', 'w') as fp:
                json.dump(self.smap , fp, sort_keys=True, indent=4)
        except:
            print "failed to save data.json"             

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
                    if i == 0 : #or i == (grid.size-1):
                        score += 1
                    if j == 0 : #or j == (grid.size-1):
                        score += 1
                    return score    
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

    def SnakeScore(self, grid):
        score = 0
        for i in xrange(grid.size):
            for j in xrange(grid.size):
                score += grid.map[i][j] * snake[i][j]

    def MixHeuristic(self, grid):
        encode = str([x for row in grid.map for x in row])
        if encode in hmap:
            return hmap[encode]

        avail = grid.getAvailableCells()
        empty_count =  math.log(len(avail)) * empty_weight if len(avail) > 1 else 0.5 * empty_weight
        max_tile = grid.getMaxTile() * max_weight
        smooth_diff, smooth_val = self.Smoothness(grid) 
        smooth_diff = math.log(smooth_diff) * smooth_weight if smooth_diff > 1 else 1
        mono = self.Monotonic(grid) 
        edge = self.OnEdge(grid, grid.getMaxTile()) * edge_weight
        #print empty_count, max_tile, smooth, mono, edge
        score = empty_count + smooth_diff + smooth_val + mono + edge
        hmap[encode] = score
        return score
        #return mono + empty_count + max_tile
        #return len(grid.getAvailableCells()) + \
        #       math.log(grid.getMaxTile(), 2) + \
        #       self.SameValue(grid) 

    def RowColHeuristic(self, row):
        # smoothness
        score_val = 0
        score_diff = 0
        for i in xrange(len(row)-1):             
            if row[i] == row[i+1]:
                score_val +=  math.log(row[i], 2) if row[i] > 0 else 0
            
            if row[i] > 0 and row[i+1] > 0:
                score_diff += abs(math.log(row[i], 2) - math.log(row[i+1], 2)) if row[i] != row[i+1] else 0


        # monotonic
        mono_l = 0
        mono_r = 0

        # non_increasing
        if all(x>=y for x, y in zip(row[:len(row)-1], row[1:])):
            mono_l += 1

        # non_decreasing 
        elif all(x<=y for x, y in zip(row[:len(row)-1], row[1:])):
            mono_r += 1 
        return max(mono_l, mono_r) * mono_weight, score_diff, score_val                 

    def SepHeuristic(self, grid):
        SepScore = 0
        for row in grid.map:
            rstring = str(row)
            if rstring in self.smap:
                #print "row hit", rstring
                SepScore += self.smap[rstring]
            else:    
                mono, smooth_diff, smooth_val = self.RowColHeuristic(row)
                smooth_diff = smooth_diff * smooth_weight 
                #smooth_diff = math.log(smooth_diff) * smooth_weight if smooth_diff > 1 else 1
                smooth_val *= smooth_val_weight
                self.smap[rstring] = mono + smooth_diff + smooth_val
                SepScore += mono + smooth_diff + smooth_val


        for i in xrange(grid.size):
            col = [row[i] for row in grid.map]
            cstring = str(col)
            if cstring in self.smap:
                #print "col hit", cstring
                SepScore += self.smap[cstring]
            else:    
                mono, smooth_diff, smooth_val = self.RowColHeuristic(col)
                smooth_diff = smooth_diff * smooth_weight 
                #smooth_diff = math.log(smooth_diff) * smooth_weight if smooth_diff > 1 else 1
                smooth_val *= smooth_val_weight
                self.smap[cstring] = mono + smooth_diff + smooth_val
                SepScore += mono + smooth_diff + smooth_val

        

        avail = grid.getAvailableCells()
        empty_count = len(avail) * empty_weight
        #empty_count =  math.log(len(avail)) * empty_weight if len(avail) > 1 else 0.5 * empty_weight
        max_tile = grid.getMaxTile()
        edge = self.OnEdge(grid, grid.getMaxTile()) * edge_weight
        #print empty_count, max_tile, smooth, mono, edge
        #snakescore = self.SnakeScore(grid)
        score = empty_count + SepScore + edge + max_tile #+ snakescore
        return score

    def debug_heuristic(self, grid):
        avail = grid.getAvailableCells()
        empty_count =  math.log(len(avail)) * empty_weight if len(avail) > 1 else 0.5 * empty_weight
        max_tile = grid.getMaxTile() * max_weight
        smooth_diff, smooth_val = self.Smoothness(grid) 
        smooth_diff = math.log(smooth_diff) if smooth_diff > 1 else 0 
        smooth_diff *= smooth_weight
        mono = self.Monotonic(grid) * mono_weight
        edge = self.OnEdge(grid, grid.getMaxTile()) * edge_weight
        print "empty:", empty_count, "max:", max_tile, "smooth_diff:", smooth_diff, "smooth_val:", smooth_val, "mono:", mono, "edge", edge
        print "score", empty_count + smooth_diff + smooth_val + mono + edge
        

    def debug_SepHeuristic(self, grid):
        SepScore = 0
        mono_debug = 0
        smooth_diff_debug = 0
        smooth_val_debug = 0
        for row in grid.map:
            mono, smooth_diff, smooth_val = self.RowColHeuristic(row)
            #smooth_diff = math.log(smooth_diff) if smooth_diff > 1 else 0 
            smooth_diff *= smooth_weight
            smooth_val *= smooth_val_weight
            SepScore += mono + smooth_diff + smooth_val
            mono_debug += mono
            smooth_diff_debug += smooth_diff
            smooth_val_debug += smooth_val
        #print "smooth_diff:", smooth_diff_debug, "smooth_val:", smooth_val_debug, "mono:", mono_debug
        for i in xrange(grid.size):
            col = [row[i] for row in grid.map]
            mono, smooth_diff, smooth_val = self.RowColHeuristic(col)
            #smooth_diff = math.log(smooth_diff) if smooth_diff > 1 else 0 
            smooth_diff *= smooth_weight
            smooth_val *= smooth_val_weight
            SepScore += mono + smooth_diff + smooth_val
            mono_debug += mono
            smooth_diff_debug += smooth_diff
            smooth_val_debug += smooth_val
        #print "smooth_diff:", smooth_diff_debug, "smooth_val:", smooth_val_debug, "mono:", mono_debug

        

        avail = grid.getAvailableCells()
        empty_count = len(avail) * empty_weight
        #empty_count =  math.log(len(avail)) * empty_weight if len(avail) > 1 else 0.5 * empty_weight
        #max_tile = grid.getMaxTile() * max_weight
        edge = self.OnEdge(grid, grid.getMaxTile()) * edge_weight
        #print empty_count, max_tile, smooth, mono, edge
        #snakescore = self.SnakeScore(grid)
        score = empty_count + SepScore + edge + snakescore
        print "empty:", empty_count, "smooth_diff:", smooth_diff_debug, "smooth_val:", smooth_val_debug, "mono:", mono_debug, "edge", edge#, "snake", snakescore
        print "score from SepHeuristic", score

    def getMove(self, grid):
        #moves = grid.getAvailableMoves()
        #return moves[randint(0,len(moves)-1)]
        if DEBUG:
            self.debug_SepHeuristic(grid)
            print grid.getAvailableMoves()
        if len(grid.getAvailableMoves()) == 0:
            #with open('data.json', 'w') as fp:
            #    json.dump(self.smap, fp, sort_keys=True, indent=4)
            return 0

        self.start = time.time()
        depth = 0
        result = 0
        while (time.time() - self.start) < TIME_LIMIT:
            depth += 1
            d, v = self.search(grid, depth, -1, MAX_VALUE, True, self.SepHeuristic)
            if d == -1 and v == -1:
                break
            else:
                result = d    
         
        if DEBUG:
            print depth  
            print "search time:",time.time() - self.start 
            debugGrid = grid.clone()
            debugGrid.move(result)
            #self.debug_heuristic(debugGrid)
            self.debug_SepHeuristic(debugGrid)
            if result not in grid.getAvailableMoves():
                print "direction", result, "not available"
                #with open('data.json', 'w') as fp:
                #    json.dump(self.smap, fp, sort_keys=True, indent=4)
                #return 0
        return result

    def search(self, grid, depth, alpha, beta, isMAX, heuristic):
        if (time.time() - self.start) > TIME_LIMIT:
            return -1, -1
        moves = grid.getAvailableMoves()
        if len(moves) == 0 or depth == 0:
            return 0, heuristic(grid)
	
        if isMAX:
            v = MIN_VALUE
            direction = moves[0]
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
            self.debug_SepHeuristic(grid)

        self.start = time.time()
        depth = 0
        result = 0
        while (time.time() - self.start) < TIME_LIMIT:
            depth += 1
            d, v = self.search(grid, depth, True, self.SepHeuristic)
            if d == -1 and v == -1:
                break
            else:
                result = d    
         
        if DEBUG:
            print depth  
            print "timd:",time.time() - self.start 
            debugGrid = grid.clone()
            debugGrid.move(result)
            self.debug_SepHeuristic(debugGrid)
            if result not in grid.getAvailableMoves():
                print "direction", result, "not available"
                return 0

        return result
    def search(self, grid, depth, isMAX, heuristic):
        if (time.time() - self.start) > TIME_LIMIT:
            return -1, -1
        moves = grid.getAvailableMoves()
        if len(moves) == 0 or depth == 0:
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
