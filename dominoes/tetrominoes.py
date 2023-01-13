from PIL import Image, ImageDraw
from space_tracer import LivePillowImage


def draw_tetromino(letter: str, colour: str) -> Image.Image:
    shapes = """
            OO
            OO
            IIII
             SS
            SS
            ZZ
             ZZ
            LLL
            L
            J
            JJJ
            TTT
             T
        """
    shape_lines = shapes.splitlines()
    coordinates = [(i, j)
                   for i, line in enumerate(shape_lines)
                   for j, c in enumerate(line)
                   if c == letter]
    min_i = min(i for i, j in coordinates)
    min_j = min(j for i, j in coordinates)
    normal_coordinates = [(i-min_i, j-min_j) for i, j in coordinates]
    square_size = 40
    image = Image.new('RGBA', (square_size*4, square_size*2))
    draw = ImageDraw.ImageDraw(image)
    for i, j in normal_coordinates:
        draw.rectangle((j*square_size, i*square_size,
                        (j+1)*square_size, (i+1)*square_size),
                       fill=colour)
    return image


def demo() -> None:
    image = draw_tetromino('I', 'cornsilk')
    live_image = LivePillowImage(image)
    live_image.display()


if __name__ == '__live_coding__':
    demo()
