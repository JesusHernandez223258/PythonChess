import random


class Player:
    def __init__(self):
        self.piece_values = {"K": 0, "Q": 10, "R": 5, "B": 3, "N": 3, "P": 1}
        self.CHECKMATE = 1000
        self.STALEMATE = 0
        self.MAX_DEPTH = 3

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
        :param game_state:
        :return:
        """
        if game_state.checkmate:
            if game_state.white_turn:
                return -self.CHECKMATE  # black wins
            else:
                return self.CHECKMATE  # white wins
        elif game_state.stalemate:
            return self.STALEMATE

        score = 0
        for r in game_state.board:
            for sq in r:
                if sq[0] == "w":
                    score += self.piece_values[sq[1]]
                elif sq[0] == "b":
                    score -= self.piece_values[sq[1]]
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
        random.shuffle(valid_moves)
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

    def best_minmax_move(self, game_state, valid_moves):
        """
        Método para generar la primera llamada de recursión
        :param game_state:
        :param valid_moves:
        :return:
        """
        global next_move
        next_move = None
        self.minmax_move(game_state, valid_moves, self.MAX_DEPTH, game_state.white_turn)
        return next_move

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











