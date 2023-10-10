import pygame


class Widget:
    def __init__(self, x: int, y: int, width: int, height: int, fg_cols: list = ((0, 0, 0),),
                 bg_cols: list = ((200, 200, 200), (255, 255, 255))):
        self.rect = pygame.Rect(x, y, width, height)
        self.fg_cols = fg_cols
        self.bg_cols = bg_cols

    def update(self, event, mouse_buttons: list, mouse_pos):
        pass

    def render(self, surface):
        pass


class Button(Widget):
    def __init__(self, x: int, y: int, width: int, height: int, text: str = None, image: pygame.Surface = None):
        super().__init__(x, y, width, height)
        self.text = text
        self.image = image

    def update(self, event, mouse_buttons: list, mouse_pos):
        # Implement button event handling logic here
        pass

    def render(self, surface):
        # Implement text entry drawing logic here
        pass


class TextEntry(Widget):
    def __init__(self, x: int, y: int, width: int, height: int):
        super().__init__(x, y, width, height)
        self.text = ""

    def update(self, event, mouse_buttons: list, mouse_pos):
        # Implement text entry event handling logic here
        pass

    def render(self, surface):
        # Implement text entry drawing logic here
        pass
