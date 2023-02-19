import numpy as np


class GameState:
    def __init__(self):
        """
        Estado actual del juego
        """
        self.board = np.array([
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ])
        self.move_functions = {"P": self.pawn_moves, "R": self.rook_moves, "N": self.knight_moves,
                               "B": self.bishop_moves, "Q": self.queen_moves, "K": self.king_moves}
        self.white_turn = True
        self.move_log = []
        self.white_king_pos = (7, 4)
        self.black_king_pos = (0, 4)

        self.in_check = False
        self.pins = []
        self.checks = []

        self.checkmate = False
        self.stalemate = False
        self.draw = False
        self.enpassant_possible = ()
        self.enpassant_possible_log = [self.enpassant_possible]
        self.current_castling_rights = CastleRights(True, True, True, True)
        self.castle_right_log = [CastleRights(self.current_castling_rights.white_ks,
                                              self.current_castling_rights.black_ks,
                                              self.current_castling_rights.white_qs,
                                              self.current_castling_rights.black_qs)]

    def make_move(self, move):
        """
        Hacer un movimiento
        :param move: movimiento a realizar
        """
        self.board[move.start_r][move.start_c] = "--"
        self.board[move.end_r][move.end_c] = move.piece_moved
        self.move_log.append(move)
        self.white_turn = not self.white_turn
        #  Actualizar posición del rey
        if move.piece_moved == "wK":
            self.white_king_pos = (move.end_r, move.end_c)
        elif move.piece_moved == "bK":
            self.black_king_pos = (move.end_r, move.end_c)
        # pawn promotion
        if move.pawn_promotion:
            self.board[move.end_r][move.end_c] = move.piece_moved[0] + "Q"
        # en passant
        if move.enpassant_move:
            self.board[move.start_r][move.end_c] = "--"
        # actualizar enpassant_possible
        if move.piece_moved[1] == "P" and abs(move.start_r - move.end_r) == 2:
            self.enpassant_possible = ((move.start_r + move.end_r) // 2, move.end_c)
        else:
            self.enpassant_possible = ()
        self.enpassant_possible_log.append(self.enpassant_possible)
        # castling
        if move.castle_move:
            if move.end_c - move.start_c == 2:  # king side
                self.board[move.end_r][move.end_c - 1] = self.board[move.end_r][move.end_c + 1]
                self.board[move.end_r][move.end_c + 1] = "--"
            else:  # queen side
                self.board[move.end_r][move.end_c + 1] = self.board[move.end_r][move.end_c - 2]
                self.board[move.end_r][move.end_c - 2] = "--"

        # actualizar castle rights
        self.update_castling(move)
        self.castle_right_log.append(CastleRights(self.current_castling_rights.white_ks,
                                                  self.current_castling_rights.black_ks,
                                                  self.current_castling_rights.white_qs,
                                                  self.current_castling_rights.black_qs))

    def undo_move(self):
        """
        Deshacer ultimo movimiento
        """
        if len(self.move_log) != 0:
            move = self.move_log.pop()
            self.board[move.end_r][move.end_c] = move.piece_captured
            self.board[move.start_r][move.start_c] = move.piece_moved
            self.white_turn = not self.white_turn
            #  actualizar posición del rey
            if move.piece_moved == "wK":
                self.white_king_pos = (move.start_r, move.start_c)
            elif move.piece_moved == "bK":
                self.black_king_pos = (move.start_r, move.start_c)
            # deshacer enpassant
            if move.enpassant_move:
                self.board[move.end_r][move.end_c] = "--"
                self.board[move.start_r][move.end_c] = move.piece_captured
                # self.enpassant_possible = (move.end_r, move.end_c)
            self.enpassant_possible_log.pop()
            self.enpassant_possible = self.enpassant_possible_log[-1]

            # deshacer avance de 2 casillas (peón)
            # if move.piece_moved[1] == "P" and abs(move.end_r - move.start_r) == 2:
            #     self.enpassant_possible = ()

            # deshacer castle rights
            self.castle_right_log.pop()
            new_right = self.castle_right_log[-1]
            self.current_castling_rights = CastleRights(new_right.white_ks, new_right.black_ks,
                                                        new_right.white_qs, new_right.black_qs)

            # deshacer castle move
            if move.castle_move:
                if move.end_c - move.start_c == 2:
                    self.board[move.end_r][move.end_c + 1] = self.board[move.end_r][move.end_c - 1]
                    self.board[move.end_r][move.end_c - 1] = "--"
                else:
                    self.board[move.end_r][move.end_c - 2] = self.board[move.end_r][move.end_c + 1]
                    self.board[move.end_r][move.end_c + 1] = "--"

            self.checkmate = False
            self.stalemate = False

    def get_pins_checks(self):
        pins = []
        checks = []
        in_check = False
        if self.white_turn:
            enemy = "b"
            ally = "w"
            start_row, start_col = self.white_king_pos
        else:
            enemy = "w"
            ally = "b"
            start_row, start_col = self.black_king_pos

        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(directions)):
            d = directions[j]
            possible_pin = ()
            for i in range(1, 8):
                end_r = start_row + d[0] * i
                end_c = start_col + d[1] * i
                if 0 <= end_r < 8 and 0 <= end_c < 8:
                    end_piece = self.board[end_r][end_c]
                    if end_piece[0] == ally and end_piece[1] != "K":
                        if possible_pin == ():
                            possible_pin = (end_r, end_c, d[0], d[1])
                        else:
                            break
                    elif end_piece[0] == enemy:
                        piece_type = end_piece[1]
                        if (0 <= j <= 3 and piece_type == "R") or (4 <= j <= 7 and piece_type == "B") \
                                or (i == 1 and piece_type == "P" and (
                                (enemy == "w" and 6 <= j <= 7) or (enemy == "b" and 4 <= j <= 5))) \
                                or (piece_type == "Q") or (i == 1 and piece_type == "K"):
                            if possible_pin == ():
                                in_check = True
                                checks.append((end_r, end_c, d[0], d[1]))
                                break
                            else:
                                pins.append(possible_pin)
                                break
                        else:
                            break
                else:
                    break
        knight_directions = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for m in knight_directions:
            end_r = start_row + m[0]
            end_c = start_col + m[1]
            if 0 <= end_r < 8 and 0 <= end_c < 8:
                end_piece = self.board[end_r][end_c]
                if end_piece[0] == enemy and end_piece[1] == "N":
                    in_check = True
                    checks.append((end_r, end_c, m[0], m[1]))
        return in_check, pins, checks

    def get_valid_moves(self):
        moves = []
        self.in_check, self.pins, self.checks = self.get_pins_checks()
        if self.white_turn:
            king_r = self.white_king_pos[0]
            king_c = self.white_king_pos[1]
        else:
            king_r = self.black_king_pos[0]
            king_c = self.black_king_pos[1]
        if self.in_check:
            if len(self.checks) == 1:
                moves = self.get_possible_moves()
                check = self.checks[0]
                check_r = check[0]
                check_c = check[1]
                piece_checking = self.board[check_r][check_c]
                valid_sqs = []
                if piece_checking[1] == "N":
                    valid_sqs = [(check_r, check_c)]
                else:
                    for i in range(1, 8):
                        valid_sq = (king_r + check[2] * i, king_c + check[3] * i)
                        valid_sqs.append(valid_sq)
                        if valid_sq[0] == check_r and valid_sq[1] == check_c:
                            break
                for i in range(len(moves) - 1, -1, -1):
                    if moves[i].piece_moved[1] != "K":
                        if not (moves[i].end_r, moves[i].end_c) in valid_sqs:
                            moves.remove(moves[i])
            else:
                self.king_moves(king_r, king_c, moves)
        else:
            moves = self.get_possible_moves()
        if len(moves) == 0:
            if self.white_turn:
                if self.square_attacked(self.white_king_pos[0], self.white_king_pos[1]):
                    self.checkmate = True
                else:
                    self.stalemate = True
            else:
                if self.square_attacked(self.black_king_pos[0], self.black_king_pos[1]):
                    self.checkmate = True
                else:
                    self.stalemate = True
        return moves

    def square_attacked(self, r, c):
        """
        Determina si el enemigo puede atacar la casilla r, c
        :param r:
        :param c:
        :return: boolean
        """
        self.white_turn = not self.white_turn
        opp_moves = self.get_possible_moves()
        self.white_turn = not self.white_turn
        for move in opp_moves:
            if move.end_r == r and move.end_c == c:
                return True
        return False

    def get_possible_moves(self):
        """
        Movimientos sin considerar jaques
        """
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn, piece = self.board[r][c][0], self.board[r][c][1]
                if (turn == "w" and self.white_turn) or (turn == "b" and not self.white_turn):
                    self.move_functions[piece](r, c, moves)
        return moves

    def multi_moves(self, r, c, moves, dirs):
        """
        Función para calcular movimientos de la torre y del alfil
        :param r: fila
        :param c: columna
        :param moves: lista de movimientos
        :param dirs: direcciones del movimiento
        :return: lista de movimientos actualizados
        """
        color = "w" if self.white_turn else "b"
        piece_pin = False
        pin_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if (self.pins[i][0] == r) and (self.pins[i][1] == c):
                piece_pin = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                if self.board[r][c][1] != "Q":
                    self.pins.remove(self.pins[i])
                break
        for i in range(len(dirs)):
            for j in range(1, len(self.board)):
                end_r = r + dirs[i][0] * j
                end_c = c + dirs[i][1] * j
                if 0 <= end_r <= 7 and 0 <= end_c <= 7:
                    if not piece_pin or pin_direction == dirs[i] or pin_direction == (-dirs[i][0], -dirs[i][1]):
                        if self.board[end_r][end_c] == "--":
                            moves.append(Move((r, c), (end_r, end_c), self.board))  # casilla vacía
                        elif self.board[end_r][end_c][0] != color:
                            moves.append(Move((r, c), (end_r, end_c), self.board))  # pieza enemigo
                            break
                        else:
                            break  # pieza amiga
                else:
                    break  # fuera de los límites

    def pawn_moves(self, r, c, moves):
        """
        Obtener movimientos del peon r, c
        :param r: fila
        :param c: columna
        :param moves: lista de movimientos
        :return: lista de movimientos del peón actualizados
        """
        piece_pin = False
        pin_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if (self.pins[i][0] == r) and (self.pins[i][1] == c):
                piece_pin = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        if self.white_turn:
            amount = -1
            enemy = "b"
            start_r = 6
            king_r, king_c = self.white_king_pos
        else:
            amount = 1
            enemy = "w"
            start_r = 1
            king_r, king_c = self.black_king_pos

        if self.board[r + amount][c] == "--":
            if not piece_pin or pin_direction == (amount, 0):
                moves.append(Move((r, c), (r + amount, c), self.board))
                if r == start_r and (self.board[r + amount * 2][c] == "--"):
                    moves.append(Move((r, c), (r + amount * 2, c), self.board))
        if c != 0:
            if not piece_pin or pin_direction == (amount, -1):
                if self.board[r + amount][c - 1][0] == enemy:
                    moves.append(Move((r, c), (r + amount, c - 1), self.board))  # captura a la izquierda
                if (r + amount, c - 1) == self.enpassant_possible:
                    attacking_piece = blocking_piece = False
                    if king_r == r:
                        if king_c < c:  # rey a la izquierda del peón
                            inside_range = range(king_c + 1, c - 1)
                            outside_range = range(c + 1, 8)
                        else:  # rey a la derecha del peón
                            inside_range = range(king_c - 1, c, -1)
                            outside_range = range(c - 2, -1, -1)
                        for i in inside_range:
                            if self.board[r][i] != "--":  # pieza al lado del movimiento en-passant
                                blocking_piece = True
                        for i in outside_range:
                            sq = self.board[r][i]
                            if sq[0] == enemy and (sq[1] == "R" or sq[1] == "Q"):
                                attacking_piece = True
                            elif sq != "--":
                                blocking_piece = True
                    if not attacking_piece or blocking_piece:
                        moves.append(
                            Move((r, c), (r + amount, c - 1), self.board, enpassant=True))  # captura al paso izquierda
        if c != 7:
            if not piece_pin or pin_direction == (amount, 1):
                if self.board[r + amount][c + 1][0] == enemy:
                    moves.append(Move((r, c), (r + amount, c + 1), self.board))  # captura a la derecha
                if (r + amount, c + 1) == self.enpassant_possible:
                    attacking_piece = blocking_piece = False
                    if king_r == r:
                        if king_c < c:  # rey a la izquierda del peón
                            inside_range = range(king_c + 1, c)
                            outside_range = range(c + 2, 8)
                        else:  # rey a la derecha del peón
                            inside_range = range(king_c - 1, c + 1, -1)
                            outside_range = range(c - 1, -1, -1)
                        for i in inside_range:
                            if self.board[r][i] != "--":  # pieza al lado del movimiento en-passant
                                blocking_piece = True
                        for i in outside_range:
                            sq = self.board[r][i]
                            if sq[0] == enemy and (sq[1] == "R" or sq[1] == "Q"):
                                attacking_piece = True
                            elif sq != "--":
                                blocking_piece = True
                    if not attacking_piece or blocking_piece:
                        moves.append(
                            Move((r, c), (r + amount, c + 1), self.board, enpassant=True))  # captura al paso derecha

    def rook_moves(self, r, c, moves):
        """
        Obtener movimientos de la torre r, c
        :param r: fila
        :param c: columna
        :param moves: lista de movimientos
        :return: lista de movimientos de la torre actualizados
        """
        dirs = ((-1, 0), (0, -1), (1, 0), (0, 1))
        self.multi_moves(r, c, moves, dirs)

    def knight_moves(self, r, c, moves):
        """
        Obtener movimientos del caballero r, c
        :param r: fila
        :param c: columna
        :param moves: lista de movimientos
        :return: lista de movimientos del caballero actualizados
        """
        dirs = ((-2, -1), (-2, 1), (-1, 2), (1, 2), (2, 1), (2, -1), (1, -2), (-1, -2))
        piece_pin = False
        # pin_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if (self.pins[i][0] == r) and (self.pins[i][1] == c):
                piece_pin = True
                # pin_direction = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        color = "w" if self.white_turn else "b"
        for i in range(len(dirs)):
            end_r = r + dirs[i][0]
            end_c = c + dirs[i][1]
            if 0 <= end_r <= 7 and 0 <= end_c <= 7:
                if not piece_pin:
                    if self.board[end_r][end_c][0] != color:
                        moves.append(Move((r, c), (end_r, end_c), self.board))  # Casilla vacía o pieza enemiga

    def bishop_moves(self, r, c, moves):
        """
        Obtener movimientos del alfil r, c
        :param r: fila
        :param c: columna
        :param moves: lista de movimientos
        :return: lista de movimientos del alfil actualizados
        """
        dirs = ((-1, 1), (1, 1), (1, -1), (-1, -1))
        self.multi_moves(r, c, moves, dirs)

    def queen_moves(self, r, c, moves):
        """
        Obtener movimientos de la reina r, c
        :param r: fila
        :param c: columna
        :param moves: lista de movimientos
        :return: lista de movimientos de la reina actualizados
        """
        self.rook_moves(r, c, moves)
        self.bishop_moves(r, c, moves)

    def king_moves(self, r, c, moves):
        """
        Obtener movimientos del rey r, c
        :param r: fila
        :param c: columna
        :param moves: lista de movimientos
        :return: lista de movimientos del rey actualizados
        """
        dirs = ((-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1))
        color = "w" if self.white_turn else "b"
        for i in range(len(dirs)):
            end_r = r + dirs[i][0]
            end_c = c + dirs[i][1]
            if 0 <= end_r <= 7 and 0 <= end_c <= 7:
                if self.board[end_r][end_c][0] != color:
                    if color == "w":
                        self.white_king_pos = (end_r, end_c)
                    else:
                        self.black_king_pos = (end_r, end_c)
                    in_check, pins, checks = self.get_pins_checks()
                    if not in_check:
                        moves.append(Move((r, c), (end_r, end_c), self.board))
                    if color == "w":
                        self.white_king_pos = (r, c)
                    else:
                        self.black_king_pos = (r, c)

    def get_castle_moves(self, r, c, moves):
        """
        Genera todos los movimientos válidos de castling
        :param r: fila
        :param c: columna
        :param moves: lista de movimientos
        :return: lista de movimientos actualizados
        """
        if self.square_attacked(r, c):  # verifica que no esté en jaque
            return
        if (self.white_turn and self.current_castling_rights.white_ks) or \
                (not self.white_turn and self.current_castling_rights.black_ks):
            self.get_ks_moves(r, c, moves)
        if (self.white_turn and self.current_castling_rights.white_qs) or \
                (not self.white_turn and self.current_castling_rights.black_qs):
            self.get_qs_moves(r, c, moves)

    def get_ks_moves(self, r, c, moves):
        """
        Movimientos del lado del rey
        """
        if self.board[r][c + 1] == "--" and self.board[r][c + 2] == "--":  # verifica que las casillas estén vacías
            if not self.square_attacked(r, c + 1) and not self.square_attacked(r, c + 2):  # verifica casillas en jaque
                moves.append(Move((r, c), (r, c + 2), self.board, castle=True))

    def get_qs_moves(self, r, c, moves):
        """
        Movimientos del lado de la reina
        """
        if self.board[r][c - 1] == "--" and self.board[r][c - 2] == "--" and self.board[r][c - 3] == "--":
            if not self.square_attacked(r, c - 1) and not self.square_attacked(r, c - 2):  # verifica casillas en jaque
                moves.append(Move((r, c), (r, c - 2), self.board, castle=True))

    def update_castling(self, move):
        """
        Actualiza los derechos de castling
        :param move: Movimiento a realizar
        :return: Derechos de castling
        """
        if move.piece_moved == "wK":  # Rey blanco
            self.current_castling_rights.white_ks = False
            self.current_castling_rights.white_qs = False
        elif move.piece_moved == "bK":  # Rey negro
            self.current_castling_rights.black_ks = False
            self.current_castling_rights.black_qs = False
        elif move.piece_moved == "wR":  # Torre blanca
            if move.start_r == 7:
                if move.start_c == 0:
                    self.current_castling_rights.white_qs = False
                elif move.start_c == 7:
                    self.current_castling_rights.white_ks = False
        elif move.piece_moved == "bR":  # Torre negra
            if move.start_r == 0:
                if move.start_c == 0:
                    self.current_castling_rights.black_qs = False
                elif move.start_c == 7:
                    self.current_castling_rights.black_ks = False

        if move.piece_captured == "wR":
            if move.end_r == 7:
                if move.end_c == 0:
                    self.current_castling_rights.white_qs = False
                elif move.end_c == 7:
                    self.current_castling_rights.white_ks = False
        if move.piece_captured == "bR":
            if move.end_r == 0:
                if move.end_c == 0:
                    self.current_castling_rights.black_qs = False
                elif move.end_c == 7:
                    self.current_castling_rights.black_ks = False

    # def fifty_move_rule(self):
    #     """
    #     Se encarga de verificar la regla de los 50 movimientos consecutivos sin capturas ni movimientos de peones
    #     """
    #     last_move = self.move_log[-1]
    #     if last_move.piece_captured != "--" or last_move.piece_moved[1] == "P":
    #         self.fifty_rule_moves = 0
    #     else:
    #         self.fifty_rule_moves += 1
    #     if self.fifty_rule_moves == 100:
    #         self.draw = True


