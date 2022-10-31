import random



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






# ### MY IMPORTS ###
# import time


# class Agent:
#     def __init__(self):
#         self.move_queue = None
#         self.whiteWeights = {"wp": 100, "wN": 300, "wB": 300, "wR": 500, "wK": 10000,
#                         "bp": -100, "bN": -300, "bB": -300, "bR": -500, "bK": -10000}
#         self.blackWeights = {"wp": -100, "wN": -300, "wB": -300, "wR": -500, "wK": -10000,
#                         "bp": 100, "bN": 300, "bB": 300, "bR": 500, "bK": 10000}
#         self.weights = None
#         self.maxDepth = 4 
        
#     def get_move(self):
#         move = None
#         while not self.move_queue.empty():
#             move = self.move_queue.get()
#         return move

#     def update_move(self, move, score, depth):
#         """
#         :param move: Object of class Move, like a list element of gamestate.getValidMoves()
#         :param score: Integer; not really necessary, just for informative printing
#         :param depth: Integer; not really necessary, just for informative printing
#         :return:
#         """
#         self.move_queue.put([move, score, depth])

#     def clear_queue(self, outer_queue):
#         self.move_queue = outer_queue

#     def findBestMove(self, gs):
#         """
#         Parameters
#         ----------
#         gs : Gamestate
#             current state of the game
#         validMoves : list
#             list of valid moves
#         returnQueue : Queue
#             multithreading queue

#         Returns
#         -------
#         none

#         """
#         # TODO
#         validMoves = gs.getValidMoves()
#         self.color = gs.whiteToMove
#         negInf = float('-inf')
#         posInf = float('inf')
#         if self.color:
#             self.weights = self.whiteWeights
#         else:
#             self.weights = self.blackWeights
#         best_v, move = self.alpha_beta_max(0, gs, negInf, posInf)
#         self.update_move(move, -1, -1)
    


#     ### BETTER: two in one ###
#     def alpha_beta_max(self, depth, gs, alpha, beta):
#         if depth == self.maxDepth:
#             #return self.simpleheuristic(gs), None
#             return self.evaluate(gs), None
#         best = float('-inf')
#         best_Move = None
#         validMoves = gs.getValidMoves()
#         if len(validMoves) == 0:
#             return self.simpleheuristic(gs), None
#         for move in gs.getValidMoves():
#             gs.makeMove(move)
#             # check for check_mate of opponent. if yes: return that move!
#             v, v_move = self.alpha_beta_min(depth + 1, gs, alpha, beta)
#             if v > best:
#                 best = v
#                 best_Move = move
#             #print(f"v of the move {move} in a_b_max:  {v}")
#             gs.undoMove()
#             #print("--- new move ---")
#             if v >= beta:
#                 break
#             alpha = max(alpha, best)
#         return best, best_Move

#     def alpha_beta_min(self, depth, gs, alpha, beta):
#         if depth == self.maxDepth:
#             #return self.simpleheuristic(gs), None
#             return self.simpleheuristic(gs), None
#         best = float('inf')
#         best_Move = None
#         validMoves = gs.getValidMoves()
#         if len(validMoves) == 0:
#             return self.evaluate(gs), None
#         for move in gs.getValidMoves():
#             gs.makeMove(move)
#             # check for check_mate of opponent. if yes: return that move!
#             v, v_move = self.alpha_beta_max(depth + 1, gs, alpha, beta)
#             if v < best:
#                 best = v
#                 best_Move = move
#             #print(f"v of the move {move} in a_b_min:  {v}")
#             gs.undoMove()
#             #print("--- new move ---")
#             if v <= alpha:
#                 break
#             beta = min(beta, best)
#         return best, best_Move
    
#     def simpleheuristic(self, gs):
#         heuristicValue = 0
#         for piece in gs.board:
#             if piece == '--':
#                 continue
#             heuristicValue += self.weights[piece]
#         return heuristicValue

#     def evaluate(self, gs):
#         ### START: counting pawns and change weights accordingly ###
#         pawn_counter = 0
#         for square in range(len(gs.board)):
#             piece = gs.board[square]
#             if piece != '--':
#                 if piece == "wp" or piece == "bp":
#                     pawn_counter += 1
#         if pawn_counter < 2:    # bei wenigen Bauern sind Bauern wertvoller & Türme und Läufer auch. 
#             stop_counting = True
#             self.weights["wp"] = 250
#             self.weights["bp"] = -250
#             self.weights["wR"] = 700
#             self.weights["bR"] = -700
#             self.weights["wB"] = 500
#             self.weights["bB"] = -500
#         else:                   # bei vielen Bauern sind Springer wertvoller
#             self.weights["wN"] = 500
#             self.weights["bN"] = -500
#         ### END: counting pawns and change weights accordingly ###

