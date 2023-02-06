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
        self.valid_moves = self.game_state.get_valid_moves()
        self.move_made = False
        self.running = True

        self.selected = ()
        self.clicks = []


    def load_images(self):
        """
        carga imagenes necesarias para el juego
        """
        pieces = ["bP", "bR", "bB", "bN", "bQ", "bK", "wP", "wR", "wB", "wN", "wQ", "wK"]
        for piece in pieces:
            self.images[piece] = pg.image.load(DIR+piece+".png")

    def check_events(self):
        """
        verifica eventos del teclado/mouse
        """
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
                    if move in self.valid_moves:
                        self.game_state.make_move(move)
                        self.move_made = True
                    print(f"{move.get_notation()} - {move.move_id}")
                    self.selected = ()
                    self.clicks = []
            elif e.type == pg.KEYDOWN:
                if e.key == pg.K_LCTRL:
                    self.game_state.undo_move()
                    self.move_made = True

        if self.move_made:
            self.valid_moves = self.game_state.get_valid_moves()
            self.move_made = False

    def draw_board(self):
        """
        dibuja tablero
        """
        colors = [pg.Color(DARK), pg.Color(LIGHT)]
        for r in range(DIMS):
            for c in range(DIMS):
                color = colors[(r+c) % 2]
                cas = pg.Surface((SQ_SIZE, SQ_SIZE))
                cas.fill(color)
                self.screen.blit(cas, (r*SQ_SIZE, c*SQ_SIZE))

    def draw_pieces(self):
        """
        dibuja las piezas segun el estado del tablero actual
        """
        for r in range(DIMS):
            for c in range(DIMS):
                piece = self.game_state.board[r][c]
                if piece != "--":
                    self.screen.blit(self.images[piece],
                                     pg.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
    def draw_highlight(self):pass

    def draw_game_state(self):
        """
        dibuja el estado del juego actual
        """
        self.draw_board()
        self.draw_highlight()
        self.draw_pieces()

    def main(self):
        """
        funcion principal del juego
        """
        pg.init()
        self.load_images()

        pg.display.set_caption(f"{self.title}-{self.clock.get_fps() :.1f}")

        while self.running:
            self.check_events()
            self.draw_game_state()
            self.clock.tick(FPS)
            pg.display.flip()