class CastleRights:
    """
    Encargada de permitir los movimientos de castling
    """

    def __init__(self, white_ks, black_ks, white_qs, black_qs):
        self.white_ks = white_ks
        self.black_ks = black_ks
        self.white_qs = white_qs
        self.black_qs = black_qs


class Move:
    ranks_rows = {"1": 7, "2": 6, "3": 5, "4": 4,
                  "5": 3, "6": 2, "7": 1, "8": 0}
    rows_ranks = {v: k for k, v in ranks_rows.items()}
    files_cols = {"a": 0, "b": 1, "c": 2, "d": 3,
                  "e": 4, "f": 5, "g": 6, "h": 7}
    cols_files = {v: k for k, v in files_cols.items()}

    def __init__(self, start, end, board, enpassant=False, castle=False):
        """
        Crea un movimiento
        :param start: primer click
        :param end: segundo click
        :param board: estado del tablero actual
        """
        self.start_r = start[0]
        self.start_c = start[1]
        self.end_r = end[0]
        self.end_c = end[1]
        self.piece_moved = board[self.start_r][self.start_c]
        self.piece_captured = board[self.end_r][self.end_c]

        # pawn promotion
        self.pawn_promotion = (self.piece_moved == "wP" and self.end_r == 0) or \
                              (self.piece_moved == "bP" and self.end_r == 7)
        # en passant
        self.enpassant_move = enpassant
        if self.enpassant_move:
            self.piece_captured = "wP" if self.piece_moved == "bP" else "bP"

        # self.capture = self.piece_captured != "-- "
        # castling
        self.castle_move = castle

        self.move_id = self.start_r * 1000 + self.start_c * 100 + self.end_r * 10 + self.end_c

    def get_notation(self):
        """
        :return: Notación del ajedrez del movimiento
        """
        return self.get_rank_file(self.start_r, self.start_c) + \
            self.get_rank_file(self.end_r, self.end_c)

    def get_rank_file(self, r, c):
        """
        :param r: fila
        :param c: columna
        :return: notación de ajedrez de la casilla
        """
        return self.cols_files[c] + self.rows_ranks[r]

    def __eq__(self, other):
        """
        Sobreescribir el método de igualdad
        :param other: objeto a igualar
        :return: boolean
        """
        if isinstance(other, Move):
            return self.move_id == other.move_id
        return False

    def __str__(self):
        """
        Sobreescribir el método de str()
        https://en.wikipedia.org/wiki/Algebraic_notation_(chess)
        """
        # castle move
        if self.castle_move:
            return "O-O" if self.end_c == 6 else "O-O-O"

        end = self.get_rank_file(self.end_r, self.end_c)
        # movimientos de peón
        if self.piece_moved[1] == "P":
            if self.piece_captured != "--":
                return self.cols_files[self.start_c] + "x" + end
            else:
                return end

            # promoción de peón

        # + para check move, # para checkmate

        # movimiento de piezas
        move_string = self.piece_moved[1]
        if self.piece_captured != "--":
            move_string += "x"
        return move_string + end
