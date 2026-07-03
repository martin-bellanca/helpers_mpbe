from kivy.utils import rgba
from kivy.utils import get_hex_from_color

def rgba_to_hex(rgba_color):
    # Asegurarnos de que los valores RGBA estén entre 0 y 1
    r, g, b, a = rgba_color
    r = int(r * 255)
    g = int(g * 255)
    b = int(b * 255)
    # Omitimos 'a' para que sea un código hexadecimal de 6 dígitos (RGB)
    return f'#{r:02x}{g:02x}{b:02x}'


def rgba_to_hex_with_alpha(rgba_color):
    r, g, b, a = rgba_color
    r = int(r * 255)
    g = int(g * 255)
    b = int(b * 255)
    a = int(a * 255)
    return f'#{r:02x}{g:02x}{b:02x}{a:02x}'
