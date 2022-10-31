import random


import time


class Agent:
    def __init__(self):
        self.move_queue = None
        self.whiteWeights = {"wp": 110, "wN": 330, "wB": 330, "wR": 550, "wK": 11000,
                        "bp": -100, "bN": -300, "bB": -300, "bR": -500, "bK": -10000}
        self.blackWeights = {"wp": -100, "wN": -300, "wB": -300, "wR": -500, "wK": -10000,
                        "bp": 110, "bN": 330, "bB": 330, "bR": 550, "bK": 11000}
        # same weights for own & opponents pieces
        # self.whiteWeights = {"wp": 100, "wN": 300, "wB": 300, "wR": 500, "wK": 10000,
        #                 "bp": -100, "bN": -300, "bB": -300, "bR": -500, "bK": -10000}
        # self.blackWeights = {"wp": -100, "wN": -300, "wB": -300, "wR": -500, "wK": -10000,
        #                 "bp": 100, "bN": 300, "bB": 300, "bR": 500, "bK": 10000}
        self.weights = None
        self.maxDepth = 4
        self.checkmateDepth = 0
        self.enemyCheckmate = False
        self.enemyInCheck = False
        self.checkmateMove = None
        self.inCheckMove = None
        self.color = None
        self.endGame = False
        self.onlyKingLeft = False

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
        self.wR_table = [0, 0, 0, 0, 0, 0,
                         5, 10, 10, 10, 10, 5,
                         -5, 5, 5, 5, 5, -5,
                         -5, 0, 0, 0, 0, -5,
                         -5, 0, 0, 0, 0, -5,
                         -5, 0, 10, 10, 0, -5]
        self.bR_table = [-5, 0, 10, 10, 0, -5,
                         -5, 0, 0, 0, 0, -5,
                         -5, 0, 0, 0, 0, -5,
                         -5, 5, 5, 5, 5, -5,
                          5, 10, 10, 10, 10, 5,
                          0, 0, 0, 0, 0, 0,]
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
        # TODO
        print("Unser Agent ist dran")
        self.color = gs.whiteToMove
        negInf = float('-inf')
        posInf = float('inf')
        if self.color:
            self.weights = self.whiteWeights
        else:
            self.weights = self.blackWeights
        
        if self.calculate_abolute_piece_board_value(gs) <= 24000:
            self.endGame = True

        if self.endGame:
            self.onlyKingLeft = self.only_king_left(gs)

        move = None

        if self.onlyKingLeft:
            move = self.force_threefold_repetition(gs)
            self.update_move(move, -1, -1)
        else:
            # count pawns and change weights accordingly 
            self.update_weights(gs)

            if self.color:
                king_square = gs.board.index("wK")
            else:
                king_square = gs.board.index("bK")
            self.king_safety(king_square)

            best_v, move = self.alpha_beta_max(0, gs, negInf, posInf)
            print("move: ", move)
            print("enemy check: ", self.enemyInCheck)
            print("enemy checkmate: ", self.enemyCheckmate)
            if self.enemyInCheck and self.enemyCheckmate:
                self.update_move(self.inCheckMove, -1, -1)
            elif self.enemyCheckmate:
                self.update_move(self.checkmateMove, -1, -1)
            else: 
                self.update_move(move, -1, -1)
            # if self.enemyCheckmate:
            #     self.update_move(self.checkmateMove, -1, -1)
            # else: 
            #     self.update_move(move, -1, -1)
        

    def alpha_beta_max(self, depth, gs, alpha, beta, move = None):
        best = float('-inf')
        best_Move = None
        for move in gs.getValidMoves():
            gs.makeMove(move)
            if depth == self.checkmateDepth: # check if checkmateDepths move (at the moment first move) leads to a checkmate
                gs.getValidMoves()
                if tuple(gs.board) in gs.game_log:
                    print("if tuple(gs.board) in gs.game_log:")
                    if gs.game_log[tuple(gs.board)] + 1 == 3:
                        print("if gs.game_log[tuple(gs.board)] + 1 == 3:")
                        continue
                if len(gs.getValidMoves()) == 0 and not gs.inCheck:
                    print("if len(gs.getValidMoves()) == 0 and not gs.inCheck:")
                    continue
                elif gs.checkMate:
                    v = float('inf')
                    self.enemyCheckmate = True
                    self.checkmateMove = move
                elif gs.inCheck: # if not checkmate, then check if enemy is in check
                    v = float('inf')
                    self.enemyInCheck = True
                    self.inCheckMove = move
            if gs.checkMate and self.enemyInCheck: # if first move leads to an inCheck and second to a checkmate, then do the first move
                v = float('inf')
                self.enemyCheckmate = True
            if depth == self.maxDepth:
                v = self.evaluate(gs)
            else:
                v, v_move = self.alpha_beta_min(depth + 1, gs, alpha, beta, move)
            if v > best:
                best = v
                best_Move = move
            gs.undoMove()
            if v >= beta:
                break
            alpha = max(alpha, best)
        print("depth: ", depth)
        print("current_move: ", move)
        print("best_move: ", best_Move)
        if not best_Move:
            best_Move = move
        return best, best_Move
    
    # old:
    # def alpha_beta_max(self, depth, gs, alpha, beta, move = None):
    #     if depth == self.maxDepth or len(gs.getValidMoves()) == 0:
    #         if gs.checkMate:
    #             returnValue = float('-inf')
    #         else:
    #             returnValue = self.evaluate(gs)
    #         return returnValue, None
    #     best = float('-inf')
    #     best_Move = None
    #     for move in gs.getValidMoves():
    #         gs.makeMove(move)
    #         v, v_move = self.alpha_beta_min(depth + 1, gs, alpha, beta, move)
    #         if v > best:
    #             best = v
    #             best_Move = move
    #         gs.undoMove()
    #         if v >= beta:
    #             break
    #         alpha = max(alpha, best)
    #     return best, best_Move

    def alpha_beta_min(self, depth, gs, alpha, beta, move = None):
        best = float('inf')
        best_Move = None
        for move in gs.getValidMoves():
            gs.makeMove(move)
            if depth == self.checkmateDepth:
            # new: if depth == self.checkmateDepth + 1:
                gs.getValidMoves()
                if gs.checkMate:
                    v = float('-inf')
            if depth == self.maxDepth:
                v = self.evaluate(gs)
            else:
                v, v_move = self.alpha_beta_max(depth + 1, gs, alpha, beta, move)
            if v < best:
                best = v
                #best_Move = v_move
                best_move = move
            gs.undoMove()
            if v <= alpha:
                break
            beta = min(beta, best)
        return best, best_Move

    # Old:
    # def alpha_beta_min(self, depth, gs, alpha, beta, move = None):
    #     if depth == self.maxDepth:
    #         return self.evaluate(gs)
    #     if depth == self.checkmateDepth and len(gs.getValidMoves()) == 0: # enemy checkmate bc after agent makes a move there are no validmoves left for the enemy 
    #         returnValue = float('inf')
    #         self.enemyCheckmate = True
    #         self.checkmateMove = move
    #         return returnValue, move
    #     best = float('inf')
    #     best_Move = None
    #     for move in gs.getValidMoves():
    #         gs.makeMove(move)
    #         v, v_move = self.alpha_beta_max(depth + 1, gs, alpha, beta, move)
    #         if v < best:
    #             best = v
    #             best_Move = move
    #         gs.undoMove()
    #         if v <= alpha:
    #             break
    #         beta = min(beta, best)
    #     return best, best_Move


    def evaluate(self, gs): 
        utility_value = 0
        for square in range(len(gs.board)):
            piece = gs.board[square] 
            if piece == '--':
                continue
            mobility_value = 0
            double_pawn = 0
            #if piece == "wp" or piece == "bp" or piece == "wR" or piece == "bR" or piece == "wB" or piece == "bB":
            if piece == "wp" or piece == "bp":
                #mobility_value = self.calculate_mobility_value(gs, square, piece, self.color)
                double_pawn = self.punish_double_pawn(gs, square)
            #utility_value = utility_value + self.weights[piece] + self.find_piece_square_value(square, piece) + 0.25 * mobility_value # evaluate board via piece values and piece-square-table-values
            utility_value = utility_value + self.weights[piece] + self.find_piece_square_value(square, piece) + double_pawn
        
        return utility_value 

    
    def calculate_abolute_piece_board_value(self, gs):
        '''
        Function needed to determine whether we have an endgame situation
        ''' 
        utility_value = 0
        for square in range(len(gs.board)):
            piece = gs.board[square] 
            if piece == '--':
                continue
            utility_value = utility_value + abs(self.weights[piece])
        return utility_value

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
    
    def calculate_mobility_value(self, gs, square, piece, color):
        mobility_value = 0
        validMoves = gs.getValidMoves()
        if len(validMoves) > 0:
            mobility_value += len(validMoves)
        surrounding_pieces, number_surrounding_pieces = self.get_surrounding_pieces(gs, square)
        if self.color:
            if piece == "wp":
                if surrounding_pieces[1] == "wp": #doubled pawn is punished
                    mobility_value -= 10
            if piece == "wR" or piece == "wB":
                if number_surrounding_pieces > 2:
                    mobility_value -= 5
                elif number_surrounding_pieces > 3:
                    mobility_value -= 10
                elif number_surrounding_pieces > 4:
                    mobility_value -= 15
                # elif number_surrounding_pieces > 5:
                #     mobility_value -= 20
        else:
            if piece == "bp": 
                if surrounding_pieces[7] == "bp": #doubled pawn is punished
                    mobility_value -= 10
            if piece == "bR" or piece == "bB":
                if number_surrounding_pieces > 2:
                    mobility_value -= 5
                elif number_surrounding_pieces > 3:
                    mobility_value -= 10
                elif number_surrounding_pieces > 4:
                    mobility_value -= 15
                # elif number_surrounding_pieces > 5:
                #     mobility_value -= 20
        return mobility_value
    
    def get_surrounding_pieces(self, gs, square):
        '''
        0  1  2  3   4  5 
        6  7  8  9  10 11
        12 13 14 15 16 17
        18 19 20 21 22 23
        24 25 26 27 28 29
        30 31 32 33 34 35
        '''
        board = gs.board
        surrounding_pieces = [] 
        surrounding_squares = [square - 7, square - 6, square - 5, 
                               square - 1,   square,   square + 1, 
                               square + 5, square + 6, square + 7]
        number_surrounding_pieces = 0
        for index in surrounding_squares:
            if index >= 0 and index <= 35: #square is on the board
                if index in [0, 6, 12, 18, 24, 30] and square in [5, 11, 17, 23, 29, 35] or index in [5, 11, 17, 23, 29, 35] and square in [0, 6, 12, 18, 24, 30]: # edge-piece 
                    surrounding_pieces.append(-1)
                elif board[index] != "--":  
                    number_surrounding_pieces += 1
                    surrounding_pieces.append(board[index])
                else: 
                    surrounding_pieces.append(0)
            else: 
                surrounding_pieces.append(-1)
        return surrounding_pieces, number_surrounding_pieces

    def update_weights(self, gs):
        # make pawns more valuable in endgame situations:
        if self.endGame:
            if self.color:
                self.weights["wp"] = 275
                self.weights["bp"] = -250
            else: 
                self.weights["wp"] = -250
                self.weights["bp"] = 275
        # change weights of certain pieces considering the number of pawns left on the board
        pawn_counter = 0
        for square in range(len(gs.board)):
            piece = gs.board[square]
            if piece == '--':
                continue
            if piece == "wp" or piece == "bp":
                    pawn_counter += 1
        if pawn_counter < 4:    # if there are few pawns left, pawns, rooks and bishops are more useful (-> more valuable) 
            if self.color:
                self.weights["wp"] = 275
                self.weights["bp"] = -250
                self.weights["wR"] = 770
                self.weights["bR"] = -700
                self.weights["wB"] = 550
                self.weights["bB"] = -500
                ## same weights for own and opponents pieces:
                # self.weights["wp"] = 250
                # self.weights["bp"] = -250
                # self.weights["wR"] = 700
                # self.weights["bR"] = -700
                # self.weights["wB"] = 500
                # self.weights["bB"] = -500
            else:
                self.weights["wp"] = -250
                self.weights["bp"] = 275
                self.weights["wR"] = -700
                self.weights["bR"] = 770
                self.weights["wB"] = -500
                self.weights["bB"] = 550
                ## same weights for own and opponents pieces:
                # self.weights["wp"] = -250
                # self.weights["bp"] = 250
                # self.weights["wR"] = -700
                # self.weights["bR"] = 700
                # self.weights["wB"] = -500
                # self.weights["bB"] = 500

        else:                   # if there are many pawns left, knights are more useful (-> more valuable)
            if self.color:
                self.weights["wN"] = 550
                self.weights["bN"] = -500
                ## same weights for own and opponents pieces:
                # self.weights["wN"] = 500
                # self.weights["bN"] = -500
            else:
                self.weights["wN"] = -500
                self.weights["bN"] = 550
                ## same weights for own and opponents pieces:
                # self.weights["wN"] = -500
                # self.weights["bN"] = 500
        
    
    def find_piece_square_value(self, square, piece):
        if self.color: # we only want the piece-square-values of our own pieces
            if piece == "wp":
                return self.wp_table[square]
            elif piece == "wN":
                return self.wN_table[square]
            elif piece == "wB":
                return self.wB_table[square]
            elif piece == "wR":
                return self.wR_table[square]
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
            elif piece == "bR":
                return -0.5 * self.bR_table[square]
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
            elif piece == "bR":
                return self.bR_table[square]
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
            elif piece == "wR":
                return -0.5 * self.wR_table[square]
            elif piece == "wK":
                if self.endGame:
                    return self.wK_table_endgame[square]
                else:
                    return -0.5 * self.wK_table[square]
        return 0
    
    def king_safety(self, king_sqaure):
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
        
    def only_king_left(self, gs):
        if self.color:
            for square in range(len(gs.board)):
                piece = gs.board[square]
                if piece in ["wp", "wB", "wN", "wR"]:
                    return False
        elif not self.color: 
            for square in range(len(gs.board)):
                piece = gs.board[square]
                if piece in ["bp", "bB", "bN", "bR"]:
                    return False
        return True

    def force_threefold_repetition(self, gs):
        for move in gs.getValidMoves():
            gs.makeMove(move)
            if tuple(gs.board) in gs.game_log:
                    if gs.game_log[tuple(gs.board)] + 1 == 3:
                        gs.undoMove()
                        return move
            gs.undoMove()
        return None



                





    def update_pawn_table(self, move):
        if move == "O-O":
            if self.color: # agent plays white
                self.wp_table = [100, 100, 100, 100, 100, 100,
                                 50, 50, 50, 50, 50, 50,
                                 10, 25, 30, 30, 25, 10,
                                 5, 15, 20, 20, 15, 5,
                                 5, 10, -25, 30, 30, 30,
                                 0, 0, 0, 0, 0, 0]
            else:   # agent plays black
                self.bp_table = [0, 0, 0, 0, 0, 0, 
                                 5, 10, -25, 30, 30, 30,
                                 5, 15, 20, 20, 15, 5,
                                 10, 25, 30, 30, 25, 10,
                                 50, 50, 50, 50, 50, 50,
                                 100, 100, 100, 100, 100, 100]
        else:
            if self.color: 
                self.wp_table = [100, 100, 100, 100, 100, 100,
                                 50, 50, 50, 50, 50, 50,
                                 10, 25, 30, 30, 25, 10,
                                 5, 15, 20, 20, 15, 5,
                                 30, 30, 30, -25, 10, 5,
                                 0, 0, 0, 0, 0, 0]
            else:
                self.bp_table = [0, 0, 0, 0, 0, 0, 
                                 30, 30, 30, -25, 10, 5,
                                 5, 15, 20, 20, 15, 5,
                                 10, 25, 30, 30, 25, 10,
                                 50, 50, 50, 50, 50, 50,
                                 100, 100, 100, 100, 100, 100]
                                














    ########
    def simpleheuristic(self, gs):
        heuristicValue = 0
        for piece in gs.board:
            if piece == '--':
                continue
            heuristicValue += self.weights[piece]
        return heuristicValue

    
    def findBestMoveWithTime(self, gs, validMoves, time_limit = 19.5): 
        """
        Parameters
        ----------
        gs : Gamestate
            current state of the game
        validMoves: list
            list of valid moves
        time_limit : time
            time limit the agent has to make a move
        """
        limit = time.time() + time_limit
        #action = self.minimax(gs, validMoves, limit)
        action = self.alpha_beta_search(0, gs, validMoves, limit)
        return action

    ### START: alpha-beta-pruning ###
    def alpha_beta_search(self, depth, gs, validMoves, time_limit):
        best_v = self.a_b_max_value(gs, float('-inf'), float('inf'), time_limit)
        for move in validMoves:
            if best_v == self.evaluate(move):
                action = move
                break
        return action
    
    def a_b_max_value(self, gs, alpha, beta, time_limit):
        # if terminal_test(gs):
        #   return self.evaluate(self.board)
        # terminal-test can either be check-mate or depth (see depth-limited-search) or time
        v = float('-inf')
        validMoves = gs.getValidMoves()
        for move in validMoves:
            if time.time() < time_limit:
                gs.makeMove(move)
                v = max(v, self.a_b_min_value(gs, alpha, beta, time_limit))
                gs.undoMove()
                if v >= beta:
                    return v
                alpha = max(alpha, v)
            else:
                v = self.evaluate(move)
        return v

    def a_b_min_value(self, gs, alpha, beta, time_limit):
        # if terminal_test(gs):
        #   return self.evaluate(self.board)
        # terminal-test can either be check-mate or depth (see depth-limited-search) or time
        v = float('inf')
        validMoves = gs.getValidMoves()
        for move in validMoves:
            if time.time() < time_limit:
                gs.makeMove(move)
                v = min(v, self.a_b_max_value(gs, alpha, beta, time_limit))
                gs.undoMove()
                if v <= alpha:
                    return v
                beta = min(beta, v)
            else:
                v = self.evaluate(move)
        return v
    
    ### END: alpha-beta-pruning ###

    def minimax(self, gs, validMoves, time_limit):
        """
        Parameters
        ----------
        gs : Gamestate
            current state of the game
        """
        #action = max(self.min_value(gs, time_limit))
        best_v = self.min_value(gs, time_limit)
        #action = validMoves[0]
        for move in validMoves:
            if best_v == self.evaluate(move):
                action = move
                break
        return action

        
    def max_value(self, gs, time_limit):
        # if terminal_test(gs):
        #   return self.evaluate(self.board)
        # terminal-test can either be check-mate or depth (see depth-limited-search) or time
        v = float('-inf')
        validMoves = gs.getValidMoves()
        for move in validMoves:
            if time.time() < time_limit:
                v = max(v, self.min_value(self.update_move(move, -1, -1).board, time_limit))
            else: 
                v = self.evaluate(move)
        return v

    def min_value(self, gs, time_limit):
        # if terminal_test(gs):
        #   return self.evaluate(self.board)
        # terminal-test can either be check-mate or depth (see depth-limited-search) or time
        v = float('inf')
        validMoves = gs.getValidMoves()
        for move in validMoves:
            if time.time() < time_limit:
                v = min(v, self.max_value(self.update_move(move, -1, -1).board, time_limit))
            else:
                v = self.evaluate(move)
        return v
    '''
    def evaluate(self, gs):
        ### START: counting pawns and change weights accordingly ###
        pawn_counter = 0
        for square in range(len(gs.board)):
            piece = gs.board[square]
            if piece != '--':
                if piece == "wp" or piece == "bp":
                    pawn_counter += 1
                if 
        if pawn_counter < 2:
            stop_counting = True
            self.weights["wp"] = 250
            self.weights["bp"] = -250
            self.weights["wR"] = 700
            self.weights["bR"] = -700
            self.weights["wB"] = 500
            self.weights["bB"] = -500
        else:
            self.weights["wN"] = 500
            self.weights["bN"] = -500
        
        ### END: counting pawns and change weights accordingly ###

        ### START: evaluate piece values ###
        utility_value = 0
        for square in range(len(gs.board)):
            piece = gs.board[square]
            if piece == '--':
                continue
            utility_value += self.weights[piece]
        ### END: evaluate piece values ###
        return utility_value 
    '''

