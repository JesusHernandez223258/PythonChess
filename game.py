import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import pygame as pg
from settings import *
from chess import GameState, Move
from player_Bot import Bot
from player_IA import Player
from openings import check_open
from multiprocessing import Process, Queue


class Game:
    def __init__(self):
        # Screen
        self.screen = pg.display.set_mode((BOARD_WIDTH + LOG_PANEL_WIDTH, BOARD_HEIGHT))
        self.screen.fill("White")
        self.clock = pg.time.Clock()
        self.images = {}
        self.font = None
        self.title = TITLE
        self.move_options_image = None
        self.move_capture_image = None
        self.menu_open = False
        # GameState
        self.running = True
        self.game_state = GameState()
        self.valid_moves = self.game_state.get_valid_moves()
        self.move_made = False
        self.animate = False
        self.game_over = False
        self.selected = ()
        self.clicks = []
        self.moves_count = 0
        self.state_log = [(self.game_state.board.copy(), self.game_state.white_turn, self.valid_moves.copy())]
        self.repetition_counter = 0
        self.end_info = ""
        # bot
        self.Bot_player = Bot()
        self.bot_moved = False
        # grafo
        self.graph = nx.Graph()  # Crear el grafo vacío
        self.move_nodes = []  # Lista para almacenar los nodos de los movimientos
        self.graph_layout = None  # Para guardar la disposición de los nodos en el grafo
        # player
        self.AI_player = Player()
        self.human_turn = None
        self.player_one = True  # True: human white, False: IA white
        self.player_two = True  # True: human Black, False: IA black
        self.thinking = False  # True si la IA esta "Pensando", False si no lo está
        self.move_undone = False
        self.move_finder_process = None
        self.return_queue = None

    def load_images(self):
        """
        Carga imágenes necesarias para el juego
        """
        pieces = ["bP", "bR", "bB", "bN", "bQ", "bK", "wP", "wR", "wB", "wN", "wQ", "wK"]
        for piece in pieces:
            self.images[piece] = pg.image.load(DIR+piece+".png")
        self.move_options_image = pg.image.load(DIR + "option.png")
        self.move_options_image.set_alpha(120)
        self.move_capture_image = pg.image.load(DIR + "capture.png")
        self.move_capture_image.set_alpha(120)

    def check_mouse(self):
        loc = pg.mouse.get_pos()
        if not self.game_over and not self.menu_open:
            col = loc[0] // SQ_SIZE
            row = loc[1] // SQ_SIZE
            if self.selected == (row, col) or col > 7:
                self.selected = ()
                self.clicks = []
            else:
                self.selected = (row, col)
                self.clicks.append(self.selected)
            if len(self.clicks) == 2 and self.human_turn:
                move = Move((self.clicks[0]), (self.clicks[1]), self.game_state.board)
                for i in range(len(self.valid_moves)):
                    if move == self.valid_moves[i]:
                        self.game_state.make_move(self.valid_moves[i])
                        self.move_made = True
                        self.animate = True
                        print(f"{move.get_notation()} - {move.move_id}")
                        self.selected = ()
                        self.clicks = []
                if not self.move_made:
                    self.clicks = [self.selected]
        if self.menu_open:
            if quit_rect.colliderect(loc[0], loc[1], 1, 1):
                self.running = False
            if enemy_rect.colliderect(loc[0], loc[1], 1, 1):
                self.reset()
                self.player_two = True if not self.player_two else False

    def check_keyboard(self, e):
        if e.key == pg.K_LCTRL and not self.menu_open:
            self.game_state.undo_move()
            self.move_made = True
            self.animate = False
            self.game_over = False
            if self.thinking:
                self.move_finder_process.terminate()
                self.thinking = False
            self.move_undone = True
            self.state_log.pop()
        if e.key == pg.K_r:
            self.reset()
        if e.key == pg.K_TAB:
            if self.menu_open:
                self.menu_open = False
            else:
                self.menu_open = True
            if self.menu_open:
                print("Menu desplegado")
            else:
                print("Menu cerrado")

    def check_ia(self):
        if not self.thinking:
            self.thinking = True
            print("Pensando...")
            self.return_queue = Queue()
            self.move_finder_process = Process(target=self.AI_player.best_move,
                                               args=(self.game_state, self.valid_moves, self.return_queue))
            self.move_finder_process.start()  # llama self.AI_player.best_move(self.game_state, self.valid_moves)

        if not self.move_finder_process.is_alive():  # si esta pensando todavía o no
            print("Listo!")
            ai_move = self.return_queue.get()
            if ai_move is None:
                print(len(self.valid_moves))
                ai_move = self.AI_player.random_move(self.valid_moves)
            self.game_state.make_move(ai_move)
            self.move_made = True
            self.animate = True
            self.thinking = False

    def check_bot(self):
        # Verifica si es el turno del bot, si no está pensando, y si el juego no ha terminado
        if not self.game_state.white_turn and not self.thinking and not self.game_state.checkmate and not self.game_state.stalemate and not self.bot_moved:
            self.thinking = True
            print("El bot está pensando...")
        
            # Obtener el siguiente movimiento del bot
            bot_move = self.Bot_player.get_move(self.game_state)
        
            if bot_move:  # Verificar si el bot encontró un movimiento válido
                self.game_state.make_move(bot_move)
                self.move_made = True
                self.animate = True
            else:
                print("El bot no pudo encontrar un movimiento válido.")
        
            # Indicar que el bot terminó de pensar y realizó su movimiento
            self.thinking = False
            self.bot_moved = True  # Marcar que el bot ya se movió en este turno

    def check_events(self):
        """
        Verifica eventos del teclado/mouse
        """
        if not self.game_state.white_turn and not self.game_state.checkmate and not self.game_state.stalemate:
            # Si es el turno del bot, no esperamos eventos del mouse ni teclado, solo realizamos el movimiento del bot
            self.check_bot()
        else:
            # Si no es el turno del bot, seguimos procesando los eventos de teclado y mouse
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    self.running = False
                elif e.type == pg.MOUSEBUTTONDOWN:
                    self.check_mouse()
                elif e.type == pg.KEYDOWN:
                    self.check_keyboard(e)

        # Si se ha realizado un movimiento, reiniciar las variables de estado
        if self.move_made:
            if self.animate:
                self.animate_move(self.game_state.move_log[-1])
            self.valid_moves = self.game_state.get_valid_moves()

            # Actualizar el estado del registro de movimientos
            if not self.move_undone:
                self.state_log.append((self.game_state.board.copy(), self.game_state.white_turn, self.valid_moves.copy()))
            self.threefold_repetition()

            self.move_made = False
            self.animate = False
            self.move_undone = False
            self.bot_moved = False  # Permitir que el bot se mueva en el próximo turno

            # Regla de los 50 movimientos consecutivos
            if len(self.game_state.move_log) >= 100:
                self.fifty_moves_rule()

        # Verificar el estado final del juego
        if self.game_state.checkmate or self.game_state.stalemate or self.game_state.draw:
            self.game_over = True
            text = "Stalemate" if self.game_state.stalemate else \
                "Draw" if self.game_state.draw else \
                "Black wins by checkmate" if self.game_state.white_turn else \
                "White wins by checkmate"
            self.draw_end_text(text)

        self.clock.tick(FPS)
        pg.display.flip()

    def draw_board(self):
        """
        Dibuja tablero
        """
        colors = [pg.Color(LIGHT), pg.Color(DARK)]
        for r in range(DIMS):
            for c in range(DIMS):
                color = colors[(r+c) % 2]
                cas = pg.Surface((SQ_SIZE, SQ_SIZE))
                cas.fill(color)
                self.screen.blit(cas, (r*SQ_SIZE, c*SQ_SIZE))

    def draw_highlight(self):
        """
        Marca la pieza seleccionada y sus movimientos válidos
        """
        s = pg.Surface((SQ_SIZE, SQ_SIZE))
        s.fill("yellow")
        s.set_alpha(120)
        if self.selected != ():
            r, c = self.selected[0], self.selected[1]
            if self.game_state.board[r][c][0] == ("w" if self.game_state.white_turn else "b"):
                self.screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
                for move in self.valid_moves:
                    if move.start_r == r and move.start_c == c:
                        color = "b" if self.game_state.white_turn else "w"
                        if self.game_state.board[move.end_r][move.end_c][0] == color:
                            self.screen.blit(self.move_capture_image, (move.end_c * SQ_SIZE, move.end_r * SQ_SIZE))
                        else:
                            self.screen.blit(self.move_options_image, (move.end_c * SQ_SIZE, move.end_r * SQ_SIZE))
        if len(self.game_state.move_log) != 0:
            move = self.game_state.move_log[-1]
            self.screen.blit(s, (move.start_c*SQ_SIZE, move.start_r*SQ_SIZE))
            self.screen.blit(s, (move.end_c * SQ_SIZE, move.end_r * SQ_SIZE))

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

    def draw_move_log(self):  # probar con itertools
        """
        Dibuja en pantalla los movimientos realizados
        """
        log_rect = pg.Rect(BOARD_WIDTH, 0, LOG_PANEL_WIDTH, LOG_PANEL_HEIGHT)
        pg.draw.rect(self.screen, pg.Color("black"), log_rect)
        move_log = self.game_state.move_log
        move_texts = []
        for i in range(0, len(move_log), 2):
            move_string = str(i//2 + 1) + "." + str(move_log[i]) + " "
            if i + 1 < len(move_log):
                move_string += str(move_log[i+1]) + "  "
            move_texts.append(move_string)
        mpr = 2
        padding = 5
        spacing = 5
        text_y = padding
        for i in range(0, len(move_texts), mpr):
            text = ""
            for j in range(mpr):
                if i + j < len(move_texts):
                    text += move_texts[i+j]
            text_object = self.font.render(text, True, pg.Color("white"))
            text_loc = log_rect.move(padding, text_y)
            self.screen.blit(text_object, text_loc)
            text_y += text_object.get_height() + spacing

    def check_opening(self):
        """
        Verifica que opening está siendo utilizado según los primeros movimientos hechos y su orden
        """
        text_object = self.font.render("Actual Opening:", True, pg.Color("white"))
        text_loc = pg.Rect(BOARD_WIDTH + ((LOG_PANEL_WIDTH - text_object.get_width()) // 2),
                           BOARD_HEIGHT - text_object.get_height() - 40, text_object.get_width(),
                           text_object.get_height())
        self.screen.blit(text_object, text_loc)
        opening = check_open(self.game_state.move_log)
        self.draw_opening(opening)

    def draw_opening(self, opening):
        """
        Escribe el opening usado en la pantalla
        :param opening: opening usado
        """
        text_object = self.font.render(opening, True, pg.Color("white"))
        text_loc = pg.Rect(BOARD_WIDTH+((LOG_PANEL_WIDTH-text_object.get_width())//2),
                           BOARD_HEIGHT-text_object.get_height()-10, text_object.get_width(),
                           text_object.get_height())
        self.screen.blit(text_object, text_loc)

    def draw_end_text(self, text):
        """
        Dibuja en la pantalla final el ganador del juego
        :param text: Texto a mostrar
        """
        font = pg.font.SysFont("Arial", 32, True, False)
        text_object = font.render(text, False, pg.Color("grey"))
        text_loc = pg.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT).move(BOARD_WIDTH / 2 - text_object.get_width() / 2,
                                                                 BOARD_HEIGHT / 2 - text_object.get_height() / 2)  # center text
        self.screen.blit(text_object, text_loc)
        text_object = font.render(text, False, pg.Color("black"))
        self.screen.blit(text_object, text_loc.move(2, 2))

        text_object = self.font.render(self.end_info, True, pg.Color("grey"))
        text_loc = pg.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT).move(BOARD_WIDTH / 2 - text_object.get_width() / 2,
                                                                 BOARD_HEIGHT / 2 - text_object.get_height() / 2)  # center text
        self.screen.blit(text_object, text_loc.move(0, 40))
        text_object = self.font.render(self.end_info, True, pg.Color("black"))
        self.screen.blit(text_object, text_loc.move(0, 42))

    def animate_move(self, move):  # Reescribir código para no redibujar el tablero siempre
        """
        Anima los movimientos de las piezas
        """
        colors = [pg.Color(DARK), pg.Color(LIGHT)]
        delta_r = move.end_r - move.start_r
        delta_c = move.end_c - move.start_c
        frames_per_square = 6
        frame_count = (abs(delta_r) + abs(delta_c)) * frames_per_square
        for frame in range(frame_count+1):
            r, c = (move.start_r + delta_r*frame/frame_count, move.start_c + delta_c*frame/frame_count)
            self.draw_board()
            self.draw_pieces()
            color = colors[(move.end_r + move.end_c) % 2]
            end = pg.Rect(move.end_c*SQ_SIZE, move.end_r*SQ_SIZE, SQ_SIZE, SQ_SIZE)
            pg.draw.rect(self.screen, color, end)
            if move.piece_captured != "--":
                if move.enpassant_move:
                    enpassant_r = (move.end_r + 1) if move.piece_captured[0] == "b" else (move.end_r - 1)
                    end = pg.Rect(move.end_c * SQ_SIZE, enpassant_r * SQ_SIZE, SQ_SIZE, SQ_SIZE)
                self.screen.blit(self.images[move.piece_captured], end)
            self.screen.blit(self.images[move.piece_moved], pg.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
            pg.display.flip()
            self.clock.tick(FPS)

    def fifty_moves_rule(self):
        """
        Se encarga de verificar la regla de los 50 movimientos consecutivos sin capturas ni movimientos de peones
        """
        last_move = self.game_state.move_log[-1]
        if last_move.piece_captured != "--" or last_move.piece_moved[1] == "P":
            self.moves_count = 0
        else:
            self.moves_count += 1
        if self.moves_count == 100:
            self.game_state.draw = True
            self.end_info = "50 consecutive moves without captures or pawn moves."

    def threefold_repetition(self):
        temp_state = self.state_log[-1]
        for i in range(len(self.state_log) - 2, -1, -1):
            if np.array_equiv(self.state_log[i][0], temp_state[0]) and self.state_log[i][1] == temp_state[1] and self.state_log[i][2] == temp_state[2]:
                self.repetition_counter += 1
        if self.repetition_counter == 3:
            self.game_state.draw = True
            self.end_info = "Draw for Threefold Repetition"
        else:
            self.repetition_counter = 0

    def menu(self):
        """
        Dibuja el menu de opciones
        """
        menu_rect = pg.Rect(0, 0, MENU_WIDTH, MENU_HEIGHT)
        pg.draw.rect(self.screen, pg.Color("GREY"), menu_rect)
        menu_text_object = self.font.render("MENU", True, pg.Color("black"))
        text_loc = pg.Rect(0, 0, MENU_WIDTH, MENU_HEIGHT).move(MENU_WIDTH / 2 - menu_text_object.get_width() / 2, 10)
        self.screen.blit(menu_text_object, text_loc)

        # Salir
        global quit_rect
        quit_rect = pg.Rect(20, MENU_HEIGHT-44, BUTTON_WIDTH, BUTTON_HEIGHT)
        pg.draw.rect(self.screen, pg.Color("red"), quit_rect)
        button_object = self.font.render("QUIT", True, pg.Color("black"))
        button_loc = pg.Rect(20 + ((quit_rect.width - button_object.get_width()) / 2),
                             MENU_HEIGHT-44 + ((quit_rect.height - button_object.get_height()) / 2),
                             BUTTON_WIDTH, BUTTON_HEIGHT)
        self.screen.blit(button_object, button_loc)

        # Enemy
        global enemy_rect
        text = "IA" if self.player_two else "HUMAN"
        button_object = self.font.render(text, True, pg.Color("black"))
        enemy_rect = pg.Rect(0, 0, BUTTON_WIDTH, BUTTON_HEIGHT).move(20, MENU_HEIGHT / 2 - button_object.get_height() / 2 - 2)
        pg.draw.rect(self.screen, pg.Color("white"), enemy_rect)
        button_loc = pg.Rect(0, 0, BUTTON_WIDTH, BUTTON_HEIGHT).move(MENU_WIDTH / 2 - button_object.get_width() / 2,
                                                                     MENU_HEIGHT / 2 - button_object.get_height() / 2)
        self.screen.blit(button_object, button_loc)

    def draw_game_state(self):
        """
        Dibuja el estado del juego actual
        """
        self.draw_board()
        self.draw_highlight()
        self.draw_pieces()
        self.draw_move_log()
        self.check_opening()

    def reset(self):
        """
        Resetea el juego completamente
        """
        self.game_state = GameState()
        self.valid_moves = self.game_state.get_valid_moves()
        self.selected = ()
        self.clicks = []
        self.move_made = False
        self.animate = False
        self.game_over = False
        self.menu_open = False
        self.moves_count = 0
        self.state_log = [(self.game_state.board.copy(), self.game_state.white_turn, self.valid_moves.copy())]
        self.repetition_counter = 0
        if self.thinking:
            self.move_finder_process.terminate()
            self.thinking = False
        self.move_undone = True

    def main(self):
        """
        Función principal del juego
        """
        pg.init()
        self.load_images()
        self.font = pg.font.SysFont("Arial", 22, False, False)
    
        pg.display.set_caption(f"{self.title}-{self.clock.get_fps() :.1f}")
    
        while self.running:
            # Verificar si es el turno del humano o del bot
            self.human_turn = (self.game_state.white_turn and self.player_one) or \
                              (not self.game_state.white_turn and self.player_two)
    
            # Si es el turno del bot, permitir que haga su movimiento automáticamente
            if not self.game_state.white_turn and not self.thinking and not self.game_state.checkmate and not self.game_state.stalemate:
                self.check_bot()  # Llamada para que el bot realice su movimiento
    
            # Ahora manejamos los eventos solo si es el turno del jugador humano
            if self.human_turn:
                self.check_events()  # Esto maneja la entrada de teclado y mouse para el jugador humano
    
            if not self.game_over:
                self.draw_game_state()  # Actualiza el estado del juego
    
            if self.menu_open:
                self.menu()  # Si hay un menú abierto, dibujarlo
    
            # Mantener la velocidad del juego
            self.clock.tick(FPS)
    
            # Actualizar la pantalla
            pg.display.flip()
