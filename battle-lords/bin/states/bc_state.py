class State:
    def __init__(self, game):
        self.game = game
        self.prev_state = None
        self.window_title = "Battle-Lords"

    def update(self, delta_time, events):
        pass

    def render(self, window):
        pass

    def enter_state(self):
        if len(self.game.state_stack) > 1:
            self.prev_state = self.game.state_stack[-1]

        self.game.window.reconfigure_window(caption=self.window_title)
        self.game.state_stack.append(self)

    def exit_state(self):
        self.game.state_stack.pop()