'''

import random

### MY IMPORTS ###
import time


class Agent:
    def __init__(self):
        self.move_queue = None
        self.WhiteWeights = {"wp": 100, "wN": 300, "wB": 300, "wR": 500, "wK": 10000,
                        "bp": -100, "bN": -300, "bB": -300, "bR": -500, "bK": -10000}
        self.BlackWeights = {"wp": -100, "wN": -300, "wB": -300, "wR": -500, "wK": -10000,
                        "bp": 100, "bN": 300, "bB": 300, "bR": 500, "bK": 10000}
        self.weights = None
        # self.weights = {"wp": 100, "wN" : 300, "wB": 300, "wR" : 500, "wK" : 10000,
        #            "bp": -100, "bN" : -300, "bB": -300, "bR" : -500, "bK" : -10000}
        self.maxDepth = 4 

        self.wp_table = [100, 100, 100, 100, 100, 100,
                         50, 50, 50, 50, 50, 50,
                         10, 25, 30, 30, 25, 10,
                         5, 15, 20, 20, 15, 5,
                         5, 10, -25, -25, 10, 5,
                         0, 0, 0, 0, 0, 0]
        self.bp_table = [0, 0, 0, 0, 0, 0, 
                         -5, -10, 25, 25, -10, -5,
                         -5, -15, -20, -20, -15, -5,
                         -10, -25, -30, -30, -25, -10,
                         -50, -50, -50, -50, -50, -50,
                         -100, -100, -100, -100, -100, -100]
        self.wN_table = [-50, -30, -30, -30, -40, -50,
                         -40, 10, 15, 15, 10, -40,
                         -30, 10, 20, 20, 10, -30,
                         -30, 10, 20, 20, 10, -30,
                         -40, 10, 15, 15, 10, -40,
                         -50, -40, -30, -30, -40, -50]
        self.bN_table = [-x for x in self.wN_table]
        self.wB_table = [-20, -10, -10, -10, -10, -20,
                         -10, 0, 0, 0, 0, -10,
                         -10, 5, 10, 10, 5, -10,
                         -10, 10, 10, 10, 10, -10,
                         -10, 5, 0, 0, 5, -10,
                         -20, -40, -10, -10, -40, -20]
        self.bB_table = [20, 40, 10, 10, 40, 20,
                         10, -5, 0, 0, -5, 10,
                         10, -10, -10, -10, -10, 10,
                         10, -5, -10, -10, -5, 10,
                         10, 0, 0, 0, 0, 10,
                         20, 10, 10, 10, 10, 20]

        self.wR_table = [0, 0, 0, 0, 0, 0,
                         5, 10, 10, 10, 10, 5,
                         -5, 5, 5, 5, 5, -5,
                         -5, 0, 0, 0, 0, -5,
                         -5, 0, 0, 0, 0, -5,
                         -5, 0, 5, 5, 0, -5]
        self.bR_table = [5, 0, -5, -5, 0, 5,
                         5, 0, 0, 0, 0, 5,
                         5, 0, 0, 0, 0, 5,
                         5, -5, -5, -5, -5, 5,
                         -5, -10, -10, -10, -10, -5,
                          0, 0, 0, 0, 0, 0,]

        self.wK_table = [-30, -40, -50, -50, -40, -30,
                         -30, -40, -50, -50, -40, -30,
                         -30, -40, -50, -50, -40, -30,
                         -10, -20, -20, -20, -20, -10,
                         20, 20, 0, 0, 20, 20,
                         20, 30, 10, 0, 10, 30]
        self.bK_table = [-20, -30, -10, 0, -10, -30,
                         -20, -20, 0, 0, -20, -20,
                         10, 20, 20, 20, 20, 10,
                         30, 40, 50, 50, 40, 30,
                         30, 40, 50, 50, 40, 30,
                         30, 40, 50, 50, 40, 30]

        self.wK_table_endgame = [-50, -40, -30, -30, -40, -50,
                                 -30, -20, 0, 0, -20, -30,
                                 -30, 0, 30, 30, 0, -30,
                                 -30, 0, 30, 30, 0, -30,
                                 -30, -20, 0, 0, -20, -30,
                                 -50, -40, -30, -30, -40, -50]
        self.bK_table_endgame = [-x for x in self.wK_table_endgame]


        

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
        # TODO
        validMoves = gs.getValidMoves()
        self.color = gs.whiteToMove
        # if self.color:
        #     self.weights = self.WhiteWeights
        # else:
        #     self.weights = self.BlackWeights
        # best_v, move = self.alpha_beta_max(0, gs, float('-inf'), float('inf'))
        #"""
        if self.color:
            best_v, move = self.alpha_beta_max(0, gs, float('-inf'), float('inf'))
        else:
            best_v, move = self.alpha_beta_min(0, gs, float('-inf'), float('inf'))
        #"""
        #move = self.findBestMoveWithTime(gs, validMoves)
        #print(f"v of the FINALLY CHOSEN move {move}: {best_v}")
        # if move == "O-O" or move == "O-O-O":
            # make pawns in front of king more valuable
        self.update_move(move, -1, -1)
    


    ### BETTER: two in one ###
    def alpha_beta_max(self, depth, gs, alpha, beta):
        if depth == self.maxDepth:
            #return self.simpleheuristic(gs), None
            return self.evaluate(gs), None
        best = float('-inf')
        best_Move = None
        validMoves = gs.getValidMoves()
        if len(validMoves) == 0:
            return self.evaluate(gs), None
        for move in gs.getValidMoves():
            gs.makeMove(move)
            # check for check_mate of opponent. if yes: return that move!
            v, v_move = self.alpha_beta_min(depth + 1, gs, alpha, beta)
            if v > best:
                best = v
                best_Move = move
            #print(f"v of the move {move} in a_b_max:  {v}")
            gs.undoMove()
            #print("--- new move ---")
            if v >= beta:
                break
            alpha = max(alpha, best)
        return best, best_Move

    def alpha_beta_min(self, depth, gs, alpha, beta):
        if depth == self.maxDepth:
            #return self.simpleheuristic(gs), None
            return self.evaluate(gs), None
        best = float('inf')
        best_Move = None
        validMoves = gs.getValidMoves()
        if len(validMoves) == 0:
            return self.evaluate(gs), None
        for move in gs.getValidMoves():
            gs.makeMove(move)
            # check for check_mate of opponent. if yes: return that move!
            v, v_move = self.alpha_beta_max(depth + 1, gs, alpha, beta)
            if v < best:
                best = v
                best_Move = move
            #print(f"v of the move {move} in a_b_min:  {v}")
            gs.undoMove()
            #print("--- new move ---")
            if v <= alpha:
                break
            beta = min(beta, best)
        return best, best_Move


    def evaluate(self, gs):

        ### START: counting pawns and change weights accordingly ###
        pawn_counter = 0
        for square in range(len(gs.board)):
            piece = gs.board[square]
            if piece != '--':
                if piece == "wp" or piece == "bp":
                    pawn_counter += 1
        if pawn_counter < 2:    # bei wenigen Bauern sind Bauern wertvoller & Türme und Läufer auch. 
            stop_counting = True
            self.weights["wp"] = 250
            self.weights["bp"] = -250
            self.weights["wR"] = 700
            self.weights["bR"] = -700
            self.weights["wB"] = 500
            self.weights["bB"] = -500
        else:                   # bei vielen Bauern sind Springer wertvoller
            self.weights["wN"] = 500
            self.weights["bN"] = -500
        ### END: counting pawns and change weights accordingly ###

        ### START: evaluate piece values ###
        utility_value = 0
        for square in range(len(gs.board)):
            piece = gs.board[square] 
            if piece == '--':
                continue
            piece_square_value = self.find_piece_square_value(square, piece)
            utility_value = utility_value + self.weights[piece] + piece_square_value
        ### END: evaluate piece values ###
        return utility_value 

    def find_piece_square_value(self, square, piece):
        if piece == "wp":
            return self.wp_table[square]
        elif piece == "bp":
            return self.bp_table[square]
        elif piece == "wN":
            return self.wN_table[square]
        elif piece == "bN":
            return self.bN_table[square]
        elif piece == "wB":
            return self.wB_table[square]
        elif piece == "bB":
            return self.bB_table[square]
        elif piece == "wR":
            return self.wR_table[square]
        elif piece == "bR":
            return self.bR_table[square]
        elif piece == "wK":
            return self.wK_table[square]
        elif piece == "bK":
            return self.bK_table[square]
        return 0
        



    ########
    def simpleheuristic(self, gs):
        heuristicValue = 0
        for piece in gs.board:
            if piece == '--':
                continue
            heuristicValue += self.weights[piece]
        return heuristicValue

    
    def findBestMoveWithTime(self, gs, validMoves, time_limit = 19.5): 
        """
        Parameters
        ----------
        gs : Gamestate
            current state of the game
        validMoves: list
            list of valid moves
        time_limit : time
            time limit the agent has to make a move
        """
        limit = time.time() + time_limit
        #action = self.minimax(gs, validMoves, limit)
        action = self.alpha_beta_search(0, gs, validMoves, limit)
        return action

    ### START: alpha-beta-pruning ###
    def alpha_beta_search(self, depth, gs, validMoves, time_limit):
        best_v = self.a_b_max_value(gs, float('-inf'), float('inf'), time_limit)
        for move in validMoves:
            if best_v == self.evaluate(move):
                action = move
                break
        return action
    
    def a_b_max_value(self, gs, alpha, beta, time_limit):
        # if terminal_test(gs):
        #   return self.evaluate(self.board)
        # terminal-test can either be check-mate or depth (see depth-limited-search) or time
        v = float('-inf')
        validMoves = gs.getValidMoves()
        for move in validMoves:
            if time.time() < time_limit:
                gs.makeMove(move)
                v = max(v, self.a_b_min_value(gs, alpha, beta, time_limit))
                gs.undoMove()
                if v >= beta:
                    return v
                alpha = max(alpha, v)
            else:
                v = self.evaluate(move)
        return v

    def a_b_min_value(self, gs, alpha, beta, time_limit):
        # if terminal_test(gs):
        #   return self.evaluate(self.board)
        # terminal-test can either be check-mate or depth (see depth-limited-search) or time
        v = float('inf')
        validMoves = gs.getValidMoves()
        for move in validMoves:
            if time.time() < time_limit:
                gs.makeMove(move)
                v = min(v, self.a_b_max_value(gs, alpha, beta, time_limit))
                gs.undoMove()
                if v <= alpha:
                    return v
                beta = min(beta, v)
            else:
                v = self.evaluate(move)
        return v
    
    ### END: alpha-beta-pruning ###

    def minimax(self, gs, validMoves, time_limit):
        """
        Parameters
        ----------
        gs : Gamestate
            current state of the game
        """
        #action = max(self.min_value(gs, time_limit))
        best_v = self.min_value(gs, time_limit)
        #action = validMoves[0]
        for move in validMoves:
            if best_v == self.evaluate(move):
                action = move
                break
        return action

        
    def max_value(self, gs, time_limit):
        # if terminal_test(gs):
        #   return self.evaluate(self.board)
        # terminal-test can either be check-mate or depth (see depth-limited-search) or time
        v = float('-inf')
        validMoves = gs.getValidMoves()
        for move in validMoves:
            if time.time() < time_limit:
                v = max(v, self.min_value(self.update_move(move, -1, -1).board, time_limit))
            else: 
                v = self.evaluate(move)
        return v

    def min_value(self, gs, time_limit):
        # if terminal_test(gs):
        #   return self.evaluate(self.board)
        # terminal-test can either be check-mate or depth (see depth-limited-search) or time
        v = float('inf')
        validMoves = gs.getValidMoves()
        for move in validMoves:
            if time.time() < time_limit:
                v = min(v, self.max_value(self.update_move(move, -1, -1).board, time_limit))
            else:
                v = self.evaluate(move)
        return v
    
    # def evaluate(self, gs):
    #     ### START: counting pawns and change weights accordingly ###
    #     pawn_counter = 0
    #     for square in range(len(gs.board)):
    #         piece = gs.board[square]
    #         if piece != '--':
    #             if piece == "wp" or piece == "bp":
    #                 pawn_counter += 1
    #             if 
    #     if pawn_counter < 2:
    #         stop_counting = True
    #         self.weights["wp"] = 250
    #         self.weights["bp"] = -250
    #         self.weights["wR"] = 700
    #         self.weights["bR"] = -700
    #         self.weights["wB"] = 500
    #         self.weights["bB"] = -500
    #     else:
    #         self.weights["wN"] = 500
    #         self.weights["bN"] = -500
        
    #     ### END: counting pawns and change weights accordingly ###

    #     ### START: evaluate piece values ###
    #     utility_value = 0
    #     for square in range(len(gs.board)):
    #         piece = gs.board[square]
    #         if piece == '--':
    #             continue
    #         utility_value += self.weights[piece]
    #     ### END: evaluate piece values ###
    #     return utility_value 
    
        
    

'''

    
            


    

    
    

    









    
            


    

    
    

    