#         ### START: evaluate piece values ###
#         utility_value = 0
#         for square in range(len(gs.board)):
#             piece = gs.board[square]
#             if piece == '--':
#                 continue
#             utility_value += self.weights[piece]
#         ### END: evaluate piece values ###
#         return utility_value 

#     def findBestMoveWithTime(self, gs, validMoves, time_limit = 19.5): 
#         """
#         Parameters
#         ----------
#         gs : Gamestate
#             current state of the game
#         validMoves: list
#             list of valid moves
#         time_limit : time
#             time limit the agent has to make a move
#         """
#         limit = time.time() + time_limit
#         #action = self.minimax(gs, validMoves, limit)
#         action = self.alpha_beta_search(0, gs, validMoves, limit)
#         return action

#     ### START: alpha-beta-pruning ###
#     def alpha_beta_search(self, depth, gs, validMoves, time_limit):
#         best_v = self.a_b_max_value(gs, float('-inf'), float('inf'), time_limit)
#         for move in validMoves:
#             if best_v == self.evaluate(move):
#                 action = move
#                 break
#         return action
    
#     def a_b_max_value(self, gs, alpha, beta, time_limit):
#         # if terminal_test(gs):
#         #   return self.evaluate(self.board)
#         # terminal-test can either be check-mate or depth (see depth-limited-search) or time
#         v = float('-inf')
#         validMoves = gs.getValidMoves()
#         for move in validMoves:
#             if time.time() < time_limit:
#                 gs.makeMove(move)
#                 v = max(v, self.a_b_min_value(gs, alpha, beta, time_limit))
#                 gs.undoMove()
#                 if v >= beta:
#                     return v
#                 alpha = max(alpha, v)
#             else:
#                 v = self.evaluate(move)
#         return v

#     def a_b_min_value(self, gs, alpha, beta, time_limit):
#         # if terminal_test(gs):
#         #   return self.evaluate(self.board)
#         # terminal-test can either be check-mate or depth (see depth-limited-search) or time
#         v = float('inf')
#         validMoves = gs.getValidMoves()
#         for move in validMoves:
#             if time.time() < time_limit:
#                 gs.makeMove(move)
#                 v = min(v, self.a_b_max_value(gs, alpha, beta, time_limit))
#                 gs.undoMove()
#                 if v <= alpha:
#                     return v
#                 beta = min(beta, v)
#             else:
#                 v = self.evaluate(move)
#         return v
    
#     ### END: alpha-beta-pruning ###

#     def minimax(self, gs, validMoves, time_limit):
#         """
#         Parameters
#         ----------
#         gs : Gamestate
#             current state of the game
#         """
#         #action = max(self.min_value(gs, time_limit))
#         best_v = self.min_value(gs, time_limit)
#         #action = validMoves[0]
#         for move in validMoves:
#             if best_v == self.evaluate(move):
#                 action = move
#                 break
#         return action

        
#     def max_value(self, gs, time_limit):
#         # if terminal_test(gs):
#         #   return self.evaluate(self.board)
#         # terminal-test can either be check-mate or depth (see depth-limited-search) or time
#         v = float('-inf')
#         validMoves = gs.getValidMoves()
#         for move in validMoves:
#             if time.time() < time_limit:
#                 v = max(v, self.min_value(self.update_move(move, -1, -1).board, time_limit))
#             else: 
#                 v = self.evaluate(move)
#         return v

#     def min_value(self, gs, time_limit):
#         # if terminal_test(gs):
#         #   return self.evaluate(self.board)
#         # terminal-test can either be check-mate or depth (see depth-limited-search) or time
#         v = float('inf')
#         validMoves = gs.getValidMoves()
#         for move in validMoves:
#             if time.time() < time_limit:
#                 v = min(v, self.max_value(self.update_move(move, -1, -1).board, time_limit))
#             else:
#                 v = self.evaluate(move)
#         return v
#     '''
#     def evaluate(self, gs):
#         ### START: counting pawns and change weights accordingly ###
#         pawn_counter = 0
#         for square in range(len(gs.board)):
#             piece = gs.board[square]
#             if piece != '--':
#                 if piece == "wp" or piece == "bp":
#                     pawn_counter += 1
#                 if 
#         if pawn_counter < 2:
#             stop_counting = True
#             self.weights["wp"] = 250
#             self.weights["bp"] = -250
#             self.weights["wR"] = 700
#             self.weights["bR"] = -700
#             self.weights["wB"] = 500
#             self.weights["bB"] = -500
#         else:
#             self.weights["wN"] = 500
#             self.weights["bN"] = -500
        
#         ### END: counting pawns and change weights accordingly ###

#         ### START: evaluate piece values ###
#         utility_value = 0
#         for square in range(len(gs.board)):
#             piece = gs.board[square]
#             if piece == '--':
#                 continue
#             utility_value += self.weights[piece]
#         ### END: evaluate piece values ###
#         return utility_value 
#         '''

