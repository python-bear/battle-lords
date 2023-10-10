import pygame
import time
from bin.states.title import TitleState
from bin.gui import *


class Application:
    def __init__(self, w: int = 32, h: int = 16, scale: int = 40):
        pygame.init()

        self.run_application = True
        self.dt = 0
        self.prev_time = 0
        self.abs_time = 0
        self.state_stack = []
        self.max_frame_rate = 60
        self.init_x_scale = scale
        self.init_y_scale = scale
        self.x_scale = scale
        self.y_scale = scale
        self.width = w
        self.height = h
        self.actions = None
        self.mouse_buttons_pressed = [0, 0, 0]
        self.mouse_position = [0, 0]
        self.window = Window(w * scale + 2 * scale, h * scale + 2 * scale, "Battle-Lords")
        self.cursor = Cursor([0.05, 0.4])

        self.title_screen = TitleState(self)
        self.state_stack.append(self.title_screen)

    def run(self):
        clock = pygame.time.Clock()

        while self.run_application:
            clock.tick(self.max_frame_rate)
            self.get_dt()
            self.handle_events()
            self.update()
            self.render()

        pygame.quit()

    def get_dt(self):
        current_time = time.time()
        self.dt = current_time - self.prev_time
        self.prev_time = current_time
        self.abs_time += self.dt

    def update(self):
        self.state_stack[-1].update(self.dt, self.actions)
        self.cursor.update(self.mouse_buttons_pressed, self.mouse_position, self.dt)

    def render(self):
        self.state_stack[-1].render(self.window)
        self.cursor.render(self.window.screen)
        # self.window.screen.blit(self.window.canvas, (0, 0))
        pygame.display.flip()

    def handle_events(self):
        self.actions = pygame.event.get()
        self.mouse_buttons_pressed = (0, 0, 0)

        for event in self.actions:
            if event.type == pygame.QUIT:
                self.run_application = False

            elif event.type == pygame.K_ESCAPE:
                self.run_application = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_buttons_pressed = pygame.mouse.get_pressed()

            elif event.type == pygame.VIDEORESIZE:
                new_width = 500 if event.w < 500 else event.w
                new_height = 250 if event.h < 250 else event.h
                self.x_scale *= new_width / self.window.screen_width
                self.y_scale *= new_height / self.window.screen_height
                self.window.reconfigure_window(new_width, new_height)
                # self.window.canvas_width, self.window.canvas_height = event.w, event.h

        self.mouse_position = pygame.mouse.get_pos()

    def reset_keys(self):
        self.actions = []


class Window:
    def __init__(self, w: int, h: int, name: str = "Battle-Lords"):
        self.screen_width = w
        self.screen_height = h
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RESIZABLE)

        # self.canvas_width = w
        # self.canvas_height = h
        # self.canvas = pygame.Surface((self.screen_width, self.screen_height))

        pygame.display.set_caption(name)
        pygame.font.init()

    def reconfigure_window(self, new_width: int = None, new_height: int = None, caption: str = None,
                           icon: pygame.surface = None):
        if new_width is not None:
            self.screen_width = new_width
        if new_height is not None:
            self.screen_height = new_height
        if new_width is not None or new_height is not None:
            self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RESIZABLE)
        if caption is not None:
            pygame.display.set_caption(caption)
        if icon is not None:
            pygame.display.set_icon(icon)

    def draw_background(self, color: tuple = (255, 255, 255)):
        self.screen.fill(color)