'''

import random

### MY IMPORTS ###
import time


class Agent:
    def __init__(self):
        self.move_queue = None
        self.WhiteWeights = {"wp": 100, "wN": 300, "wB": 300, "wR": 500, "wK": 10000,
                        "bp": -100, "bN": -300, "bB": -300, "bR": -500, "bK": -10000}
        self.BlackWeights = {"wp": -100, "wN": -300, "wB": -300, "wR": -500, "wK": -10000,
                        "bp": 100, "bN": 300, "bB": 300, "bR": 500, "bK": 10000}
        self.weights = None
        # self.weights = {"wp": 100, "wN" : 300, "wB": 300, "wR" : 500, "wK" : 10000,
        #            "bp": -100, "bN" : -300, "bB": -300, "bR" : -500, "bK" : -10000}
        self.maxDepth = 4 

        self.wp_table = [100, 100, 100, 100, 100, 100,
                         50, 50, 50, 50, 50, 50,
                         10, 25, 30, 30, 25, 10,
                         5, 15, 20, 20, 15, 5,
                         5, 10, -25, -25, 10, 5,
                         0, 0, 0, 0, 0, 0]
        self.bp_table = [0, 0, 0, 0, 0, 0, 
                         -5, -10, 25, 25, -10, -5,
                         -5, -15, -20, -20, -15, -5,
                         -10, -25, -30, -30, -25, -10,
                         -50, -50, -50, -50, -50, -50,
                         -100, -100, -100, -100, -100, -100]
        self.wN_table = [-50, -30, -30, -30, -40, -50,
                         -40, 10, 15, 15, 10, -40,
                         -30, 10, 20, 20, 10, -30,
                         -30, 10, 20, 20, 10, -30,
                         -40, 10, 15, 15, 10, -40,
                         -50, -40, -30, -30, -40, -50]
        self.bN_table = [-x for x in self.wN_table]
        self.wB_table = [-20, -10, -10, -10, -10, -20,
                         -10, 0, 0, 0, 0, -10,
                         -10, 5, 10, 10, 5, -10,
                         -10, 10, 10, 10, 10, -10,
                         -10, 5, 0, 0, 5, -10,
                         -20, -40, -10, -10, -40, -20]
        self.bB_table = [20, 40, 10, 10, 40, 20,
                         10, -5, 0, 0, -5, 10,
                         10, -10, -10, -10, -10, 10,
                         10, -5, -10, -10, -5, 10,
                         10, 0, 0, 0, 0, 10,
                         20, 10, 10, 10, 10, 20]

        self.wR_table = [0, 0, 0, 0, 0, 0,
                         5, 10, 10, 10, 10, 5,
                         -5, 5, 5, 5, 5, -5,
                         -5, 0, 0, 0, 0, -5,
                         -5, 0, 0, 0, 0, -5,
                         -5, 0, 5, 5, 0, -5]
        self.bR_table = [5, 0, -5, -5, 0, 5,
                         5, 0, 0, 0, 0, 5,
                         5, 0, 0, 0, 0, 5,
                         5, -5, -5, -5, -5, 5,
                         -5, -10, -10, -10, -10, -5,
                          0, 0, 0, 0, 0, 0,]

        self.wK_table = [-30, -40, -50, -50, -40, -30,
                         -30, -40, -50, -50, -40, -30,
                         -30, -40, -50, -50, -40, -30,
                         -10, -20, -20, -20, -20, -10,
                         20, 20, 0, 0, 20, 20,
                         20, 30, 10, 0, 10, 30]
        self.bK_table = [-20, -30, -10, 0, -10, -30,
                         -20, -20, 0, 0, -20, -20,
                         10, 20, 20, 20, 20, 10,
                         30, 40, 50, 50, 40, 30,
                         30, 40, 50, 50, 40, 30,
                         30, 40, 50, 50, 40, 30]

        self.wK_table_endgame = [-50, -40, -30, -30, -40, -50,
                                 -30, -20, 0, 0, -20, -30,
                                 -30, 0, 30, 30, 0, -30,
                                 -30, 0, 30, 30, 0, -30,
                                 -30, -20, 0, 0, -20, -30,
                                 -50, -40, -30, -30, -40, -50]
        self.bK_table_endgame = [-x for x in self.wK_table_endgame]


        

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
        # TODO
        validMoves = gs.getValidMoves()
        self.color = gs.whiteToMove
        # if self.color:
        #     self.weights = self.WhiteWeights
        # else:
        #     self.weights = self.BlackWeights
        # best_v, move = self.alpha_beta_max(0, gs, float('-inf'), float('inf'))
        #"""
        if self.color:
            best_v, move = self.alpha_beta_max(0, gs, float('-inf'), float('inf'))
        else:
            best_v, move = self.alpha_beta_min(0, gs, float('-inf'), float('inf'))
        #"""
        #move = self.findBestMoveWithTime(gs, validMoves)
        #print(f"v of the FINALLY CHOSEN move {move}: {best_v}")
        # if move == "O-O" or move == "O-O-O":
            # make pawns in front of king more valuable
        self.update_move(move, -1, -1)
    


    ### BETTER: two in one ###
    def alpha_beta_max(self, depth, gs, alpha, beta):
        if depth == self.maxDepth:
            #return self.simpleheuristic(gs), None
            return self.evaluate(gs), None
        best = float('-inf')
        best_Move = None
        validMoves = gs.getValidMoves()
        if len(validMoves) == 0:
            return self.evaluate(gs), None
        for move in gs.getValidMoves():
            gs.makeMove(move)
            # check for check_mate of opponent. if yes: return that move!
            v, v_move = self.alpha_beta_min(depth + 1, gs, alpha, beta)
            if v > best:
                best = v
                best_Move = move
            #print(f"v of the move {move} in a_b_max:  {v}")
            gs.undoMove()
            #print("--- new move ---")
            if v >= beta:
                break
            alpha = max(alpha, best)
        return best, best_Move

    def alpha_beta_min(self, depth, gs, alpha, beta):
        if depth == self.maxDepth:
            #return self.simpleheuristic(gs), None
            return self.evaluate(gs), None
        best = float('inf')
        best_Move = None
        validMoves = gs.getValidMoves()
        if len(validMoves) == 0:
            return self.evaluate(gs), None
        for move in gs.getValidMoves():
            gs.makeMove(move)
            # check for check_mate of opponent. if yes: return that move!
            v, v_move = self.alpha_beta_max(depth + 1, gs, alpha, beta)
            if v < best:
                best = v
                best_Move = move
            #print(f"v of the move {move} in a_b_min:  {v}")
            gs.undoMove()
            #print("--- new move ---")
            if v <= alpha:
                break
            beta = min(beta, best)
        return best, best_Move


    def evaluate(self, gs):

        ### START: counting pawns and change weights accordingly ###
        pawn_counter = 0
        for square in range(len(gs.board)):
            piece = gs.board[square]
            if piece != '--':
                if piece == "wp" or piece == "bp":
                    pawn_counter += 1
        if pawn_counter < 2:    # bei wenigen Bauern sind Bauern wertvoller & Türme und Läufer auch. 
            stop_counting = True
            self.weights["wp"] = 250
            self.weights["bp"] = -250
            self.weights["wR"] = 700
            self.weights["bR"] = -700
            self.weights["wB"] = 500
            self.weights["bB"] = -500
        else:                   # bei vielen Bauern sind Springer wertvoller
            self.weights["wN"] = 500
            self.weights["bN"] = -500
        ### END: counting pawns and change weights accordingly ###

        ### START: evaluate piece values ###
        utility_value = 0
        for square in range(len(gs.board)):
            piece = gs.board[square] 
            if piece == '--':
                continue
            piece_square_value = self.find_piece_square_value(square, piece)
            utility_value = utility_value + self.weights[piece] + piece_square_value
        ### END: evaluate piece values ###
        return utility_value 

    def find_piece_square_value(self, square, piece):
        if piece == "wp":
            return self.wp_table[square]
        elif piece == "bp":
            return self.bp_table[square]
        elif piece == "wN":
            return self.wN_table[square]
        elif piece == "bN":
            return self.bN_table[square]
        elif piece == "wB":
            return self.wB_table[square]
        elif piece == "bB":
            return self.bB_table[square]
        elif piece == "wR":
            return self.wR_table[square]
        elif piece == "bR":
            return self.bR_table[square]
        elif piece == "wK":
            return self.wK_table[square]
        elif piece == "bK":
            return self.bK_table[square]
        return 0
        



    ########
    def simpleheuristic(self, gs):
        heuristicValue = 0
        for piece in gs.board:
            if piece == '--':
                continue
            heuristicValue += self.weights[piece]
        return heuristicValue

    
    def findBestMoveWithTime(self, gs, validMoves, time_limit = 19.5): 
        """
        Parameters
        ----------
        gs : Gamestate
            current state of the game
        validMoves: list
            list of valid moves
        time_limit : time
            time limit the agent has to make a move
        """
        limit = time.time() + time_limit
        #action = self.minimax(gs, validMoves, limit)
        action = self.alpha_beta_search(0, gs, validMoves, limit)
        return action

    ### START: alpha-beta-pruning ###
    def alpha_beta_search(self, depth, gs, validMoves, time_limit):
        best_v = self.a_b_max_value(gs, float('-inf'), float('inf'), time_limit)
        for move in validMoves:
            if best_v == self.evaluate(move):
                action = move
                break
        return action
    
    def a_b_max_value(self, gs, alpha, beta, time_limit):
        # if terminal_test(gs):
        #   return self.evaluate(self.board)
        # terminal-test can either be check-mate or depth (see depth-limited-search) or time
        v = float('-inf')
        validMoves = gs.getValidMoves()
        for move in validMoves:
            if time.time() < time_limit:
                gs.makeMove(move)
                v = max(v, self.a_b_min_value(gs, alpha, beta, time_limit))
                gs.undoMove()
                if v >= beta:
                    return v
                alpha = max(alpha, v)
            else:
                v = self.evaluate(move)
        return v

    def a_b_min_value(self, gs, alpha, beta, time_limit):
        # if terminal_test(gs):
        #   return self.evaluate(self.board)
        # terminal-test can either be check-mate or depth (see depth-limited-search) or time
        v = float('inf')
        validMoves = gs.getValidMoves()
        for move in validMoves:
            if time.time() < time_limit:
                gs.makeMove(move)
                v = min(v, self.a_b_max_value(gs, alpha, beta, time_limit))
                gs.undoMove()
                if v <= alpha:
                    return v
                beta = min(beta, v)
            else:
                v = self.evaluate(move)
        return v
    
    ### END: alpha-beta-pruning ###

    def minimax(self, gs, validMoves, time_limit):
        """
        Parameters
        ----------
        gs : Gamestate
            current state of the game
        """
        #action = max(self.min_value(gs, time_limit))
        best_v = self.min_value(gs, time_limit)
        #action = validMoves[0]
        for move in validMoves:
            if best_v == self.evaluate(move):
                action = move
                break
        return action

        
    def max_value(self, gs, time_limit):
        # if terminal_test(gs):
        #   return self.evaluate(self.board)
        # terminal-test can either be check-mate or depth (see depth-limited-search) or time
        v = float('-inf')
        validMoves = gs.getValidMoves()
        for move in validMoves:
            if time.time() < time_limit:
                v = max(v, self.min_value(self.update_move(move, -1, -1).board, time_limit))
            else: 
                v = self.evaluate(move)
        return v

    def min_value(self, gs, time_limit):
        # if terminal_test(gs):
        #   return self.evaluate(self.board)
        # terminal-test can either be check-mate or depth (see depth-limited-search) or time
        v = float('inf')
        validMoves = gs.getValidMoves()
        for move in validMoves:
            if time.time() < time_limit:
                v = min(v, self.max_value(self.update_move(move, -1, -1).board, time_limit))
            else:
                v = self.evaluate(move)
        return v
    
    # def evaluate(self, gs):
    #     ### START: counting pawns and change weights accordingly ###
    #     pawn_counter = 0
    #     for square in range(len(gs.board)):
    #         piece = gs.board[square]
    #         if piece != '--':
    #             if piece == "wp" or piece == "bp":
    #                 pawn_counter += 1
    #             if 
    #     if pawn_counter < 2:
    #         stop_counting = True
    #         self.weights["wp"] = 250
    #         self.weights["bp"] = -250
    #         self.weights["wR"] = 700
    #         self.weights["bR"] = -700
    #         self.weights["wB"] = 500
    #         self.weights["bB"] = -500
    #     else:
    #         self.weights["wN"] = 500
    #         self.weights["bN"] = -500
        
    #     ### END: counting pawns and change weights accordingly ###

    #     ### START: evaluate piece values ###
    #     utility_value = 0
    #     for square in range(len(gs.board)):
    #         piece = gs.board[square]
    #         if piece == '--':
    #             continue
    #         utility_value += self.weights[piece]
    #     ### END: evaluate piece values ###
    #     return utility_value 
    
        
    

'''

    
            


    

    
    

    









    
            


    

    
    

    






