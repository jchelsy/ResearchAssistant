__all__ = ['asciiText', 'clear']

from os import system, name
from PIL import Image, ImageDraw, ImageFont
import numpy as np


def clear():
    # Windows
    if name == 'nt':
        _ = system('cls')
    # Mac and Linux (os.name is 'posix')
    else:
        _ = system('clear')


def asciiText(txt):
    myfont = ImageFont.truetype("verdanab.ttf", 12)
    size = myfont.getsize(txt)
    img = Image.new("1", size, "black")
    draw = ImageDraw.Draw(img)
    draw.text((0, 0), txt, "white", font=myfont)
    pixels = np.array(img, dtype=np.uint8)
    chars = np.array([' ', '#'], dtype="U1")[pixels]
    strings = chars.view('U' + str(chars.shape[1])).flatten()
    print("\n".join(strings))
