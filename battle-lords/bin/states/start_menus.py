from bin.states.bc_state import State
from bin.states.online_game import OnlineGameState
from bin.utils import painting as pt
import pygame


class MainMenu(State):
    def __init__(self, game):
        super().__init__(game)
        self.window_title = "Battle-Lords · main menu"

    def update(self, delta_time, events):
        for event in events:
            if event.type == pygame.KEYUP:
                new_state = OnlineGameState(self.game)
                new_state.enter_state()
        self.game.reset_keys()

    def render(self, surface):
        surface.draw_background()
        pt.draw_text(surface.screen, "Main Menu", int(surface.screen_width / 2),
                     int(surface.screen_height / 5) - int(surface.screen_height / 7.5),
                     int(surface.screen_height / 4) + int(surface.screen_height / 7.5),
                     self.game.y_scale, self.game.init_y_scale, center=True)
