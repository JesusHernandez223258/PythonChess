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

    def make_move(self):pass

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
    def __init__(self):pass

    def get_move_annotation(self):pass

    def __eq__(self, other):pass

    def __str__(self):pass
