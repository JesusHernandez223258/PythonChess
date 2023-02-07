from settings import *
from chess import GameState, Move
import pygame as pg

#  Highlight el ultimo movimiento realizado


class Game:
    def __init__(self):
        self.images = {}
        self.move_options = ""
        self.title = TITLE
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.screen.fill("White")
        self.clock = pg.time.Clock()
        self.game_state = GameState()
        self.valid_moves = self.game_state.get_valid_moves()
        self.move_made = False
        self.animate = False
        self.running = True
        self.game_over = False
        self.selected = ()
        self.clicks = []

    def load_images(self):
        """
        Carga imágenes necesarias para el juego
        """
        pieces = ["bP", "bR", "bB", "bN", "bQ", "bK", "wP", "wR", "wB", "wN", "wQ", "wK"]
        for piece in pieces:
            self.images[piece] = pg.image.load(DIR+piece+".png")
        self.move_options = pg.image.load(DIR+"option.png")  # Modificar imagen. Más pequeña y centrada
        self.move_options.set_alpha(120)

    def check_events(self):
        """
        Verifica eventos del teclado/mouse
        """
        for e in pg.event.get():
            if e.type == pg.QUIT:
                self.running = False
            elif e.type == pg.MOUSEBUTTONDOWN:
                if not self.game_over:
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
                            self.animate = True
                            print(f"{move.get_notation()} - {move.move_id}")
                            self.selected = ()
                            self.clicks = []
                        else:
                            self.clicks = [self.selected]
            elif e.type == pg.KEYDOWN:
                if e.key == pg.K_LCTRL:
                    self.game_state.undo_move()
                    self.move_made = True
                    self.animate = False
                if e.key == pg.K_r:
                    self.game_state = GameState()
                    self.valid_moves = self.game_state.get_valid_moves()
                    self.selected = ()
                    self.clicks = []
                    self.move_made = False
                    self.animate = False
                    self.game_over = False

        if self.move_made:
            if self.animate:
                self.animate_move(self.game_state.move_log[-1])
            self.valid_moves = self.game_state.get_valid_moves()
            self.move_made = False
            self.animate = False

    def draw_board(self):
        """
        Dibuja tablero
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
        Dibuja las piezas según el estado del tablero actual
        """
        for r in range(DIMS):
            for c in range(DIMS):
                piece = self.game_state.board[r][c]
                if piece != "--":
                    self.screen.blit(self.images[piece],
                                     pg.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

    def draw_highlight(self):
        """
        Marca la pieza seleccionada y sus movimientos válidos
        """
        if self.selected != ():
            r, c = self.selected[0], self.selected[1]
            if self.game_state.board[r][c][0] == ("w" if self.game_state.white_turn else "b"):
                s = pg.Surface((SQ_SIZE, SQ_SIZE))
                s.fill("yellow")
                s.set_alpha(120)
                self.screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
                for move in self.valid_moves:
                    if move.start_r == r and move.start_c == c:
                        self.screen.blit(self.move_options, (move.end_c*SQ_SIZE, move.end_r*SQ_SIZE))

    def draw_game_state(self):
        """
        Dibuja el estado del juego actual
        """
        self.draw_board()
        self.draw_highlight()
        self.draw_pieces()

    def animate_move(self, move):  # Reescribir código para no redibujar el tablero siempre
        """
        Anima los movimientos de las piezas
        """
        colors = [pg.Color(DARK), pg.Color(LIGHT)]
        delta_r = move.end_r - move.start_r
        delta_c = move.end_c - move.end_c
        frames_per_square = 8
        frame_count = (abs(delta_r) + abs(delta_c)) * frames_per_square
        for frame in range(frame_count+1):
            r, c = (move.start_r + delta_r*frame/frame_count, move.start_c + delta_c*frame/frame_count)
            self.draw_board()
            self.draw_pieces()
            color = colors[(move.end_r + move.end_c) % 2]
            end = pg.Rect(move.end_c*SQ_SIZE, move.end_r*SQ_SIZE, SQ_SIZE, SQ_SIZE)
            pg.draw.rect(self.screen, color, end)
            if move.piece_capture != "--":
                self.screen.blit(self.images[move.piece_capture], end)
            self.screen.blit(self.images[move.piece_moved], pg.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
            pg.display.flip()
            self.clock.tick(FPS)

    def main(self):
        """
        Función principal del juego
        """
        pg.init()
        self.load_images()

        pg.display.set_caption(f"{self.title}-{self.clock.get_fps() :.1f}")

        while self.running:
            self.check_events()
            self.draw_game_state()
            self.clock.tick(FPS)
            pg.display.flip()
