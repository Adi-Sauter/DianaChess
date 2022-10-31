"""
@author: Adem Atmaca, Adrian Sauter

This is Agent Jesse, which is fed with enough functions/ techniques to play diana-chess as good as possible.
"""

import random


class Agent:
    def __init__(self):
        self.move_queue = None
        self.color = None
        self.maxDepth = 4
        self.weights = None
        self.whiteWeights = {"wp": 110, "wN": 330, "wB": 330, "wR": 550, "wK": 11000,
                        "bp": -100, "bN": -300, "bB": -300, "bR": -500, "bK": -10000}
        self.blackWeights = {"wp": -100, "wN": -300, "wB": -300, "wR": -500, "wK": -10000,
                        "bp": 110, "bN": 330, "bB": 330, "bR": 550, "bK": 11000}
        self.checkmateDepth = 0
        self.enemyCheckmate = False
        self.checkmateMove = None
        self.enemyInCheck = False
        self.best_move = None
        self.endGame = False
        self.onlyKingLeft = False
        self.forceThreefoldMove = None
         ### Pawns ###
        self.wp_table = [0, 0, 0, 0, 0, 0,
                         50, 50, 50, 50, 50, 50,
                         10, 25, 30, 30, 25, 10,
                         10, 15, 20, 20, 15, 5,
                         5, 10, -25, -25, 10, 5,
                         0, 0, 0, 0, 0, 0]
        self.bp_table = [0, 0, 0, 0, 0, 0, 
                         5, 10, -25, -25, 10, 5,
                         10, 15, 20, 20, 15, 5,
                         10, 25, 30, 30, 25, 10,
                         50, 50, 50, 50, 50, 50,
                         0, 0, 0, 0, 0, 0]
        ### Knights ###
        self.wN_table = [-50, -30, -30, -30, -40, -50,
                         -40, 10, 15, 15, 10, -40,
                         -30, 10, 20, 20, 10, -30,
                         -30, 10, 20, 20, 10, -30,
                         -40, 10, 15, 15, 10, -40,
                         -50, -40, -30, -30, -40, -50]
        self.bN_table = self.wN_table
        ### Bishops ###
        self.wB_table = [-5, -10, -10, -10, -10, -5,
                         -10, 0, 0, 0, 0, -10,
                         -10, 5, 10, 10, 5, -10,
                         -10, 10, 10, 10, 10, -10,
                         -10, 5, 0, 0, 5, -10,
                         -20, -40, -10, -10, -40, -20]
        self.bB_table = [-20, -40, -10, -10, -40, -20,
                         -10, 5, 0, 0, 5, -10,
                         -10, 10, 10, 10, 10, -10,
                         -10, 5, 10, 10, 5, -10,
                         -10, 0, 0, 0, 0, -10,
                         -5, -10, -10, -10, -10, -5]
        ### Rooks ###
        # not really useful for this version
        # self.wR_table = [0, 0, 0, 0, 0, 0,
        #                  5, 10, 10, 10, 10, 5,
        #                  -5, 5, 5, 5, 5, -5,
        #                  -5, 0, 0, 0, 0, -5,
        #                  -5, 0, 0, 0, 0, -5,
        #                  -5, 0, 10, 10, 0, -5]
        # self.bR_table = [-5, 0, 10, 10, 0, -5,
        #                  -5, 0, 0, 0, 0, -5,
        #                  -5, 0, 0, 0, 0, -5,
        #                  -5, 5, 5, 5, 5, -5,
        #                   5, 10, 10, 10, 10, 5,
        #                   0, 0, 0, 0, 0, 0,]
        ### Kings ###
        self.wK_table = [-30, -40, -50, -50, -40, -30,
                         -30, -40, -50, -50, -40, -30,
                         -30, -40, -50, -50, -40, -30,
                         -10, -20, -20, -20, -20, -10,
                          5, 5, 0, 0, 5, 5,
                          20, 30, 10, 0, 10, 30]
        self.bK_table = [20, 30, 10, 0, 10, 30,
                         5, 5, 0, 0, 5, 5,
                         -10, -20, -20, -20, -20, -10,
                         -30, -40, -50, -50, -40, -30,
                         -30, -40, -50, -50, -40, -30,
                         -30, -40, -50, -50, -40, -30]

        self.wK_table_endgame = [-50, -40, -30, -30, -40, -50,
                                 -30, -20, 10, 10, -20, -30,
                                 -30, 10, 30, 30, 10, -30,
                                 -30, 10, 30, 30, 10, -30,
                                 -30, -20, 10, 10, -20, -30,
                                 -50, -40, -30, -30, -40, -50]
        self.bK_table_endgame = self.wK_table_endgame

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
        """
        Parameters
        ----------
        gs : Gamestate
            current state of the game
        validMoves : list
            list of valid moves
        returnQueue : Queue
            multithreading queue

        Returns
        -------
        none

        """
        self.color = gs.whiteToMove
        negInf = float('-inf')
        posInf = float('inf')
        if self.color:
            self.weights = self.whiteWeights
        else:
            self.weights = self.blackWeights
        self.update_weights(gs)
        if self.color:
            king_square = gs.board.index("wK")
        else:
            king_square = gs.board.index("bK")
        self.king_safety(king_square)
        
        best_v, move = self.alpha_beta_max(0, gs, negInf, posInf)
        if self.onlyKingLeft and self.forceThreefoldMove:
            self.update_move(self.forceThreefoldMove, -1, -1) # try to force threefold in case our agent only has his king left
        elif self.enemyCheckmate:
            self.update_move(self.checkmateMove, -1, -1) # in case our opponent can be set to checkmate in one move, our agent does that move
        elif move:
            self.update_move(move, -1, -1) # if none of the two cases above are present, do the move that was found by the pruning algorithm

    
    def alpha_beta_max(self, depth, gs, alpha, beta):
        best = float('-inf')
        best_move = None
        best_move_score = float('-inf')
        for move in gs.getValidMoves():
            gs.makeMove(move)
            if depth == self.checkmateDepth: # this is for checking wehther we can set our opponent to checkmate in the next move
                temp_score = self.evaluate(gs)
                if temp_score > best_move_score: # for storing a move in case our time runs out
                    best_move_score = temp_score
                    self.update_move(move, -1, -1)
                gs.getValidMoves() #to update inCheck and checkMate flags
                if len(gs.getValidMoves()) == 0 and not gs.inCheck:
                    gs.undoMove()
                    continue #choose a different move in case our move sets opponent to draw
                elif gs.checkMate:
                    self.enemyCheckmate = True
                    self.checkmateMove = move
                    break 
                if tuple(gs.board) in gs.game_log: 
                    if gs.game_log[tuple(gs.board)] + 1 == 3:
                        gs.undoMove()
                        if self.onlyKingLeft:
                        # force three fold repetition
                            self.forceThreefoldMove = move
                            break
                        else:
                        # avoid three fold repetition
                            continue
            if depth >= self.maxDepth:
                v = self.evaluate(gs)
            else:
                v, v_move = self.alpha_beta_min(depth + 1, gs, alpha, beta)
            if v > best:
                best = v
                best_move = move
            gs.undoMove()
            if v >= beta:
                break
            alpha = max(alpha, best)
        return best, best_move

    def alpha_beta_min(self, depth, gs, alpha, beta):
        best = float('inf')
        best_move = None
        for move in gs.getValidMoves():
            gs.makeMove(move)
            if depth >= self.maxDepth:
                v = self.evaluate(gs)
            else:
                v, v_move = self.alpha_beta_max(depth + 1, gs, alpha, beta)
            if depth == self.checkmateDepth + 1:
                gs.getValidMoves()
                if gs.checkMate:  # in case our agent is in danger of loosing in the next move by the opponent, he shouldn´t choose the move that lets the opponent set our agent to checkmate
                    v = float('-inf')
            if v < best:
                best = v
                best_move = move
            gs.undoMove()

            if v <= alpha:
                break

            beta = min(beta, best)
        return best, best_move
    
    def evaluate(self, gs):
        utility_value = 0
        for square in range(len(gs.board)):
            piece = gs.board[square]
            if piece == '--':
                continue
            else:
                double_pawn = 0
                if piece == "wp" or piece == "bp":
                    double_pawn = self.punish_double_pawn(gs, square)
                utility_value = utility_value + self.weights[piece] + 2 * self.find_piece_square_value(square, piece) + double_pawn
        return utility_value

    # Extra functions:

    def find_piece_square_value(self, square, piece):
        if self.color: # we only want the piece-square-values of our own pieces
            if piece == "wp":
                return self.wp_table[square]
            elif piece == "wN":
                return self.wN_table[square]
            elif piece == "wB":
                return self.wB_table[square]
            # elif piece == "wR":
            #     return self.wR_table[square]
            elif piece == "wK":
                if self.endGame:
                    return self.wK_table_endgame[square]
                else:
                    return self.wK_table[square]
            elif piece == "bp":
                return -0.5 * self.bp_table[square]
            elif piece == "bN":
                return -0.5 * self.bN_table[square]
            elif piece == "bB":
                return -0.5 * self.bB_table[square]
            # elif piece == "bR":
            #     return -0.5 * self.bR_table[square]
            elif piece == "bK":
                if self.endGame:
                    return -0.5 * self.bK_table_endgame[square]
                else:
                    return -0.5 * self.bK_table[square]
        else:
            if piece == "bp":
                return self.bp_table[square]
            elif piece == "bN":
                return self.bN_table[square]
            elif piece == "bB":
                return self.bB_table[square]
            # elif piece == "bR":
            #     return self.bR_table[square]
            elif piece == "bK":
                if self.endGame:
                    return self.bK_table_endgame[square]
                else:
                    return self.bK_table[square]
            elif piece == "wp":
                return -0.5 * self.wp_table[square]
            elif piece == "wN":
                return -0.5 * self.wN_table[square]
            elif piece == "wB":
                return -0.5 * self.wB_table[square]
            # elif piece == "wR":
            #     return -0.5 * self.wR_table[square]
            elif piece == "wK":
                if self.endGame:
                    return self.wK_table_endgame[square]
                else:
                    return -0.5 * self.wK_table[square]
        return 0

    def update_weights(self, gs):
        pawn_counter = 0
        board_value = 0
        our_piece_counter = 0
        for square in range(len(gs.board)):
            piece = gs.board[square]
            if piece == '--':
                continue
            board_value = board_value + abs(self.weights[piece]) # for determining whether we´re in endgame or not
            if self.color:
                if piece in ["wp", "wN", "wB", "wR", "wK"]:
                    our_piece_counter += 1
            else:
                if piece in ["bp", "bN", "bB", "bR", "bK"]:
                    our_piece_counter += 1
            if piece == "wp" or piece == "bp":
                pawn_counter += 1
        if our_piece_counter == 1:
            self.onlyKingLeft = True 
        if board_value <= 24000: # boundary for endgame status
            self.endGame = True
    
       # make pawns more valuable in endgame situations:
        if self.endGame:
            if self.color:
                self.weights["wp"] = 275
                self.weights["bp"] = -250
            else:
                self.weights["wp"] = -250
                self.weights["bp"] = 275
        # change weights of certain pieces considering the number of pawns left on the board
        if pawn_counter < 4:    # if there are few pawns left, pawns, rooks and bishops are more useful (-> more valuable)
            if self.color:
                self.weights["wp"] = 275
                self.weights["bp"] = -250
                self.weights["wR"] = 770
                self.weights["bR"] = -700
                self.weights["wB"] = 550
                self.weights["bB"] = -500
            else:
                self.weights["wp"] = -250
                self.weights["bp"] = 275
                self.weights["wR"] = -700
                self.weights["bR"] = 770
                self.weights["wB"] = -500
                self.weights["bB"] = 550
        else:                   # if there are many pawns left, knights are more useful (-> more valuable)
            if self.color:
                self.weights["wN"] = 550
                self.weights["bN"] = -500
            else:
                self.weights["wN"] = -500
                self.weights["bN"] = 550

    def king_safety(self, king_sqaure): # if king is in one of the corners (mostly after castling), the pawns should stay in front of the king to form a safety wall
        if self.color:
            if king_sqaure == 31:
                self.wp_table = [0, 0, 0, 0, 0, 0,
                                 50, 50, 50, 50, 50, 50,
                                 10, 25, 30, 30, 25, 10,
                                 5, 15, 20, 20, 15, 5,
                                 30, 30, 30, -25, 10, 5,
                                 0, 0, 0, 0, 0, 0]
            elif king_sqaure == 35:
                self.wp_table = [0, 0, 0, 0, 0, 0,
                                 50, 50, 50, 50, 50, 50,
                                 10, 25, 30, 30, 25, 10,
                                 5, 15, 20, 20, 15, 5,
                                 5, 10, -25, 30, 30, 30,
                                 0, 0, 0, 0, 0, 0]
        else:
            if king_sqaure == 1:
                self.bp_table = [0, 0, 0, 0, 0, 0,
                                 30, 30, 30, -25, 10, 5,
                                 5, 15, 20, 20, 15, 5,
                                 10, 25, 30, 30, 25, 10,
                                 50, 50, 50, 50, 50, 50,
                                 0, 0, 0, 0, 0, 0]
            elif king_sqaure == 5:
                 self.bp_table = [0, 0, 0, 0, 0, 0,
                                 5, 10, -25, 30, 30, 30,
                                 5, 15, 20, 20, 15, 5,
                                 10, 25, 30, 30, 25, 10,
                                 50, 50, 50, 50, 50, 50,
                                 0, 0, 0, 0, 0, 0]

    def punish_double_pawn(self, gs, square):
        if self.color:
            if gs.board[square - 6]:
                if gs.board[square - 6] == "wp": # piece directly above is a white pawn
                    return -50
        else:
            if gs.board[square + 6]:
                if gs.board[square + 6] == "bp": # piece directly below is a black pawn
                    return -50
        return 0


    

    ###  Functions that might be useful for further versions, but including them exceeds the time limit of 20 seconds ###
    # def calculate_mobility_value(self, gs, square, piece, color):
    #     mobility_value = 0
    #     validMoves = gs.getValidMoves()
    #     if len(validMoves) > 0:
    #         mobility_value += len(validMoves)
    #     surrounding_pieces, number_surrounding_pieces = self.get_surrounding_pieces(gs, square)
    #     if self.color:
    #         if piece == "wp":
    #             if surrounding_pieces[1] == "wp": #doubled pawn is punished
    #                 mobility_value -= 10
    #         if piece == "wR" or piece == "wB":
    #             if number_surrounding_pieces > 2:
    #                 mobility_value -= 5
    #             elif number_surrounding_pieces > 3:
    #                 mobility_value -= 10
    #             elif number_surrounding_pieces > 4:
    #                 mobility_value -= 15
    #             # elif number_surrounding_pieces > 5:
    #             #     mobility_value -= 20
    #     else:
    #         if piece == "bp": 
    #             if surrounding_pieces[7] == "bp": #doubled pawn is punished
    #                 mobility_value -= 10
    #         if piece == "bR" or piece == "bB":
    #             if number_surrounding_pieces > 2:
    #                 mobility_value -= 5
    #             elif number_surrounding_pieces > 3:
    #                 mobility_value -= 10
    #             elif number_surrounding_pieces > 4:
    #                 mobility_value -= 15
    #             # elif number_surrounding_pieces > 5:
    #             #     mobility_value -= 20
    #     return mobility_value
    
    # def get_surrounding_pieces(self, gs, square):
    #     '''
    #     0  1  2  3   4  5 
    #     6  7  8  9  10 11
    #     12 13 14 15 16 17
    #     18 19 20 21 22 23
    #     24 25 26 27 28 29
    #     30 31 32 33 34 35
    #     '''
    #     board = gs.board
    #     surrounding_pieces = [] 
    #     surrounding_squares = [square - 7, square - 6, square - 5, 
    #                            square - 1,   square,   square + 1, 
    #                            square + 5, square + 6, square + 7]
    #     number_surrounding_pieces = 0
    #     for index in surrounding_squares:
    #         if index >= 0 and index <= 35: #square is on the board
    #             if index in [0, 6, 12, 18, 24, 30] and square in [5, 11, 17, 23, 29, 35] or index in [5, 11, 17, 23, 29, 35] and square in [0, 6, 12, 18, 24, 30]: # edge-piece 
    #                 surrounding_pieces.append(-1)
    #             elif board[index] != "--":  
    #                 number_surrounding_pieces += 1
    #                 surrounding_pieces.append(board[index])
    #             else: 
    #                 surrounding_pieces.append(0)
    #         else: 
    #             surrounding_pieces.append(-1)
    #     return surrounding_pieces, number_surrounding_pieces