from chess import GameState, Move
import random
import numpy as np
import math

class AFD:
    def __init__(self, estados, transiciones, estado_inicial):
        self.estados = estados
        self.transiciones = transiciones
        self.estado_actual = estado_inicial

    def realizar_transicion(self, entrada):
        """
        Realiza una transición basada en la entrada.
        :param entrada: Movimiento o jugada a procesar.
        :return: Nuevo estado después de la transición.
        """
        if entrada in self.transiciones.get(self.estado_actual, {}):
            nuevo_estado = self.transiciones[self.estado_actual][entrada]
            self.estado_actual = nuevo_estado
            return self.estado_actual
        else:
            raise ValueError(f"Entrada '{entrada}' no válida para el estado '{self.estado_actual}'.")



    def reset_estado(self, estado_inicial):
        """
        Restablece el estado actual al inicial.
        """
        self.estado_actual = estado_inicial

    def obtener_estado_actual(self):
        """
        Devuelve el estado actual del AFD.
        :return: El estado actual.
        """
        return self.estado_actual
    def obtener_estados(self):
        # Los estados son las claves principales del diccionario de transiciones.
        return self.obtener_transiciones().keys()

    def obtener_transiciones(self):
        # Devuelve las transiciones tal como las definiste.
        return {
                "inicio": {
                    "Jaque Mate del Pastor": "pastor_1",
                    "Jaque Mate del Loco": "loco_1",
                    "Defensa Siciliana": "siciliana_1",
                    "Gambito de Dama": "gambito_dama_1",
                    "Defensa Caro-Kann": "caro_kann_1",
                    "Apertura Italiana": "italiana_1",
                    "Apertura Española": "espanola_1",
                    "Defensa Francesa": "francesa_1",
                    "Defensa Alekhine": "alekhine_1",
                    "Defensa Escandinava": "escandinava_1",
                    "Ataque de Londres": "londres_1",
                    "Gambito de Rey": "gambito_rey_1",
                    "Gambito Letón": "leton_1",
                    "Apertura Inglesa": "inglesa_1",
                    "Apertura Reti": "reti_1",
                    "Gambito Evans": "evans_1"
                },
                "pastor_1": {
                    "[1,4] → [3,4]": "pastor_2"
                },
                "pastor_2": {
                    "[6,4] → [4,4]": "pastor_3"
                },
                "pastor_3": {
                    "[0,5] → [4,1]": "pastor_4"
                },
                "pastor_4": {
                    "[7,6] → [5,5]": "fin"
                },
                "loco_1": {
                    "[1,5] → [2,5]": "loco_2"
                },
                "loco_2": {
                    "[6,4] → [4,4]": "loco_3"
                },
                "loco_3": {
                    "[1,6] → [3,6]": "fin"
                },
                "siciliana_1": {
                    "[1,4] → [3,4]": "siciliana_2"
                },
                "siciliana_2": {
                    "[6,2] → [4,2]": "fin"
                },
                "gambito_dama_1": {
                    "[1,3] → [3,3]": "gambito_dama_2"
                },
                "gambito_dama_2": {
                    "[6,3] → [4,3]": "gambito_dama_3"
                },
                "gambito_dama_3": {
                    "[1,2] → [3,2]": "fin"
                },
                "caro_kann_1": {
                    "[1,4] → [3,4]": "caro_kann_2"
                },
                "caro_kann_2": {
                    "[6,2] → [4,2]": "fin"
                },
                "italiana_1": {
                    "[1,4] → [3,4]": "italiana_2"
                },
                "italiana_2": {
                    "[6,4] → [4,4]": "italiana_3"
                },
                "italiana_3": {
                    "[0,6] → [2,5]": "italiana_4"
                },
                "italiana_4": {
                    "[7,1] → [5,2]": "italiana_5"
                },
                "italiana_5": {
                    "[0,5] → [4,1]": "fin"
                },
                "espanola_1": {
                    "[1,4] → [3,4]": "espanola_2"
                },
                "espanola_2": {
                    "[0,6] → [2,5]": "espanola_3"
                },
                "espanola_3": {
                    "[0,5] → [3,2]": "espanola_4"
                },
                "espanola_4": {
                    "[7,2] → [5,3]": "espanola_5"
                },
                "espanola_5": {
                    "[0,4] → [4,0]": "fin"
                },
                "francesa_1": {
                    "[1,4] → [3,4]": "francesa_2"
                },
                "francesa_2": {
                    "[6,3] → [4,3]": "fin"
                },
                "alekhine_1": {
                    "[1,4] → [3,4]": "alekhine_2"
                },
                "alekhine_2": {
                    "[6,3] → [4,3]": "fin"
                },
                "escandinava_1": {
                    "[1,4] → [3,4]": "escandinava_2"
                },
                "escandinava_2": {
                    "[6,1] → [4,1]": "fin"
                },
                "londres_1": {
                    "[1,3] → [3,3]": "londres_2"
                },
                "londres_2": {
                    "[0,2] → [2,4]": "londres_3"
                },
                "londres_3": {
                    "[7,1] → [5,2]": "fin"
                },
                "gambito_rey_1": {
                    "[1,4] → [3,4]": "gambito_rey_2"
                },
                "gambito_rey_2": {
                    "[1,5] → [3,5]": "gambito_rey_3"
                },
                "gambito_rey_3": {
                    "[7,1] → [5,2]": "fin"
                },
                "leton_1": {
                    "[1,4] → [3,4]": "leton_2"
                },
                "leton_2": {
                    "[0,6] → [2,5]": "leton_3"
                },
                "leton_3": {
                    "[0,5] → [3,2]": "leton_4"
                },
                "leton_4": {
                    "[7,2] → [5,3]": "fin"
                },
                "inglesa_1": {
                    "[1,2] → [3,2]": "fin"
                },
                "reti_1": {
                    "[0,6] → [2,5]": "reti_2"
                },
                "reti_2": {
                    "[1,2] → [3,2]": "reti_3"
                },
                "reti_3": {
                    "[0,3] → [2,4]": "fin"
                },
                "evans_1": {
                    "[1,4] → [3,4]": "evans_2"
                },
                "evans_2": {
                    "[0,6] → [2,5]": "evans_3"
                },
                "evans_3": {
                    "[0,5] → [4,1]": "evans_4"
                },
                "evans_4": {
                    "[1,1] → [3,1]": "evans_5"
                },
                "evans_5": {
                    "[1,4] → [3,4]": "evans_6"
                },
                "evans_6": {
                    "[0,6] → [2,5]": "evans_7"
                },
                "evans_7": {
                    "[1,1] → [3,1]": "fin"
                }
            }

