import pygame
import pickle
import os
import math


with open(os.path.join(os.getcwd(), "var", "font_equations.pkl"), "rb") as file:
    font_equations = pickle.load(file)


def draw_text(surface, text: str, x: int, y: int, bottom_y: int, y_scale: float, init_y_scale: int,
              color: list = (255, 0, 0), width_scaling: int = 1, height_scaling: int = 1,
              font_name: str = "magicmedieval", center: bool = False):
    do_return = False
    lines = text.split("\n")
    y_offset = 0

    if center:
        font_size = get_font_size(int((bottom_y - y) / len(lines)), font_name)
    else:
        font_size = get_font_size(int(bottom_y * (y_scale / (init_y_scale / 2)) / len(lines) - y / len(lines)),
                                  font_name)
    font_obj = pygame.font.SysFont(font_name, font_size)

    for line in lines:
        if center:
            render = font_obj.render(line, True, color)
            scaled_render = pygame.transform.scale(render, (int(render.get_width() * width_scaling),
                                                            int(render.get_height() * height_scaling)))
            render_rect = scaled_render.get_rect()
            render_rect.center = (x, y + y_offset + (bottom_y / len(lines) - y / len(lines)) // 2)

            if surface is None and do_return is not True:
                do_return = True
                surface = pygame.Surface((render_rect.width, len(lines) * font_size), pygame.SRCALPHA)
                surface.fill((0, 0, 0, 0))

            surface.blit(scaled_render, render_rect)

        else:
            render = font_obj.render(line, True, color)
            scaled_render = pygame.transform.scale(render, (int(render.get_width() * width_scaling),
                                                            int(render.get_height() * height_scaling)))
            render_rect = scaled_render.get_rect()

            if surface is None and do_return is not True:
                do_return = True
                surface = pygame.Surface((render_rect.width, len(lines) * font_size), pygame.SRCALPHA)
                surface.fill((0, 0, 0, 0))

            surface.blit(scaled_render, render_rect)

        y_offset += font_size

    if do_return:
        return surface


def get_font_size(height: int, font_name: str) -> int:
    global font_equations
    return int(math.floor((height - font_equations[font_name]["slope"]) / font_equations[font_name]["slope"]))


def load_img(image_path: str, allow_alpha: bool = False) -> pygame.Surface:
    if allow_alpha:
        return pygame.image.load(image_path).convert()

    else:
        return pygame.image.load(image_path).convert_alpha()


def scale_image(image: pygame.Surface, scale: int = 2) -> pygame.Surface:
    dimensions = (image.get_width() * scale, image.get_height() * scale)

    scaled_image = pygame.transform.scale(image, dimensions)
    return scaled_image


def draw_rectangle(surface, x: int, y: int, width: int, height: int, color: tuple):
    pygame.draw.rect(surface, color, (x, y, width, height))


def draw_circle(surface, x: int, y: int, radius: int, color: tuple):
    pygame.draw.circle(surface, color, (x, y), radius)
