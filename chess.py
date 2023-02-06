import numpy as np


class GameState:
    def __init__(self):
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
        self.board[move.start_r][move.start_c] = "--"
        self.board[move.end_r][move.end_c] = move.piece_moved
        self.move_log.append(move)
        self.white_turn = not self.white_turn

    def undo_move(self):pass

    def get_valid_moves(self):pass

    def check(self):pass

    def square_attacked(self):pass

    def get_possible_moves(self):pass

    def pawn_moves(self):pass

    def rook_moves(self):pass

    def knight_moves(self):pass

    def bishop_moves(self):pass

    def queen_moves(self):pass

    def king_moves(self):pass


class Move:
    ranks_rows = {"1": 7, "2": 6, "3": 5, "4": 4,
                  "5": 3, "6": 2, "7": 1, "8": 0}
    rows_ranks = {v: k for k, v in ranks_rows.items()}
    files_cols = {"a": 0, "b": 1, "c": 2, "d": 3,
                  "e": 4, "f": 5, "g": 6, "h": 7}
    cols_files = {v: k for k, v in files_cols.items()}

    def __init__(self, start, end, board):
        self.start_r = start[0]
        self.start_c = start[1]
        self.end_r = end[0]
        self.end_c = end[1]
        self.piece_moved = board[self.start_r][self.start_c]
        self.piece_capture = board[self.end_r][self.start_c]

    def get_notation(self):
        return self.get_rank_file(self.start_r, self.start_c) +\
            self.get_rank_file(self.end_r, self.end_c)

    def get_rank_file(self, r, c):
        return self.cols_files[c] + self.rows_ranks[r]

    def __eq__(self, other):pass
