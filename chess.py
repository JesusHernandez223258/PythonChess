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
        self.check_mate = False
        self.stale_mate = False
        self.enpassant_possible = ()
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
            self.enpassant_possible = ((move.start_r + move.end_r)//2, move.end_c)
        else:
            self.enpassant_possible = ()
        # castling
        if move.castle_move:
            if move.end_c - move.start_c == 2:  # king side
                self.board[move.end_r][move.end_c-1] = self.board[move.end_r][move.end_c+1]
                self.board[move.end_r][move.end_c+1] = "--"
            else:  # queen side
                self.board[move.end_r][move.end_c+1] = self.board[move.end_r][move.end_c-2]
                self.board[move.end_r][move.end_c-2] = "--"

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
            self.board[move.end_r][move.end_c] = move.piece_capture
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
                self.board[move.start_r][move.end_c] = move.piece_capture
                self.enpassant_possible = (move.end_r, move.end_c)
            # deshacer avance de 2 casillas (peón)
            if move.piece_moved[1] == "P" and abs(move.end_r - move.start_r) == 2:
                self.enpassant_possible = ()
            # deshacer castle rights
            self.castle_right_log.pop()
            new_right = self.castle_right_log[-1]
            self.current_castling_rights = CastleRights(new_right.white_ks, new_right.black_ks,
                                                        new_right.white_qs, new_right.black_qs)

            # deshacer castle move
            if move.castle_move:
                if move.end_c - move.start_c == 2:
                    self.board[move.end_r][move.end_c+1] = self.board[move.end_r][move.end_c-1]
                    self.board[move.end_r][move.end_c-1] = "--"
                else:
                    self.board[move.end_r][move.end_c-2] = self.board[move.end_r][move.end_c+1]
                    self.board[move.end_r][move.end_c+1] = "--"

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

    def get_valid_moves(self):
        """
        Calcula los movimientos considerando los posibles jaques
        :return: Devuelve solo los movimientos válidos
        """
        temp_enpassant = self.enpassant_possible
        temp_castle_rights = CastleRights(self.current_castling_rights.white_ks, self.current_castling_rights.black_ks,
                                          self.current_castling_rights.white_qs, self.current_castling_rights.black_qs)
        moves = self.get_possible_moves()
        if self.white_turn:
            self.get_castle_moves(self.white_king_pos[0], self.white_king_pos[1], moves)
        else:
            self.get_castle_moves(self.black_king_pos[0], self.black_king_pos[1], moves)
        for i in range(len(moves)-1, -1, -1):
            self.make_move(moves[i])
            self.white_turn = not self.white_turn
            if self.check():
                moves.remove(moves[i])
            self.white_turn = not self.white_turn
            self.undo_move()
        if len(moves) == 0:
            if self.check():
                self.check_mate = True
            else:
                self.stale_mate = True
        else:
            self.check_mate = False
            self.stale_mate = False
        self.enpassant_possible = temp_enpassant
        self.current_castling_rights = temp_castle_rights
        return moves

    def check(self):
        """
        Determina si hay jaque
        :return: boolean
        """
        if self.white_turn:
            return self.square_attacked(self.white_king_pos[0], self.white_king_pos[1])
        else:
            return self.square_attacked(self.black_king_pos[0], self.black_king_pos[1])

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

    def single_moves(self, r, c, moves, dirs):
        """
        Función para calcular movimientos del caballero y del rey
        :param r: fila
        :param c: columna
        :param moves: lista de movimientos
        :param dirs: direcciones de movimiento
        :return: lista de movimientos actualizados
        """
        color = "w" if self.white_turn else "b"
        for i in range(len(dirs)):
            end_r = r + dirs[i][0]
            end_c = c + dirs[i][1]
            if 0 <= end_r <= 7 and 0 <= end_c <= 7:
                if self.board[end_r][end_c][0] != color:
                    moves.append(Move((r, c), (end_r, end_c), self.board))  # Casilla vacía o pieza enemiga

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
        for i in range(len(dirs)):
            for j in range(1, len(self.board)):
                end_r = r + dirs[i][0] * j
                end_c = c + dirs[i][1] * j
                if 0 <= end_r <= 7 and 0 <= end_c <= 7:
                    if self.board[end_r][end_c] == "--":
                        moves.append(Move((r, c), (end_r, end_c), self.board))  # casilla vacía
                    elif self.board[end_r][end_c][0] != color:
                        moves.append(Move((r, c), (end_r, end_c), self.board))  # pieza enemigo
                        break
                    else:
                        break  # pieza amiga
                else:
                    break  # fuera de los límites

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
        if self.board[r][c+1] == "--" and self.board[r][c+2] == "--":  # verifica que las casillas estén vacías
            if not self.square_attacked(r, c+1) and not self.square_attacked(r, c+2):  # verifica casillas en jaque
                moves.append(Move((r, c), (r, c+2), self.board, castle=True))

    def get_qs_moves(self, r, c, moves):
        """
        Movimientos del lado de la reina
        """
        if self.board[r][c-1] == "--" and self.board[r][c-2] == "--" and self.board[r][c-3] == "--":
            if not self.square_attacked(r, c-1) and not self.square_attacked(r, c-2):  # verifica casillas en jaque
                moves.append(Move((r, c), (r, c-2), self.board, castle=True))

    def pawn_moves(self, r, c, moves):
        """
        Obtener movimientos del peon r, c
        :param r: fila
        :param c: columna
        :param moves: lista de movimientos
        :return: lista de movimientos del peón actualizados
        """
        if self.white_turn:  # peón blanco
            if self.board[r-1][c] == "--":  # avance de 1 casilla
                moves.append(Move((r, c), (r-1, c), self.board))
                if r == 6 and (self.board[r-2][c]):
                    moves.append(Move((r, c), (r-2, c), self.board))  # avance de 2 casillas
            if c != 0:
                if self.board[r-1][c-1][0] == "b":
                    moves.append(Move((r, c), (r-1, c-1), self.board))  # captura a la izquierda
                elif (r-1, c-1) == self.enpassant_possible:
                    moves.append(Move((r, c), (r-1, c-1), self.board, enpassant=True))  # captura al paso izquierda
            if c != 7:
                if self.board[r-1][c+1][0] == "b":
                    moves.append(Move((r, c), (r-1, c+1), self.board))  # captura a la derecha
                elif (r-1, c+1) == self.enpassant_possible:
                    moves.append(Move((r, c), (r-1, c+1), self.board, enpassant=True))  # captura al paso derecha
        else:  # peón negro
            if self.board[r+1][c] == "--":
                moves.append(Move((r, c), (r+1, c), self.board))  # avance de 1 casilla
                if r == 1 and (self.board[r+2][c] == "--"):
                    moves.append(Move((r, c), (r+2, c), self.board))  # avance de 2 casillas
            if c != 0:
                if self.board[r+1][c-1][0] == "w":
                    moves.append(Move((r, c), (r+1, c-1), self.board))  # captura a la izquierda
                elif (r+1, c-1) == self.enpassant_possible:
                    moves.append(Move((r, c), (r+1, c-1), self.board, enpassant=True))  # captura al paso izquierda
            if c != 7:
                if self.board[r+1][c+1][0] == "w":
                    moves.append(Move((r, c), (r+1, c+1), self.board))  # captura a la derecha
                elif (r+1, c+1) == self.enpassant_possible:
                    moves.append(Move((r, c), (r+1, c+1), self.board, enpassant=True))  # captura al paso derecha

    def rook_moves(self, r, c, moves):
        """
        Obtener movimientos de la torre r, c
        :param r: fila
        :param c: columna
        :param moves: lista de movimientos
        :return: lista de movimientos de la torre actualizados
        """
        dirs = ((-1, 0), (0, 1), (1, 0), (0, -1))
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
        self.single_moves(r, c, moves, dirs)

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
        self.single_moves(r, c, moves, dirs)


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
        self.piece_capture = board[self.end_r][self.end_c]
        # pawn promotion
        self.pawn_promotion = (self.piece_moved == "wP" and self.end_r == 0) or \
                              (self.piece_moved == "bP" and self.end_r == 7)
        # en passant
        self.enpassant_move = enpassant
        if self.enpassant_move:
            self.piece_capture = "wP" if self.piece_moved == "bP" else "bP"
        # castling
        self.castle_move = castle

        self.move_id = self.start_r*1000 + self.start_c*100 + self.end_r*10 + self.end_c

    def get_notation(self):
        """
        :return: Notación del ajedrez del movimiento
        """
        return self.get_rank_file(self.start_r, self.start_c) +\
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
