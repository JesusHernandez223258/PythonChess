import random
import numpy as np
next_move = None  # Para evitar marcado de error en PyCharm
counter = None  # Igual


class Player:
    def __init__(self):
        self.piece_values = {"K": 0, "Q": 10, "R": 5, "B": 3, "N": 3, "P": 1}
        self.queen_scores = np.array([
            [1, 1, 1, 3, 1, 1, 1, 1],
            [1, 2, 3, 3, 3, 1, 1, 1],
            [1, 4, 3, 3, 3, 4, 2, 1],
            [1, 2, 3, 3, 3, 2, 2, 1],
            [1, 2, 3, 3, 3, 2, 2, 1],
            [1, 4, 3, 3, 3, 4, 2, 1],
            [1, 1, 2, 3, 3, 1, 1, 1],
            [1, 1, 1, 3, 1, 1, 1, 1]
        ])
        self.rook_scores = np.array([
            [4, 3, 4, 4, 4, 4, 3, 4],
            [4, 4, 4, 4, 4, 4, 4, 4],
            [1, 1, 2, 3, 3, 2, 1, 1],
            [1, 2, 3, 4, 4, 3, 2, 1],
            [1, 2, 3, 4, 4, 3, 2, 1],
            [1, 1, 2, 3, 3, 2, 1, 1],
            [4, 4, 4, 4, 4, 4, 4, 4],
            [4, 3, 4, 4, 4, 4, 3, 4]
        ])
        self.bishop_scores = np.array([
            [4, 3, 2, 1, 1, 2, 3, 4],
            [3, 4, 3, 2, 2, 3, 4, 3],
            [2, 3, 4, 3, 3, 4, 3, 2],
            [1, 2, 3, 4, 4, 3, 2, 1],
            [1, 2, 3, 4, 4, 3, 2, 1],
            [2, 3, 4, 3, 3, 4, 3, 2],
            [3, 4, 3, 2, 2, 3, 4, 3],
            [4, 3, 2, 1, 1, 2, 3, 4]
        ])
        self.knight_scores = np.array([
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 2, 2, 2, 2, 2, 2, 1],
            [1, 2, 3, 3, 3, 3, 2, 1],
            [1, 2, 3, 4, 4, 3, 2, 1],
            [1, 2, 3, 4, 4, 3, 2, 1],
            [1, 2, 3, 3, 3, 3, 2, 1],
            [1, 2, 2, 2, 2, 2, 2, 1],
            [1, 1, 1, 1, 1, 1, 1, 1]
        ])
        self.white_pawn_scores = np.array([
            [10, 10, 10, 10, 10, 10, 10, 10],
            [8, 8, 8, 8, 8, 8, 8, 8],
            [5, 6, 6, 7, 7, 6, 6, 5],
            [2, 3, 3, 6, 6, 3, 3, 2],
            [1, 2, 8, 10, 10, 8, 2, 1],
            [1, 1, 2, 3, 3, 2, 1, 1],
            [1, 1, 1, 0, 0, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ])
        self.black_pawn_scores = np.array([
            [0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 0, 0, 1, 1, 1],
            [1, 1, 2, 3, 3, 2, 1, 1],
            [1, 2, 8, 10, 10, 8, 2, 1],
            [2, 3, 3, 6, 6, 3, 3, 2],
            [5, 6, 6, 7, 7, 6, 6, 5],
            [8, 8, 8, 8, 8, 8, 8, 8],
            [10, 10, 10, 10, 10, 10, 10, 10]
        ])

        self.positions_scores = {"Q": self.queen_scores, "R": self.rook_scores, "B": self.black_pawn_scores,
                                 "N": self.knight_scores, "bP": self.black_pawn_scores, "wP": self.white_pawn_scores}
        self.psm = .2
        self.CHECKMATE = 1000
        self.STALEMATE = 0
        self.MAX_DEPTH = 4

    @staticmethod
    def random_move(valid_moves):
        """
        Devuelve un movimiento aleatorio de los movimientos válidos
        :param valid_moves: lista de movimientos válidos
        :return: movimiento aleatorio
        """
        return valid_moves[random.randint(0, len(valid_moves)-1)]

    def material_score(self, board):
        """
        Calcula el score del tablero según las piezas restantes de cada color. + para blancas, - para negras
        :param board: estado del tablero actual
        :return: score del tablero
        """
        score = 0
        for r in board:
            for sq in r:
                if sq[0] == "w":
                    score += self.piece_values[sq[1]]
                elif sq[0] == "b":
                    score -= self.piece_values[sq[1]]
        return score

    def board_score(self, game_state):
        """
        Calcula el score del tablero según . + para blancas, - para negras
        :param game_state: estado actual del juego
        :return: puntuación del material del tablero
        """
        if game_state.checkmate:
            if game_state.white_turn:
                return -self.CHECKMATE  # black wins
            else:
                return self.CHECKMATE  # white wins
        elif game_state.stalemate:
            return self.STALEMATE

        score = 0
        for r in range(len(game_state.board)):
            for c in range(len(game_state.board[r])):
                sq = game_state.board[r][c]
                if sq != "--":
                    position_score = 0
                    if sq[1] != "K":
                        if sq[1] == "P":
                            position_score = self.positions_scores[sq][r][c]
                        else:
                            position_score = self.positions_scores[sq[1]][r][c]
                    if sq[0] == "w":
                        score += self.piece_values[sq[1]] + position_score * self.psm
                    elif sq[0] == "b":
                        score -= self.piece_values[sq[1]] + position_score * self.psm
        return score

    def greedy_move(self, games_state, valid_moves):
        """
        Algoritmo minmax (sin recursión) para generar un movimiento válido teniendo en cuenta el "material" y los prox dos movimientos
        Material: Score resultado de la suma y resta de piezas, posiciones, etc. en el tablero
        :param games_state: estado del juego actual
        :param valid_moves: lista de movimientos válidos
        :return: "mejor" movimiento calculado
        """
        turn_multiplier = 1 if games_state.white_turn else -1
        opp_minmax_score = self.CHECKMATE
        best_player_move = None
        for player_move in valid_moves:
            games_state.make_move(player_move)
            opp_moves = games_state.get_valid_moves()
            if games_state.checkmate:
                opp_max_score = -self.CHECKMATE
            elif games_state.stalemate:
                opp_max_score = self.STALEMATE
            else:
                opp_max_score = -self.CHECKMATE
                for opp_move in opp_moves:
                    games_state.make_move(opp_move)
                    games_state.get_valid_moves()
                    if games_state.checkmate:
                        score = self.CHECKMATE
                    elif games_state.stalemate:
                        score = self.STALEMATE
                    else:
                        score = -turn_multiplier * self.material_score(games_state.board)
                    if score > opp_max_score:  # Maximiza el score del oponente
                        opp_max_score = score
                    games_state.undo_move()
            if opp_max_score < opp_minmax_score:  # Minimiza el máximo score del oponente
                opp_minmax_score = opp_max_score
                best_player_move = player_move
            games_state.undo_move()
        return best_player_move

    def best_move(self, game_state, valid_moves, return_queue):
        """
        Método para generar la primera llamada de recursión. Generar el movimiento
        :param return_queue:
        :param game_state: estado actual del juego
        :param valid_moves: lista de movimientos válidos
        :return: siguiente movimiento
        """
        global next_move, counter
        next_move = None
        counter = 0
        random.shuffle(valid_moves)
        # self.greedy_move(game_state, valid_moves)
        # self.minmax_move(game_state, valid_moves, self.MAX_DEPTH, game_state.white_turn)
        # self.negamax_move(game_state, valid_moves, self.MAX_DEPTH, 1 if game_state.white_turn else -1)
        self.alpha_beta_negamax_move(game_state, valid_moves, self.MAX_DEPTH, -self.CHECKMATE, self.CHECKMATE, 1 if game_state.white_turn else -1)
        print(f"{counter} movimientos evaluados")
        return_queue.put(next_move)

    def minmax_move(self, game_state, valid_moves, depth, white_turn):
        """
        Algoritmo MinMax recursivo para calcular en mejor movimiento posible
        :param game_state: estado actual del juego
        :param valid_moves: lista de movimientos válidos
        :param depth: profundidad del algoritmo. Cuantos movimientos próximos calcula
        :param white_turn: True turno del blanco, False turno del negro
        :return: "mejor" movimiento calculado
        """
        global next_move
        if depth == 0:
            return self.material_score(game_state.board)

        if white_turn:  # maximizar
            max_score = -self.CHECKMATE
            for move in valid_moves:
                game_state.make_move(move)
                next_moves = game_state.get_valid_moves()
                score = self.minmax_move(game_state, next_moves, depth-1, not white_turn)
                if score > max_score:
                    max_score = score
                    if depth == self.MAX_DEPTH:
                        next_move = move
                game_state.undo_move()
            return max_score

        else:  # minimizar
            min_score = self.CHECKMATE
            for move in valid_moves:
                game_state.make_move(move)
                next_moves = game_state.get_valid_moves()
                score = self.minmax_move(game_state, next_moves, depth-1, not white_turn)
                if score < min_score:
                    min_score = score
                    if depth == self.MAX_DEPTH:
                        next_move = move
                game_state.undo_move()
            return min_score

    def negamax_move(self, game_state, valid_moves, depth, turn_multiplier):
        """
        Algoritmo NegaMax. Hace lo mismo que MinMax solo que es más corto y sencillo
        :param game_state: estado actual del juego
        :param valid_moves: lista de movimientos válidos
        :param depth: profundidad del algoritmo. Cuantos movimientos próximos calcula
        :param turn_multiplier: 1: turno blanco, -1 turno negro
        :return:
        """
        global next_move, counter
        counter += 1
        if depth == 0:
            return turn_multiplier * self.board_score(game_state)

        max_score = -self.CHECKMATE
        for move in valid_moves:
            game_state.make_move(move)
            next_moves = game_state.get_valid_moves()
            score = -self.negamax_move(game_state, next_moves, depth-1, -turn_multiplier)
            if score > max_score:
                max_score = score
                if depth == self.MAX_DEPTH:
                    next_move = move
            game_state.undo_move()
        return max_score

    def alpha_beta_negamax_move(self, game_state, valid_moves, depth, alpha, beta, turn_multiplier):
        """
        Algoritmo NegaMax con poda alpha-beta.
        :param game_state: estado actual del juego
        :param valid_moves: lista de movimientos válidos
        :param depth: profundidad del algoritmo. Cuantos movimientos próximos calcula
        :param alpha: puntuación maxima
        :param beta: puntuación minima
        :param turn_multiplier: 1: turno blanco, -1 turno negro
        :return:
        """
        global next_move, counter
        counter += 1
        if depth == 0:
            return turn_multiplier * self.board_score(game_state)

        max_score = -self.CHECKMATE
        for move in valid_moves:
            game_state.make_move(move)
            next_moves = game_state.get_valid_moves()
            score = -self.alpha_beta_negamax_move(game_state, next_moves, depth-1, -beta, -alpha, -turn_multiplier)
            if score > max_score:
                max_score = score
                if depth == self.MAX_DEPTH:
                    next_move = move
            game_state.undo_move()
            if max_score > alpha:
                alpha = max_score
            if alpha >= beta:
                break
        return max_score