'''
import random


import time


class Agent:
    def __init__(self):
        self.move_queue = None
        self.whiteWeights = {"wp": 110, "wN": 330, "wB": 330, "wR": 550, "wK": 11000,
                        "bp": -100, "bN": -300, "bB": -300, "bR": -500, "bK": -10000}
        self.blackWeights = {"wp": -100, "wN": -300, "wB": -300, "wR": -500, "wK": -10000,
                        "bp": 110, "bN": 330, "bB": 330, "bR": 550, "bK": 11000}
        # same weights for own & opponents pieces
        # self.whiteWeights = {"wp": 100, "wN": 300, "wB": 300, "wR": 500, "wK": 10000,
        #                 "bp": -100, "bN": -300, "bB": -300, "bR": -500, "bK": -10000}
        # self.blackWeights = {"wp": -100, "wN": -300, "wB": -300, "wR": -500, "wK": -10000,
        #                 "bp": 100, "bN": 300, "bB": 300, "bR": 500, "bK": 10000}
        self.weights = None
        self.maxDepth = 4
        self.checkmateDepth = 0
        self.enemyCheckmate = False
        self.enemyInCheck = False
        self.checkmateMove = None
        self.inCheckMove = None
        self.color = None
        self.endGame = False
        self.onlyKingLeft = False

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
        self.wB_table = [-20, -10, -10, -10, -10, -20,
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
                         -20, -10, -10, -10, -10, -20]
        ### Rooks ###
        self.wR_table = [0, 0, 0, 0, 0, 0,
                         5, 10, 10, 10, 10, 5,
                         -5, 5, 5, 5, 5, -5,
                         -5, 0, 0, 0, 0, -5,
                         -5, 0, 0, 0, 0, -5,
                         -5, 0, 10, 10, 0, -5]
        self.bR_table = [-5, 0, 10, 10, 0, -5,
                         -5, 0, 0, 0, 0, -5,
                         -5, 0, 0, 0, 0, -5,
                         -5, 5, 5, 5, 5, -5,
                          5, 10, 10, 10, 10, 5,
                          0, 0, 0, 0, 0, 0,]
        
        self.wR_table_endgame = [10, 10, 10, 10, 10, 10,
                                 10, 5, 5, 5, 5, 10,
                                 10, 5, 0, 0, 5, 10,
                                 10, 5, 0, 0, 5, 10,
                                 10, 5, 5, 5, 5, 10,
                                 10, 10, 10, 10, 10, 10]
                    
        self.bR_table_endgame = self.wR_table_endgame

        
        ### Kings ###
        self.wK_table = [-30, -40, -50, -50, -40, -30,
                         -30, -40, -50, -50, -40, -30,
                         -30, -40, -50, -50, -40, -30,
                         -10, -20, -20, -20, -20, -10,
                          0, 0, -5, -5, 0, 0,
                          20, 30, 10, 0, 10, 30]
        self.bK_table = [20, 30, 10, 0, 10, 30,
                         0, 0, -5, -5, 0, 0,
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
        # TODO
        self.color = gs.whiteToMove
        negInf = float('-inf')
        posInf = float('inf')
        if self.color:
            self.weights = self.whiteWeights
        else:
            self.weights = self.blackWeights
        
        if self.calculate_abolute_piece_board_value(gs) <= 24000:
            self.endGame = True

        if self.endGame:
            self.onlyKingLeft = self.only_king_left(gs)

        move = None

        if self.onlyKingLeft:
            move = self.force_threefold_repetition(gs)
        
        if move:
            self.update_move(move, -1, -1)
        
        else:

            # count pawns and change weights accordingly 
            self.update_weights(gs)

            if self.color:
                king_square = gs.board.index("wK")
            else:
                king_square = gs.board.index("bK")
            self.king_safety(king_square)

            best_v, move = self.alpha_beta_max(0, gs, negInf, posInf)

            if self.enemyInCheck and self.enemyCheckmate:
                self.update_move(self.inCheckMove, -1, -1)
            elif self.enemyCheckmate:
                self.update_move(self.checkmateMove, -1, -1)
            else: 
                self.update_move(move, -1, -1)
            # if self.enemyCheckmate:
            #     self.update_move(self.checkmateMove, -1, -1)
            # else: 
            #     self.update_move(move, -1, -1)
        

    def alpha_beta_max(self, depth, gs, alpha, beta, move = None):
        best = float('-inf')
        best_Move = None
        for move in gs.getValidMoves():
            gs.makeMove(move)
            if depth == self.checkmateDepth: # check if checkmateDepths move (at the moment first move) leads to a checkmate
                gs.getValidMoves()
                if tuple(gs.board) in gs.game_log:
                    if gs.game_log[tuple(gs.board)] + 1 == 3:
                        continue
                if len(gs.getValidMoves()) == 0 and not gs.inCheck:
                    continue
                elif gs.checkMate:
                    v = float('inf')
                    self.enemyCheckmate = True
                    self.checkmateMove = move
                elif gs.inCheck: # if not checkmate, then check if enemy is in check
                    v = float('inf')
                    self.enemyInCheck = True
                    self.inCheckMove = move
            if gs.checkMate and self.enemyInCheck: # if first move leads to an inCheck and second to a checkmate, then do the first move
                v = float('inf')
                self.enemyCheckmate = True
            if depth == self.maxDepth:
                v = self.evaluate(gs)
            else:
                v, v_move = self.alpha_beta_min(depth + 1, gs, alpha, beta, move)
            if v > best:
                best = v
                best_Move = move
            gs.undoMove()
            if v >= beta:
                break
            alpha = max(alpha, best)
        return best, best_Move
    
    # old:
    # def alpha_beta_max(self, depth, gs, alpha, beta, move = None):
    #     if depth == self.maxDepth or len(gs.getValidMoves()) == 0:
    #         if gs.checkMate:
    #             returnValue = float('-inf')
    #         else:
    #             returnValue = self.evaluate(gs)
    #         return returnValue, None
    #     best = float('-inf')
    #     best_Move = None
    #     for move in gs.getValidMoves():
    #         gs.makeMove(move)
    #         v, v_move = self.alpha_beta_min(depth + 1, gs, alpha, beta, move)
    #         if v > best:
    #             best = v
    #             best_Move = move
    #         gs.undoMove()
    #         if v >= beta:
    #             break
    #         alpha = max(alpha, best)
    #     return best, best_Move

    def alpha_beta_min(self, depth, gs, alpha, beta, move = None):
        best = float('inf')
        best_Move = None
        for move in gs.getValidMoves():
            gs.makeMove(move)
            if depth == self.checkmateDepth:
                gs.getValidMoves()
                if gs.checkMate:
                    v = float('-inf')
            if depth == self.maxDepth:
                v = self.evaluate(gs)
            else:
                v, v_move = self.alpha_beta_max(depth + 1, gs, alpha, beta, move)
            if v < best:
                best = v
                best_Move = move
            gs.undoMove()
            if v <= alpha:
                break
            beta = min(beta, best)
        return best, best_Move

    # Old:
    # def alpha_beta_min(self, depth, gs, alpha, beta, move = None):
    #     if depth == self.maxDepth:
    #         return self.evaluate(gs)
    #     if depth == self.checkmateDepth and len(gs.getValidMoves()) == 0: # enemy checkmate bc after agent makes a move there are no validmoves left for the enemy 
    #         returnValue = float('inf')
    #         self.enemyCheckmate = True
    #         self.checkmateMove = move
    #         return returnValue, move
    #     best = float('inf')
    #     best_Move = None
    #     for move in gs.getValidMoves():
    #         gs.makeMove(move)
    #         v, v_move = self.alpha_beta_max(depth + 1, gs, alpha, beta, move)
    #         if v < best:
    #             best = v
    #             best_Move = move
    #         gs.undoMove()
    #         if v <= alpha:
    #             break
    #         beta = min(beta, best)
    #     return best, best_Move


    def evaluate(self, gs): 
        utility_value = 0
        for square in range(len(gs.board)):
            piece = gs.board[square] 
            if piece == '--':
                continue
            mobility_value = 0
            double_pawn = 0
            #if piece == "wp" or piece == "bp" or piece == "wR" or piece == "bR" or piece == "wB" or piece == "bB":
            if piece == "wp" or piece == "bp":
                #mobility_value = self.calculate_mobility_value(gs, square, piece, self.color)
                double_pawn = self.punish_double_pawn(gs, square)
            #utility_value = utility_value + self.weights[piece] + self.find_piece_square_value(square, piece) + 0.25 * mobility_value # evaluate board via piece values and piece-square-table-values
            utility_value = utility_value + self.weights[piece] + 0.5 * self.find_piece_square_value(square, piece) + double_pawn
        
        return utility_value 
    
    def calculate_abolute_piece_board_value(self, gs):
        
        #Function needed to determine whether we have an endgame situation
        
        utility_value = 0
        for square in range(len(gs.board)):
            piece = gs.board[square] 
            if piece == '--':
                continue
            utility_value = utility_value + abs(self.weights[piece])
        return utility_value

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
    
    def calculate_mobility_value(self, gs, square, piece, color):
        mobility_value = 0
        validMoves = gs.getValidMoves()
        if len(validMoves) > 0:
            mobility_value += len(validMoves)
        surrounding_pieces, number_surrounding_pieces = self.get_surrounding_pieces(gs, square)
        if self.color:
            if piece == "wp":
                if surrounding_pieces[1] == "wp": #doubled pawn is punished
                    mobility_value -= 10
            if piece == "wR" or piece == "wB":
                if number_surrounding_pieces > 2:
                    mobility_value -= 5
                elif number_surrounding_pieces > 3:
                    mobility_value -= 10
                elif number_surrounding_pieces > 4:
                    mobility_value -= 15
                # elif number_surrounding_pieces > 5:
                #     mobility_value -= 20
        else:
            if piece == "bp": 
                if surrounding_pieces[7] == "bp": #doubled pawn is punished
                    mobility_value -= 10
            if piece == "bR" or piece == "bB":
                if number_surrounding_pieces > 2:
                    mobility_value -= 5
                elif number_surrounding_pieces > 3:
                    mobility_value -= 10
                elif number_surrounding_pieces > 4:
                    mobility_value -= 15
                # elif number_surrounding_pieces > 5:
                #     mobility_value -= 20
        return mobility_value
    
    def get_surrounding_pieces(self, gs, square):
        
        # 0  1  2  3   4  5 
        # 6  7  8  9  10 11
        # 12 13 14 15 16 17
        # 18 19 20 21 22 23
        # 24 25 26 27 28 29
        # 30 31 32 33 34 35
        
        board = gs.board
        surrounding_pieces = [] 
        surrounding_squares = [square - 7, square - 6, square - 5, 
                               square - 1,   square,   square + 1, 
                               square + 5, square + 6, square + 7]
        number_surrounding_pieces = 0
        for index in surrounding_squares:
            if index >= 0 and index <= 35: #square is on the board
                if index in [0, 6, 12, 18, 24, 30] and square in [5, 11, 17, 23, 29, 35] or index in [5, 11, 17, 23, 29, 35] and square in [0, 6, 12, 18, 24, 30]: # edge-piece 
                    surrounding_pieces.append(-1)
                elif board[index] != "--":  
                    number_surrounding_pieces += 1
                    surrounding_pieces.append(board[index])
                else: 
                    surrounding_pieces.append(0)
            else: 
                surrounding_pieces.append(-1)
        return surrounding_pieces, number_surrounding_pieces

    def update_weights(self, gs):
        # make pawns more valuable in endgame situations:
        if self.endGame:
            if self.color:
                self.weights["wp"] = 275
                self.weights["bp"] = -250
            else: 
                self.weights["wp"] = -250
                self.weights["bp"] = 275
        # change weights of certain pieces considering the number of pawns left on the board
        pawn_counter = 0
        for square in range(len(gs.board)):
            piece = gs.board[square]
            if piece == '--':
                continue
            if piece == "wp" or piece == "bp":
                    pawn_counter += 1
        if pawn_counter < 4:    # if there are few pawns left, pawns, rooks and bishops are more useful (-> more valuable) 
            if self.color:
                self.weights["wp"] = 275
                self.weights["bp"] = -250
                self.weights["wR"] = 770
                self.weights["bR"] = -700
                self.weights["wB"] = 550
                self.weights["bB"] = -500
                ## same weights for own and opponents pieces:
                # self.weights["wp"] = 250
                # self.weights["bp"] = -250
                # self.weights["wR"] = 700
                # self.weights["bR"] = -700
                # self.weights["wB"] = 500
                # self.weights["bB"] = -500
            else:
                self.weights["wp"] = -250
                self.weights["bp"] = 275
                self.weights["wR"] = -700
                self.weights["bR"] = 770
                self.weights["wB"] = -500
                self.weights["bB"] = 550
                ## same weights for own and opponents pieces:
                # self.weights["wp"] = -250
                # self.weights["bp"] = 250
                # self.weights["wR"] = -700
                # self.weights["bR"] = 700
                # self.weights["wB"] = -500
                # self.weights["bB"] = 500

        else:                   # if there are many pawns left, knights are more useful (-> more valuable)
            if self.color:
                self.weights["wN"] = 550
                self.weights["bN"] = -500
                ## same weights for own and opponents pieces:
                # self.weights["wN"] = 500
                # self.weights["bN"] = -500
            else:
                self.weights["wN"] = -500
                self.weights["bN"] = 550
                ## same weights for own and opponents pieces:
                # self.weights["wN"] = -500
                # self.weights["bN"] = 500
        
    
    def find_piece_square_value(self, square, piece):
        if self.color: # we only want the piece-square-values of our own pieces
            if piece == "wp":
                return self.wp_table[square]
            elif piece == "wN":
                return self.wN_table[square]
            elif piece == "wB":
                return self.wB_table[square]
            elif piece == "wR":
                if self.endGame:
                    return self.wR_table_endgame[square]
                else:
                    return self.wR_table[square]
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
            elif piece == "bR":
                if self.endGame:
                    return -0.5 * self.bR_table_endgame[square]
                else:
                    return -0.5 * self.bR_table[square]
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
            elif piece == "bR":
                if self.endGame:
                    return self.bR_table_endgame[square]
                else:
                    return self.bR_table[square]
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
            elif piece == "wR":
                if self.endGame:
                    return -0.5 * self.wR_table_endgame[square]
                else:
                    return -0.5 * self.wR_table[square]
            elif piece == "wK":
                if self.endGame:
                    return self.wK_table_endgame[square]
                else:
                    return -0.5 * self.wK_table[square]
        return 0
    
    def king_safety(self, king_sqaure):
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
        
    def only_king_left(self, gs):
        if self.color:
            for square in range(len(gs.board)):
                piece = gs.board[square]
                if piece in ["wp", "wB", "wN", "wR"]:
                    return False
        elif not self.color: 
            for square in range(len(gs.board)):
                piece = gs.board[square]
                if piece in ["bp", "bB", "bN", "bR"]:
                    return False
        return True

    def force_threefold_repetition(self, gs):
        for move in gs.getValidMoves():
            gs.makeMove(move)
            if tuple(gs.board) in gs.game_log:
                    if gs.game_log[tuple(gs.board)] + 1 == 3:
                        gs.undoMove()
                        return move
            gs.undoMove()
        return None





                





    def update_pawn_table(self, move):
        if move == "O-O":
            if self.color: # agent plays white
                self.wp_table = [100, 100, 100, 100, 100, 100,
                                 50, 50, 50, 50, 50, 50,
                                 10, 25, 30, 30, 25, 10,
                                 5, 15, 20, 20, 15, 5,
                                 5, 10, -25, 30, 30, 30,
                                 0, 0, 0, 0, 0, 0]
            else:   # agent plays black
                self.bp_table = [0, 0, 0, 0, 0, 0, 
                                 5, 10, -25, 30, 30, 30,
                                 5, 15, 20, 20, 15, 5,
                                 10, 25, 30, 30, 25, 10,
                                 50, 50, 50, 50, 50, 50,
                                 100, 100, 100, 100, 100, 100]
        else:
            if self.color: 
                self.wp_table = [100, 100, 100, 100, 100, 100,
                                 50, 50, 50, 50, 50, 50,
                                 10, 25, 30, 30, 25, 10,
                                 5, 15, 20, 20, 15, 5,
                                 30, 30, 30, -25, 10, 5,
                                 0, 0, 0, 0, 0, 0]
            else:
                self.bp_table = [0, 0, 0, 0, 0, 0, 
                                 30, 30, 30, -25, 10, 5,
                                 5, 15, 20, 20, 15, 5,
                                 10, 25, 30, 30, 25, 10,
                                 50, 50, 50, 50, 50, 50,
                                 100, 100, 100, 100, 100, 100]
                                







'''
import time

