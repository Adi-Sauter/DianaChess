import copy
import random
import math


class Agent:
    def __init__(self):
        self.move_queue = None

    def get_move(self):
        move = None
        while not self.move_queue.empty():
            move = self.move_queue.get()
        return move

    def update_move(self, move, score, depth):
        """
        :param move: Object of class Move, like a list element of gamestate.getValidMoves()
        :param score: Integer; not really necessary, just for informative printing
        :param depth: Integer; not really necessary, just for informative printing
        :return:
        """
        self.move_queue.put([move, score, depth])

    def clear_queue(self, outer_queue):
        self.move_queue = outer_queue

    def findBestMove(self, gs):
        ### player white: true, player black: false
        player = gs.whiteToMove
        print("1")
        move = minimax(gs, player, 3)
        self.update_move(move, -1, -1)


### METRICS TO ANALYZE HOW GOOD THE POSITION IS
def howManyPiecesLost(gs, pov):
    # given a gameState and player: return how many pieces the opponent has lost
    white = 0
    black = 0
    for piece in gs.board:
        if piece == 'wp':
            white = white + 1
        elif (piece == 'wB') | (piece == 'wN'):
            white = white + 3
        elif piece == 'wR':
            white = white + 5
        elif piece == 'wK':
            white = white + 1
        elif piece == 'bp':
            black = black + 1
        elif (piece == 'bB') | (piece == 'bN'):
            black = black + 3
        elif piece == 'bR':
            black = black + 5
        elif piece == 'bK':
            black = black + 1
    if pov:
        return white - black
    else:
        return black - white


def utility(gs, pov):
    return howManyPiecesLost(gs, pov)


### Implement MiniMax algorithm.
### Utility for starters: how many pieces the opponent looses.
### Depth at first: two

# given gamestate, return move
def minimax(gs, pov, depth):
    moves = gs.getValidMoves()
    max = -math.inf
    maxMove = moves[0]
    for move in moves:
        nextGameState = copy.deepcopy(gs)
        nextGameState.makeMove(move)
        nextGameStateUtility = minValue(nextGameState, pov, depth - 1)
        if nextGameStateUtility > max:
            max = nextGameStateUtility
            maxMove = move
    return maxMove


def minValue(gs, pov, depth):
    if depth == 0:
        return utility(gs, pov)

    moves = gs.getValidMoves()
    min = math.inf

    for move in moves:
        nextGameState = copy.deepcopy(gs)
        nextGameState.makeMove(move)
        nextGameStateUtility = maxValue(nextGameState, pov, depth - 1)
        if nextGameStateUtility < min:
            min = nextGameStateUtility
    return min


def maxValue(gs, pov, depth):
    if depth == 0:
        return utility(gs, pov)

    moves = gs.getValidMoves()
    max = -math.inf
    for move in moves:
        nextGameState = copy.deepcopy(gs)
        nextGameState.makeMove(move)
        nextGameStateUtility = minValue(nextGameState, pov, depth - 1)
        if nextGameStateUtility > max:
            max = nextGameStateUtility
    return max
