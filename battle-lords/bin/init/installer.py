import pygame
import pickle
import os
import sys
from scipy.stats import linregress


def install():
    pygame.font.init()
    cwd = os.getcwd()

    if not os.path.exists(os.path.join(cwd, "var", "font_equations.pkl")):
        handle_fonts(["magicmedieval", "couriernew"], cwd)

    if not os.path.exists(os.path.join(cwd, "var", "os_info.pkl")):
        save_os_info(cwd)


def handle_fonts(font_list, cwd):
    font_equations = {font: None for font in font_list}
    font_tables = {font: [[], []] for font in font_list}

    for n in range(0, 1001):
        for font in font_list:
            font_tables[font][0].append(n)
            font_tables[font][1].append(pygame.font.SysFont(font, n).get_height())

    for font in font_list:
        slope, intercept, r_value, p_value, std_err = linregress(font_tables[font][0], font_tables[font][1])
        font_equations[font] = {"slope": float(slope), "intercept": float(intercept)}

    with open(os.path.join(cwd, "var", "font_equations.pkl"), "wb") as file:
        pickle.dump(font_equations, file)


def save_os_info(cwd: str = None):
    operating_sys = "Unknown"
    if sys.platform.startswith("win") or sys.platform.startswith("cygwin") or sys.platform.startswith("msys"):
        operating_sys = "windows"
    elif sys.platform.startswith("darwin"):
        operating_sys = "mac"
    elif sys.platform.startswith("linux"):
        operating_sys = "linux"
    elif sys.platform.startswith("os2"):
        operating_sys = "os2"
    elif sys.platform.startswith("freebsd"):
        operating_sys = "freebsd"
    elif sys.platform.startswith("atheos"):
        operating_sys = "atheos"
    elif sys.platform.startswith("riscos"):
        operating_sys = "riscos"

    username = "Unknown"
    if operating_sys == "windows":
        username = os.environ.get("USERNAME")
    elif operating_sys in ("linux", "os2", "mac"):
        username = os.environ.get("USER")

    if cwd is not None:
        with open(os.path.join(cwd, "var", "os_info.pkl"), "wb") as file:
            pickle.dump([operating_sys, username], file)

    else:
        return [operating_sys, username]
