from bin.utils import painting as pt
import pygame
import os


class Cursor(pygame.sprite.Sprite):
    def __init__(self, update_speed: list):
        super().__init__()
        pygame.mouse.set_visible(False)

        self.sprite_index = 0
        self.sprites = {
            "load": [],
            "normal": [],
            "glove": []
        }
        self.update_speed = update_speed
        self.last_time = 0
        self.state = "normal"
        self.click_sounds = [pygame.mixer.Sound(os.path.join(os.getcwd(), "lib", "sfx", f"click_{i}.wav"))
                             for i in range(3)]

        self.cursor_img_dir = os.path.join(os.getcwd(), "lib", "imgs", "cursor")
        for key in self.sprites.keys():
            for i in range(len([name for name in os.listdir(os.path.join(self.cursor_img_dir, key))
                                if os.path.isfile(os.path.join(self.cursor_img_dir, key, name))])):
                self.sprites[key].append(pt.load_img(os.path.join(self.cursor_img_dir, key, f"{i}.png")))
        self.rect = self.sprites[self.state][self.sprite_index].get_rect()

    def increment_sprite(self, delta_time):
        self.last_time += delta_time

        if self.state == "load":
            if self.last_time >= self.update_speed[0]:
                self.sprite_index += 1

                if self.sprite_index >= len(self.sprites[self.state]):
                    self.sprite_index = 0

                self.last_time = 0

        else:
            if self.last_time >= self.update_speed[1]:
                self.sprite_index = 0
                self.last_time = 0

    def change_state(self, state: str = "normal", index: int = 0):
        self.sprite_index = 0
        self.last_time = 0
        self.last_time = index
        self.state = state

    def update(self, mouse_buttons: list, mouse_pos, delta_time):
        if mouse_buttons[0]:  # left
            self.click_sounds[0].play()
            if self.state == "normal":
                self.sprite_index = 1
        if mouse_buttons[1]:  # middle
            self.click_sounds[1].play()
            if self.state == "normal":
                self.sprite_index = 2
        if mouse_buttons[2]:  # right
            self.click_sounds[2].play()
            if self.state == "normal":
                self.sprite_index = 3

        if self.state == "load":
            self.rect.center = mouse_pos
        elif self.state == "normal":
            self.rect.topleft = mouse_pos
        elif self.state == "glove":
            self.rect.topleft = [mouse_pos[0] - 2, mouse_pos[1] - 9]

        self.increment_sprite(delta_time)

    def render(self, surface):
        surface.blit(self.sprites[self.state][self.sprite_index], (self.rect.x, self.rect.y))
