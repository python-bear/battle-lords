import pygame
import math


class Mobile:
    def __init__(self, start_x: int, start_y: int, team: str, image_path: str, movement_pattern: list = (),
                 attack_pattern: list = (), jump_pattern: list = ()):
        self.x = start_x
        self.y = start_y
        self.team = team
        self.image = image_path
        self.movement_pattern = movement_pattern  # [[1, 0], [1, 1], [0, 1], [0, 0]]
        self.attack_pattern = attack_pattern
        self.jump_pattern = jump_pattern

    def draw(self, g, x_scale, y_scale):
        pygame.draw.rect(g, self.team, (math.ceil(self.y * x_scale + x_scale + (x_scale / 4)),
                                        math.ceil(self.x * y_scale + y_scale + (y_scale / 4)),
                                        math.ceil(x_scale / 2), math.ceil(y_scale / 2)), 0)

    def move(self, movement: list, map_dimension: list) -> None:
        if not 0 <= (self.x + movement[0]) <= (map_dimension[0] - 1) or \
                not 0 <= (self.y + movement[1]) <= (map_dimension[1] - 1):
            pass

        else:
            self.x, self.y = (self.x + movement[0]), (self.y + movement[1])


class King(Mobile):
    def __init__(self, start_x: int, start_y: int, team: str, image_path: str):
        movement = [[1, -1], [1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0], [0, -1], [-1, -1]]
        super().__init__(start_x, start_y, team, image_path, movement, movement)