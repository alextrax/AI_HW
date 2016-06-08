#!/usr/bin/env python
#coding:utf-8

from random import randint
from BaseAI import BaseAI

#vecIndex = [UP, DOWN, LEFT, RIGHT] 
DEFAULT_DEPTH = 8
MAX_VALUE = 2**32 - 1
class PlayerAI(BaseAI):
    def MaxTile(self, grid):
        return grid.getMaxTile()

    def EmptyTile(self, grid):
        return len(grid.getAvailableCells())   

    def getMove(self, grid):
        d, v = self.search(grid, DEFAULT_DEPTH, -1, MAX_VALUE, True, self.EmptyTile)
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