class Bot:
    def __init__(self, piece_values=None):
        if piece_values is None:
            piece_values = {"K": 0, "Q": 10, "R": 5, "B": 3, "N": 3, "P": 1}
        
        # Inicialización de los valores de las piezas y la puntuación del tablero
        self.piece_values = piece_values
        self.MAX_DEPTH = 4
        self.CHECKMATE = 1000
        self.STALEMATE = 0

        # Tabla de movimientos predefinidos
        self.predefined_moves = {
            "Jaque Mate del Pastor": [
                [(1, 4), (3, 4)], [(0, 3), (4, 7)], [(0, 5), (4, 1)]
            ],
            "Jaque Mate del Loco": [
                [(1, 5), (2, 5)], [(1, 6), (3, 6)], [(0, 3), (3, 7)]
            ],
            "Defensa Siciliana": [
                [(1, 4), (3, 4)]
            ],
            "Gambito de Dama": [
                [(1, 3), (3, 3)], [(1, 2), (3, 2)]
            ],
            "Defensa Caro-Kann": [
                [(1, 4), (3, 4)]
            ],
            "Apertura Italiana": [
                [(1, 4), (3, 4)], [(0, 6), (2, 5)], [(0, 5), (4, 1)]
            ],
            "Apertura Española": [
                [(1, 4), (3, 4)], [(0, 6), (2, 5)], [(0, 5), (3, 2)]
            ],
            "Defensa Francesa": [
                [(1, 4), (3, 4)]
            ],
            "Defensa Alekhine": [
                [(1, 4), (3, 4)]
            ],
            "Defensa Escandinava": [
                [(1, 4), (3, 4)]
            ],
            "Ataque de Londres": [
                [(1, 3), (3, 3)], [(0, 2), (2, 4)]
            ],
            "Gambito de Rey": [
                [(1, 4), (3, 4)], [(1, 5), (3, 5)]
            ],
            "Gambito Letón": [
                [(1, 4), (3, 4)], [(0, 6), (2, 5)]
            ],
            "Apertura Inglesa": [
                [(1, 2), (3, 2)]
            ],
            "Apertura Reti": [
                [(0, 6), (2, 5)], [(1, 2), (3, 2)]
            ],
            "Gambito Evans": [
                [(1, 4), (3, 4)], [(0, 6), (2, 5)], [(0, 5), (4, 1)], [(1, 1), (3, 1)]
            ]
        }

        # Variables para rastrear el progreso de la apertura
        self.current_opening = None
        self.opening_progress = 0

    def get_move(self, game_state):
        """
        Devuelve un movimiento basado en aperturas predefinidas o uno aleatorio si no es posible.
        """
        valid_moves = game_state.get_valid_moves()

        if not valid_moves:
            print("No hay movimientos válidos disponibles para el bot.")
            return None

        # Continuar con la apertura seleccionada si es posible
        if self.current_opening is not None:
            opening_moves = self.predefined_moves[self.current_opening]
            if self.opening_progress < len(opening_moves):
                start_square, end_square = opening_moves[self.opening_progress]
                move_obj = Move(start_square, end_square, game_state.board)
                if move_obj in valid_moves:
                    self.opening_progress += 1
                    print(f"Movimiento de apertura {self.current_opening}: {move_obj}")
                    return move_obj
            else:
                # Finalizar la apertura si se completó
                print(f"Apertura {self.current_opening} completada.")
                self.current_opening = None

        # Seleccionar una nueva apertura si no hay una activa
        if self.current_opening is None:
            self.current_opening = random.choice(list(self.predefined_moves.keys()))
            self.opening_progress = 0
            print(f"Nueva apertura seleccionada: {self.current_opening}")

        # Intentar el primer movimiento de la nueva apertura
        opening_moves = self.predefined_moves[self.current_opening]
        for start_square, end_square in opening_moves:
            move_obj = Move(start_square, end_square, game_state.board)
            if move_obj in valid_moves:
                self.opening_progress += 1
                print(f"Primer movimiento de apertura {self.current_opening}: {move_obj}")
                return move_obj

        # Si no hay movimientos válidos en la apertura seleccionada, realizar un movimiento aleatorio
        print(f"No se encontraron movimientos válidos para la apertura {self.current_opening}.")
        random_move = random.choice(valid_moves)
        print(f"Movimiento aleatorio seleccionado: {random_move}")
        self.current_opening = None  # Reiniciar la apertura
        return random_move
    def best_move(self, game_state, valid_moves):
        """
        Devuelve el mejor movimiento utilizando el algoritmo Minimax con poda alfa-beta.
        :param game_state: Estado del juego actual
        :param valid_moves: Lista de movimientos válidos
        :return: Mejor movimiento calculado
        """
        best_move = None
        max_score = -float('inf')

        # Evaluar todos los movimientos válidos
        for move in valid_moves:
            game_state.make_move(move)
            score = self.minimax(game_state, self.MAX_DEPTH, -float('inf'), float('inf'), True)
            if score > max_score:
                max_score = score
                best_move = move
            game_state.undo_move()

        return best_move

    def minimax(self, game_state, depth, alpha, beta, maximizing_player):
        """
        Algoritmo Minimax con poda alfa-beta.
        :param game_state: Estado del juego
        :param depth: Profundidad de la búsqueda
        :param alpha: Valor alfa (mejor opción para el jugador maximizador)
        :param beta: Valor beta (mejor opción para el jugador minimizador)
        :param maximizing_player: Booleano que indica si el jugador actual es el maximizador
        :return: Valor evaluado del estado actual
        """
        if depth == 0 or game_state.checkmate or game_state.stalemate:
            return self.board_score(game_state)

        valid_moves = game_state.get_valid_moves()
        if maximizing_player:
            max_eval = -float('inf')
            for move in valid_moves:
                game_state.make_move(move)
                eval = self.minimax(game_state, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break  # Poda alfa
                game_state.undo_move()
            return max_eval
        else:
            min_eval = float('inf')
            for move in valid_moves:
                game_state.make_move(move)
                eval = self.minimax(game_state, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break  # Poda beta
                game_state.undo_move()
            return min_eval

    def board_score(self, game_state):
        """
        Calcula el puntaje del tablero para determinar qué tan favorable es para el bot.
        :param game_state: Estado actual del juego
        :return: Puntaje del tablero
        """
        if game_state.checkmate:
            if game_state.white_turn:
                return -self.CHECKMATE  # El bot pierde
            else:
                return self.CHECKMATE  # El bot gana
        elif game_state.stalemate:
            return self.STALEMATE

        score = 0
        for row in game_state.board:
            for sq in row:
                if sq != "--":
                    piece = sq[1]
                    score += self.piece_values.get(piece, 0)
        return score

    def convert_to_uci(self, move):
        """
        Convierte el movimiento en coordenadas (de tipo (start, end)) al formato UCI.
        :param move: Movimiento en formato (start, end) como tupla de coordenadas
        :return: Movimiento en formato UCI
        """
        start, end = move
        start_col = chr(start[1] + 97)  # Convertir columna a letra (ej. 0 -> 'a', 1 -> 'b', etc.)
        start_row = 8 - start[0]  # Convertir fila a notación de ajedrez
        end_col = chr(end[1] + 97)
        end_row = 8 - end[0]
        return f"{start_col}{start_row}{end_col}{end_row}"