class Fuck:

    ########
    def simpleheuristic(self, gs):
        heuristicValue = 0
        for piece in gs.board:
            if piece == '--':
                continue
            heuristicValue += self.weights[piece]
        return heuristicValue

    
    def findBestMoveWithTime(self, gs, validMoves, time_limit = 19.5): 
        """
        Parameters
        ----------
        gs : Gamestate
            current state of the game
        validMoves: list
            list of valid moves
        time_limit : time
            time limit the agent has to make a move
        """
        limit = time.time() + time_limit
        #action = self.minimax(gs, validMoves, limit)
        action = self.alpha_beta_search(0, gs, validMoves, limit)
        return action

    ### START: alpha-beta-pruning ###
    def alpha_beta_search(self, depth, gs, validMoves, time_limit):
        best_v = self.a_b_max_value(gs, float('-inf'), float('inf'), time_limit)
        for move in validMoves:
            if best_v == self.evaluate(move):
                action = move
                break
        return action
    
    def a_b_max_value(self, gs, alpha, beta, time_limit):
        # if terminal_test(gs):
        #   return self.evaluate(self.board)
        # terminal-test can either be check-mate or depth (see depth-limited-search) or time
        v = float('-inf')
        validMoves = gs.getValidMoves()
        for move in validMoves:
            if time.time() < time_limit:
                gs.makeMove(move)
                v = max(v, self.a_b_min_value(gs, alpha, beta, time_limit))
                gs.undoMove()
                if v >= beta:
                    return v
                alpha = max(alpha, v)
            else:
                v = self.evaluate(move)
        return v

    def a_b_min_value(self, gs, alpha, beta, time_limit):
        # if terminal_test(gs):
        #   return self.evaluate(self.board)
        # terminal-test can either be check-mate or depth (see depth-limited-search) or time
        v = float('inf')
        validMoves = gs.getValidMoves()
        for move in validMoves:
            if time.time() < time_limit:
                gs.makeMove(move)
                v = min(v, self.a_b_max_value(gs, alpha, beta, time_limit))
                gs.undoMove()
                if v <= alpha:
                    return v
                beta = min(beta, v)
            else:
                v = self.evaluate(move)
        return v
    
    ### END: alpha-beta-pruning ###

    def minimax(self, gs, validMoves, time_limit):
        """
        Parameters
        ----------
        gs : Gamestate
            current state of the game
        """
        #action = max(self.min_value(gs, time_limit))
        best_v = self.min_value(gs, time_limit)
        #action = validMoves[0]
        for move in validMoves:
            if best_v == self.evaluate(move):
                action = move
                break
        return action

        
    def max_value(self, gs, time_limit):
        # if terminal_test(gs):
        #   return self.evaluate(self.board)
        # terminal-test can either be check-mate or depth (see depth-limited-search) or time
        v = float('-inf')
        validMoves = gs.getValidMoves()
        for move in validMoves:
            if time.time() < time_limit:
                v = max(v, self.min_value(self.update_move(move, -1, -1).board, time_limit))
            else: 
                v = self.evaluate(move)
        return v

    def min_value(self, gs, time_limit):
        # if terminal_test(gs):
        #   return self.evaluate(self.board)
        # terminal-test can either be check-mate or depth (see depth-limited-search) or time
        v = float('inf')
        validMoves = gs.getValidMoves()
        for move in validMoves:
            if time.time() < time_limit:
                v = min(v, self.max_value(self.update_move(move, -1, -1).board, time_limit))
            else:
                v = self.evaluate(move)
        return v
    '''
    def evaluate(self, gs):
        ### START: counting pawns and change weights accordingly ###
        pawn_counter = 0
        for square in range(len(gs.board)):
            piece = gs.board[square]
            if piece != '--':
                if piece == "wp" or piece == "bp":
                    pawn_counter += 1
                if 
        if pawn_counter < 2:
            stop_counting = True
            self.weights["wp"] = 250
            self.weights["bp"] = -250
            self.weights["wR"] = 700
            self.weights["bR"] = -700
            self.weights["wB"] = 500
            self.weights["bB"] = -500
        else:
            self.weights["wN"] = 500
            self.weights["bN"] = -500
        
        ### END: counting pawns and change weights accordingly ###

        ### START: evaluate piece values ###
        utility_value = 0
        for square in range(len(gs.board)):
            piece = gs.board[square]
            if piece == '--':
                continue
            utility_value += self.weights[piece]
        ### END: evaluate piece values ###
        return utility_value 
    '''

