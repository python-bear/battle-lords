from bin.states.bc_state import State
from bin.states.start_menus import MainMenu
from bin.utils import painting as pt
import pygame


class TitleState(State):
    def __init__(self, game):
        super().__init__(game)

    def update(self, delta_time, events):
        for event in events:
            if event.type == pygame.KEYUP:
                new_state = MainMenu(self.game)
                new_state.enter_state()
        self.game.reset_keys()

    def render(self, window):
        window.draw_background()

        pt.draw_text(window.screen, "Battle-Lords", int(window.screen_width / 2),
                     int(window.screen_height / 2) - int(window.screen_height / 7.5),
                     int(window.screen_height / 2) + int(window.screen_height / 7.5),
                     self.game.y_scale, self.game.init_y_scale, center=True)

        # pt.draw_rectangle(window.screen, int(window.screen_width / 4),
        #                   int(window.screen_height / 2) - int(window.screen_height / 7.5), int(window.screen_width / 2),
        #                   int(window.screen_width / 2), (5, 215, 99))
        #
        # pt.draw_rectangle(window.screen, 100, 100, 300, 200, (100, 22, 237))
