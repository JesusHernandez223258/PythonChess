from settings import *
from chess import GameState, Move
import pygame as pg


class Game:
    def __init__(self):
        self.images = {}
        self.title = TITLE
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.screen.fill("White")
        self.clock = pg.time.Clock()
        self.game_state = GameState()
        self.running = True

        self.selected = ()
        self.clicks = []

    def load_images(self):
        pieces = ["bP", "bR", "bB", "bN", "bQ", "bK", "wP", "wR", "wB", "wN", "wQ", "wK"]
        for piece in pieces:
            self.images[piece] = pg.image.load(DIR+piece+".png")

    def check_events(self):
        for e in pg.event.get():
            if e.type == pg.QUIT:
                self.running = False
            elif e.type == pg.MOUSEBUTTONDOWN:
                loc = pg.mouse.get_pos()
                col = loc[0] // SQ_SIZE
                row = loc[1] // SQ_SIZE
                if self.selected == (row, col):
                    self.selected = ()
                    self.clicks = []
                else:
                    self.selected = (row, col)
                    self.clicks.append(self.selected)
                if len(self.clicks) == 2:
                    move = Move((self.clicks[0]), (self.clicks[1]), self.game_state.board)
                    self.game_state.make_move(move)
                    print(move.get_notation())
                    self.selected = ()
                    self.clicks = []

    def draw_board(self):
        colors = [pg.Color(DARK), pg.Color(LIGHT)]
        for r in range(DIMS):
            for c in range(DIMS):
                color = colors[(r+c) % 2]
                cas = pg.Surface((SQ_SIZE, SQ_SIZE))
                cas.fill(color)
                self.screen.blit(cas, (r*SQ_SIZE, c*SQ_SIZE))

    def draw_pieces(self):
        for r in range(DIMS):
            for c in range(DIMS):
                piece = self.game_state.board[r][c]
                if piece != "--":
                    self.screen.blit(self.images[piece],
                                     pg.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
    def draw_highlight(self):pass

    def draw_game_state(self):
        self.draw_board()
        self.draw_highlight()
        self.draw_pieces()

    def main(self):
        pg.init()
        self.load_images()

        pg.display.set_caption(f"{self.title}-{self.clock.get_fps() :.1f}")

        while self.running:
            self.check_events()
            self.draw_game_state()
            self.clock.tick(FPS)
            pg.display.flip()