'''

import random

### MY IMPORTS ###
import time


class Agent:
    def __init__(self):
        self.move_queue = None
        self.WhiteWeights = {"wp": 100, "wN": 300, "wB": 300, "wR": 500, "wK": 10000,
                        "bp": -100, "bN": -300, "bB": -300, "bR": -500, "bK": -10000}
        self.BlackWeights = {"wp": -100, "wN": -300, "wB": -300, "wR": -500, "wK": -10000,
                        "bp": 100, "bN": 300, "bB": 300, "bR": 500, "bK": 10000}
        self.weights = None
        # self.weights = {"wp": 100, "wN" : 300, "wB": 300, "wR" : 500, "wK" : 10000,
        #            "bp": -100, "bN" : -300, "bB": -300, "bR" : -500, "bK" : -10000}
        self.maxDepth = 4 

        self.wp_table = [100, 100, 100, 100, 100, 100,
                         50, 50, 50, 50, 50, 50,
                         10, 25, 30, 30, 25, 10,
                         5, 15, 20, 20, 15, 5,
                         5, 10, -25, -25, 10, 5,
                         0, 0, 0, 0, 0, 0]
        self.bp_table = [0, 0, 0, 0, 0, 0, 
                         -5, -10, 25, 25, -10, -5,
                         -5, -15, -20, -20, -15, -5,
                         -10, -25, -30, -30, -25, -10,
                         -50, -50, -50, -50, -50, -50,
                         -100, -100, -100, -100, -100, -100]
        self.wN_table = [-50, -30, -30, -30, -40, -50,
                         -40, 10, 15, 15, 10, -40,
                         -30, 10, 20, 20, 10, -30,
                         -30, 10, 20, 20, 10, -30,
                         -40, 10, 15, 15, 10, -40,
                         -50, -40, -30, -30, -40, -50]
        self.bN_table = [-x for x in self.wN_table]
        self.wB_table = [-20, -10, -10, -10, -10, -20,
                         -10, 0, 0, 0, 0, -10,
                         -10, 5, 10, 10, 5, -10,
                         -10, 10, 10, 10, 10, -10,
                         -10, 5, 0, 0, 5, -10,
                         -20, -40, -10, -10, -40, -20]
        self.bB_table = [20, 40, 10, 10, 40, 20,
                         10, -5, 0, 0, -5, 10,
                         10, -10, -10, -10, -10, 10,
                         10, -5, -10, -10, -5, 10,
                         10, 0, 0, 0, 0, 10,
                         20, 10, 10, 10, 10, 20]

        self.wR_table = [0, 0, 0, 0, 0, 0,
                         5, 10, 10, 10, 10, 5,
                         -5, 5, 5, 5, 5, -5,
                         -5, 0, 0, 0, 0, -5,
                         -5, 0, 0, 0, 0, -5,
                         -5, 0, 5, 5, 0, -5]
        self.bR_table = [5, 0, -5, -5, 0, 5,
                         5, 0, 0, 0, 0, 5,
                         5, 0, 0, 0, 0, 5,
                         5, -5, -5, -5, -5, 5,
                         -5, -10, -10, -10, -10, -5,
                          0, 0, 0, 0, 0, 0,]

        self.wK_table = [-30, -40, -50, -50, -40, -30,
                         -30, -40, -50, -50, -40, -30,
                         -30, -40, -50, -50, -40, -30,
                         -10, -20, -20, -20, -20, -10,
                         20, 20, 0, 0, 20, 20,
                         20, 30, 10, 0, 10, 30]
        self.bK_table = [-20, -30, -10, 0, -10, -30,
                         -20, -20, 0, 0, -20, -20,
                         10, 20, 20, 20, 20, 10,
                         30, 40, 50, 50, 40, 30,
                         30, 40, 50, 50, 40, 30,
                         30, 40, 50, 50, 40, 30]

        self.wK_table_endgame = [-50, -40, -30, -30, -40, -50,
                                 -30, -20, 0, 0, -20, -30,
                                 -30, 0, 30, 30, 0, -30,
                                 -30, 0, 30, 30, 0, -30,
                                 -30, -20, 0, 0, -20, -30,
                                 -50, -40, -30, -30, -40, -50]
        self.bK_table_endgame = [-x for x in self.wK_table_endgame]


        

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
        # TODO
        validMoves = gs.getValidMoves()
        self.color = gs.whiteToMove
        # if self.color:
        #     self.weights = self.WhiteWeights
        # else:
        #     self.weights = self.BlackWeights
        # best_v, move = self.alpha_beta_max(0, gs, float('-inf'), float('inf'))
        #"""
        if self.color:
            best_v, move = self.alpha_beta_max(0, gs, float('-inf'), float('inf'))
        else:
            best_v, move = self.alpha_beta_min(0, gs, float('-inf'), float('inf'))
        #"""
        #move = self.findBestMoveWithTime(gs, validMoves)
        #print(f"v of the FINALLY CHOSEN move {move}: {best_v}")
        # if move == "O-O" or move == "O-O-O":
            # make pawns in front of king more valuable
        self.update_move(move, -1, -1)
    


    ### BETTER: two in one ###
    def alpha_beta_max(self, depth, gs, alpha, beta):
        if depth == self.maxDepth:
            #return self.simpleheuristic(gs), None
            return self.evaluate(gs), None
        best = float('-inf')
        best_Move = None
        validMoves = gs.getValidMoves()
        if len(validMoves) == 0:
            return self.evaluate(gs), None
        for move in gs.getValidMoves():
            gs.makeMove(move)
            # check for check_mate of opponent. if yes: return that move!
            v, v_move = self.alpha_beta_min(depth + 1, gs, alpha, beta)
            if v > best:
                best = v
                best_Move = move
            #print(f"v of the move {move} in a_b_max:  {v}")
            gs.undoMove()
            #print("--- new move ---")
            if v >= beta:
                break
            alpha = max(alpha, best)
        return best, best_Move

    def alpha_beta_min(self, depth, gs, alpha, beta):
        if depth == self.maxDepth:
            #return self.simpleheuristic(gs), None
            return self.evaluate(gs), None
        best = float('inf')
        best_Move = None
        validMoves = gs.getValidMoves()
        if len(validMoves) == 0:
            return self.evaluate(gs), None
        for move in gs.getValidMoves():
            gs.makeMove(move)
            # check for check_mate of opponent. if yes: return that move!
            v, v_move = self.alpha_beta_max(depth + 1, gs, alpha, beta)
            if v < best:
                best = v
                best_Move = move
            #print(f"v of the move {move} in a_b_min:  {v}")
            gs.undoMove()
            #print("--- new move ---")
            if v <= alpha:
                break
            beta = min(beta, best)
        return best, best_Move


    def evaluate(self, gs):

        ### START: counting pawns and change weights accordingly ###
        pawn_counter = 0
        for square in range(len(gs.board)):
            piece = gs.board[square]
            if piece != '--':
                if piece == "wp" or piece == "bp":
                    pawn_counter += 1
        if pawn_counter < 2:    # bei wenigen Bauern sind Bauern wertvoller & Türme und Läufer auch. 
            stop_counting = True
            self.weights["wp"] = 250
            self.weights["bp"] = -250
            self.weights["wR"] = 700
            self.weights["bR"] = -700
            self.weights["wB"] = 500
            self.weights["bB"] = -500
        else:                   # bei vielen Bauern sind Springer wertvoller
            self.weights["wN"] = 500
            self.weights["bN"] = -500
        ### END: counting pawns and change weights accordingly ###

        ### START: evaluate piece values ###
        utility_value = 0
        for square in range(len(gs.board)):
            piece = gs.board[square] 
            if piece == '--':
                continue
            piece_square_value = self.find_piece_square_value(square, piece)
            utility_value = utility_value + self.weights[piece] + piece_square_value
        ### END: evaluate piece values ###
        return utility_value 

    def find_piece_square_value(self, square, piece):
        if piece == "wp":
            return self.wp_table[square]
        elif piece == "bp":
            return self.bp_table[square]
        elif piece == "wN":
            return self.wN_table[square]
        elif piece == "bN":
            return self.bN_table[square]
        elif piece == "wB":
            return self.wB_table[square]
        elif piece == "bB":
            return self.bB_table[square]
        elif piece == "wR":
            return self.wR_table[square]
        elif piece == "bR":
            return self.bR_table[square]
        elif piece == "wK":
            return self.wK_table[square]
        elif piece == "bK":
            return self.bK_table[square]
        return 0
        



    ########
    def simpleheuristic(self, gs):
        heuristicValue = 0
        for piece in gs.board:
            if piece == '--':
                continue
            heuristicValue += self.weights[piece]
        return heuristicValue

    
    def findBestMoveWithTime(self, gs, validMoves, time_limit = 19.5): 
        """
        Parameters
        ----------
        gs : Gamestate
            current state of the game
        validMoves: list
            list of valid moves
        time_limit : time
            time limit the agent has to make a move
        """
        limit = time.time() + time_limit
        #action = self.minimax(gs, validMoves, limit)
        action = self.alpha_beta_search(0, gs, validMoves, limit)
        return action

    ### START: alpha-beta-pruning ###
    def alpha_beta_search(self, depth, gs, validMoves, time_limit):
        best_v = self.a_b_max_value(gs, float('-inf'), float('inf'), time_limit)
        for move in validMoves:
            if best_v == self.evaluate(move):
                action = move
                break
        return action
    
    def a_b_max_value(self, gs, alpha, beta, time_limit):
        # if terminal_test(gs):
        #   return self.evaluate(self.board)
        # terminal-test can either be check-mate or depth (see depth-limited-search) or time
        v = float('-inf')
        validMoves = gs.getValidMoves()
        for move in validMoves:
            if time.time() < time_limit:
                gs.makeMove(move)
                v = max(v, self.a_b_min_value(gs, alpha, beta, time_limit))
                gs.undoMove()
                if v >= beta:
                    return v
                alpha = max(alpha, v)
            else:
                v = self.evaluate(move)
        return v

    def a_b_min_value(self, gs, alpha, beta, time_limit):
        # if terminal_test(gs):
        #   return self.evaluate(self.board)
        # terminal-test can either be check-mate or depth (see depth-limited-search) or time
        v = float('inf')
        validMoves = gs.getValidMoves()
        for move in validMoves:
            if time.time() < time_limit:
                gs.makeMove(move)
                v = min(v, self.a_b_max_value(gs, alpha, beta, time_limit))
                gs.undoMove()
                if v <= alpha:
                    return v
                beta = min(beta, v)
            else:
                v = self.evaluate(move)
        return v
    
    ### END: alpha-beta-pruning ###

    def minimax(self, gs, validMoves, time_limit):
        """
        Parameters
        ----------
        gs : Gamestate
            current state of the game
        """
        #action = max(self.min_value(gs, time_limit))
        best_v = self.min_value(gs, time_limit)
        #action = validMoves[0]
        for move in validMoves:
            if best_v == self.evaluate(move):
                action = move
                break
        return action

        
    def max_value(self, gs, time_limit):
        # if terminal_test(gs):
        #   return self.evaluate(self.board)
        # terminal-test can either be check-mate or depth (see depth-limited-search) or time
        v = float('-inf')
        validMoves = gs.getValidMoves()
        for move in validMoves:
            if time.time() < time_limit:
                v = max(v, self.min_value(self.update_move(move, -1, -1).board, time_limit))
            else: 
                v = self.evaluate(move)
        return v

    def min_value(self, gs, time_limit):
        # if terminal_test(gs):
        #   return self.evaluate(self.board)
        # terminal-test can either be check-mate or depth (see depth-limited-search) or time
        v = float('inf')
        validMoves = gs.getValidMoves()
        for move in validMoves:
            if time.time() < time_limit:
                v = min(v, self.max_value(self.update_move(move, -1, -1).board, time_limit))
            else:
                v = self.evaluate(move)
        return v
    
    # def evaluate(self, gs):
    #     ### START: counting pawns and change weights accordingly ###
    #     pawn_counter = 0
    #     for square in range(len(gs.board)):
    #         piece = gs.board[square]
    #         if piece != '--':
    #             if piece == "wp" or piece == "bp":
    #                 pawn_counter += 1
    #             if 
    #     if pawn_counter < 2:
    #         stop_counting = True
    #         self.weights["wp"] = 250
    #         self.weights["bp"] = -250
    #         self.weights["wR"] = 700
    #         self.weights["bR"] = -700
    #         self.weights["wB"] = 500
    #         self.weights["bB"] = -500
    #     else:
    #         self.weights["wN"] = 500
    #         self.weights["bN"] = -500
        
    #     ### END: counting pawns and change weights accordingly ###

    #     ### START: evaluate piece values ###
    #     utility_value = 0
    #     for square in range(len(gs.board)):
    #         piece = gs.board[square]
    #         if piece == '--':
    #             continue
    #         utility_value += self.weights[piece]
    #     ### END: evaluate piece values ###
    #     return utility_value 
    
        
    

'''

    
            


    

    
    

    









    
            


    

    
    

    


