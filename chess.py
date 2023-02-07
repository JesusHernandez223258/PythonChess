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

    def make_move(self, move):
        """
        Hacer un movimiento
        :param move:
        """
        self.board[move.start_r][move.start_c] = "--"
        self.board[move.end_r][move.end_c] = move.piece_moved
        self.move_log.append(move)
        self.white_turn = not self.white_turn

    def undo_move(self):
        """
        Deshacer ultimo movimiento
        """
        if len(self.move_log) != 0:
            move = self.move_log.pop()
            self.board[move.end_r][move.end_c] = move.piece_capture
            self.board[move.start_r][move.start_c] = move.piece_moved
            self.white_turn = not self.white_turn

    def get_valid_moves(self):
        """
        Movimientos considerando jaques
        """
        return self.get_possible_moves()

    def check(self):pass

    def square_attacked(self):pass

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
                if self.board[r-2][c] == "--" and r == 6:
                    moves.append(Move((r, c), (r-2, c), self.board))  # avance de 2 casillas
            if c != 0:
                if self.board[r-1][c-1][0] == "b":
                    moves.append(Move((r, c), (r-1, c-1), self.board))  # captura a la izquierda
            if c != 7:
                if self.board[r-1][c+1][0] == "b":
                    moves.append(Move((r, c), (r-1, c+1), self.board))  # captura a la derecha
        else:  # peón negro
            if self.board[r+1][c] == "--":
                moves.append(Move((r, c), (r+1, c), self.board))  # avance de 1 casilla
                if self.board[r+2][c] == "--" and r == 1:
                    moves.append(Move((r, c), (r+2, c), self.board))  # avance de 2 casillas
            if c != 0:
                if self.board[r+1][c-1][0] == "w":
                    moves.append(Move((r, c), (r+1, c-1), self.board))  # captura a la izquierda
            if c != 7:
                if self.board[r+1][c+1][0] == "w":
                    moves.append(Move((r, c), (r+1, c+1), self.board))  # captura a la derecha

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


class Move:
    ranks_rows = {"1": 7, "2": 6, "3": 5, "4": 4,
                  "5": 3, "6": 2, "7": 1, "8": 0}
    rows_ranks = {v: k for k, v in ranks_rows.items()}
    files_cols = {"a": 0, "b": 1, "c": 2, "d": 3,
                  "e": 4, "f": 5, "g": 6, "h": 7}
    cols_files = {v: k for k, v in files_cols.items()}

    def __init__(self, start, end, board):
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

