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

    def load_images(self):
        pieces = ["bP", "bR", "bB", "bN", "bQ", "bK", "wP", "wR", "wB", "wN", "wQ", "wK"]
        for piece in pieces:
            self.images[piece] = pg.image.load(DIR+piece+".png")

    def check_events(self):
        for e in pg.event.get():
            if e.type == pg.QUIT:
                self.running = False

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
        self.clock.tick(FPS)
        pg.display.set_caption(f"{self.title}-{self.clock.get_fps() :.1f}")

        while self.running:
            self.check_events()
            self.draw_game_state()
            pg.display.flip()
