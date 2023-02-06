import numpy as np


class GameState:
    def __init__(self):
        """
        estado actual del juego
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
        movimientos considerando jaques
        """
        return self.get_possible_moves()

    def check(self):pass

    def square_attacked(self):pass

    def get_possible_moves(self):
        """
        movimientos sin considerar jaques
        """
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn, piece = self.board[r][c][0], self.board[r][c][1]
                if (turn == "w" and self.white_turn) and (turn == "b" and not self.white_turn):
                    match piece:
                        case "P":
                            self.pawn_moves(r, c, moves)
                        case "R":
                            self.rook_moves(r, c, moves)
                        case "N":
                            self.knight_moves(r, c, moves)
                        case "B":
                            self.bishop_moves(r, c, moves)
                        case "Q":
                            self.queen_moves(r, c, moves)
                        case "K":
                            self.king_moves(r, c, moves)
        return moves

    def pawn_moves(self, r, c, moves):
        """
        obtener movimientos del peon r, c
        :param r: fila
        :param c: columna
        :param moves: lista de movimientos
        :return: movimientos del peon
        """

    def rook_moves(self, r, c, moves):
        """
        obtener movimientos de la torre r, c
        :param r: fila
        :param c: columna
        :param moves: lista de movimientos
        :return: movimientos de la torre
        """

    def knight_moves(self, r, c, moves):
        """
        obtener movimientos del caballero r, c
        :param r: fila
        :param c: columna
        :param moves: lista de movimientos
        :return: movimientos del caballero
        """

    def bishop_moves(self, r, c, moves):
        """
        obtener movimientos del alfin r, c
        :param r: fila
        :param c: columna
        :param moves: lista de movimientos
        :return: movimientos del alfin
        """

    def queen_moves(self, r, c, moves):
        """
        obtener movimientos de la reina r, c
        :param r: fila
        :param c: columna
        :param moves: lista de movimientos
        :return: movimientos de la reina
        """

    def king_moves(self, r, c, moves):
        """
        obtener movimientos del rey r, c
        :param r: fila
        :param c: columna
        :param moves: lista de movimientos
        :return: movimientos del rey
        """


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
        :return: notacion del ajedrez del movimiento
        """
        return self.get_rank_file(self.start_r, self.start_c) +\
            self.get_rank_file(self.end_r, self.end_c)

    def get_rank_file(self, r, c):
        """
        :param r: fila
        :param c: columna
        :return: notacion de ajedrez de la casilla
        """
        return self.cols_files[c] + self.rows_ranks[r]

    def __eq__(self, other):
        """
        sobreescribir el metodo de igualdad
        :param other: objeto a igualar
        :return: bollean
        """
        if isinstance(other, Move):
            return other.move_id == self.move_id
        return False

