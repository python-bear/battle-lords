from bin.states.bc_state import State
from bin.utils import painting as pt
from bin.networking import NetworkAgent
from bin.game.mobiles import *
import random
import pygame
import math


class Team:
    def __init__(self):
        pass


class OnlineGameState(State):
    def __init__(self, game):
        super().__init__(game)
        self.window_title = "Battle-Lords · Online Game"
        self.net = NetworkAgent()

        if self.net.id == "0":
            self.is_turn = True
            self.king1 = King(self.game.height // 2, 2, "#aa00bb", 'goop')
            self.king2 = King(self.game.height // 2, self.game.width - 3, "#00ccdd", 'goop')
        else:
            self.is_turn = False
            self.king2 = King(self.game.height // 2, 2, "#aa00bb", 'goop')
            self.king1 = King(self.game.height // 2, self.game.width - 3, "#00ccdd", 'goop')

        self.terrain = {
            "mountain": 0,
            "water": 1,
            "forest": 2,
            "plain": 3,
            "farmland": 4,
            "bridge": 5,
            "road": 6,
            "path": 7,
            "cottage": 8,
            "housing": 9,
            "wall": 10,
            "castle": 11,
        }
        self.terrain_colors = {
            0: "black",
            1: "light blue",
            2: "dark green",
            3: "light green",
            4: "yellow",
            5: "brown",
            6: "tan",
            7: "light gray",
            8: "red",
            9: "orange",
            10: "dark gray",
            11: "gold",
        }
        self.map = self.generate_map(self.game.height, self.game.width)
        self.map_dimension = [len(self.map[1]), len(self.map[1][0])]

    def update(self, delta_time, events):
        has_moved = False

        for event in events:
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN:
                    if event.key == pygame.K_RIGHT and self.is_turn:
                        self.king1.move([0, 1], self.map_dimension)
                        has_moved = True
                    elif event.key == pygame.K_LEFT and self.is_turn:
                        self.king1.move([0, -1], self.map_dimension)
                        has_moved = True
                    elif event.key == pygame.K_UP and self.is_turn:
                        self.king1.move([-1, 0], self.map_dimension)
                        has_moved = True
                    elif event.key == pygame.K_DOWN and self.is_turn:
                        self.king1.move([1, 0], self.map_dimension)
                        has_moved = True

        if has_moved:
            print('moved')
            self.is_turn = False
            msg_type = 21
        else:
            msg_type = 11

        # Networking
        data = self.send_data(msg_type)

        if data is not None:
            parsed_data = self.parse_data(int(data[1]), str(data[2]))
            if parsed_data is not None:
                if int(data[1]) == 21:
                    self.king2.x, self.king2.y = parsed_data[0], parsed_data[1]
                    self.is_turn = True

        self.game.reset_keys()

    def render(self, window):
        window.draw_background()
        self.draw_board(window.screen, self.map, self.game.x_scale, self.game.y_scale)
        self.king1.draw(window.screen, self.game.x_scale, self.game.y_scale)
        self.king2.draw(window.screen, self.game.x_scale, self.game.y_scale)
        if self.is_turn:
            pt.draw_text(window.screen, "It is your turn.", 2, 2, 20, self.game.y_scale, self.game.init_y_scale)
        else:
            pt.draw_text(window.screen, "It is your opponent\'s turn.", 2, 2, 20, self.game.y_scale,
                         self.game.init_y_scale)

    def send_data(self, msg_type: int) -> list:
        msg_body = ""
        if msg_type == 21:
            msg_body = f"{self.king1.x},{self.king1.y}"
        elif msg_type == 11:
            msg_body = f""
        reply = self.net.send(msg_type, msg_body)

        if not reply[0]:
            return reply[1]
        else:
            return None

    def generate_map(self, h: int = 16, w: int = 32) -> list:
        empty_map = [[[[] for width in range(w)] for height in range(h)],
                     [[-1 for width in range(w)] for height in range(h)]]

        new_map = [[[[] for width in range(w)] for height in range(h)],
                   [[-1 for width in range(w)] for height in range(h)]]

        for j in range(len(empty_map[1])):
            for i in range(len(empty_map[1][j])):
                if i in (0, w - 1):
                    if j == 7 or j == 8:
                        new_map[1][j][i] = self.terrain["castle"]
                    else:
                        n = random.randint(0, h - 1)
                        if n == 0:
                            new_map[1][j][i] = self.terrain["housing"]
                        else:
                            new_map[1][j][i] = self.terrain["path"]
                elif i in (1, 2, 3, 4, w - 2, w - 3, w - 4, w - 5):
                    top = h - (i if i <= 3 else (1 if i == w - 4 else (2 if i == w - 3 else 3)))
                    n = random.randint(0, top)
                    if n == 0:
                        new_map[1][j][i] = self.terrain["housing"]
                    else:
                        new_map[1][j][i] = self.terrain["path"]
                elif i in (5, w - 6):
                    n = random.randint(0, h)
                    if n in (0, 1):
                        new_map[1][j][i] = self.terrain["plain"]
                    elif n in (2, 3, 4, 5, 6, 7):
                        new_map[1][j][i] = self.terrain["path"]
                    elif n == 8:
                        new_map[1][j][i] = self.terrain["mountain"]
                    else:
                        new_map[1][j][i] = self.terrain["wall"]
                elif i in (5, 6, 7, 8, 9, 10, 11, w - 6, w - 7, w - 8, w - 9, w - 10, w - 11, w - 12):
                    n = random.randint(0, h)
                    if n == 0:
                        new_map[1][j][i] = self.terrain["cottage"]
                    elif 2 < n < (h - h // 2):
                        new_map[1][j][i] = self.terrain["farmland"]
                    else:
                        new_map[1][j][i] = self.terrain["plain"]
                elif i in (12, w - 13):
                    n = random.randint(0, 1)
                    if n == 0:
                        new_map[1][j][i] = self.terrain["plain"]
                    else:
                        new_map[1][j][i] = self.terrain["forest"]
                elif i in (13, 14, 15, w - 14, w - 15, w - 16):
                    n = random.randint(0, h)
                    if n in (0, 1):
                        new_map[1][j][i] = self.terrain["mountain"]
                    elif n in (2, 3):
                        new_map[1][j][i] = self.terrain["plain"]
                    else:
                        new_map[1][j][i] = self.terrain["forest"]

        return new_map

    def draw_board(self, surface, board_map, x_scale, y_scale):
        map_height = len(board_map[1])
        map_width = len(board_map[1][0])
        for j in range(map_height):
            for i in range(map_width):
                pygame.draw.rect(surface, self.terrain_colors[board_map[1][j][i]],
                                 [math.ceil(i * x_scale + x_scale), math.ceil(j * y_scale + y_scale),
                                  math.ceil(x_scale), math.ceil(y_scale)])

    @staticmethod
    def parse_data(msg_type: int, msg_body_data: str):
        try:
            if msg_type == 21:
                data = msg_body_data.split(",")
                return [int(data[0]), int(data[1])]
        except:
            return None
