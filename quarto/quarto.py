from pathlib import Path
from turtle import Turtle

from cairosvg import svg2png
from svg_turtle import SvgTurtle


def draw_piece(turtle: Turtle,
               size: float,
               is_big: bool,
               is_dark: bool,
               is_hollow: bool,
               is_square: bool):
    if not is_big:
        turtle.up()
        size /= 2
        turtle.forward(size/2)
        turtle.right(90)
        turtle.forward(size/2)
        turtle.left(90)
    turtle.down()
    turtle.color('black')
    if is_dark:
        turtle.fillcolor('chocolate')
    else:
        turtle.fillcolor('tan')
    pen_size = max(int(size / 31), 1)
    turtle.pensize(pen_size)
    if is_square:
        turtle.begin_fill()
        for _ in range(4):
            turtle.forward(size)
            turtle.right(90)
        turtle.end_fill()
    else:
        turtle.up()
        turtle.forward(size/2)
        turtle.down()
        turtle.begin_fill()
        turtle.circle(-size/2)
        turtle.end_fill()
        turtle.up()
        turtle.back(size/2)
    if is_hollow:
        turtle.up()
        turtle.forward(size/2)
        turtle.right(90)
        turtle.forward(size/4)
        turtle.left(90)
        turtle.down()
        turtle.begin_fill()
        turtle.color('black')
        turtle.circle(-size/4)
        turtle.end_fill()
        turtle.up()
        turtle.back(size/2)
        turtle.right(90)
        turtle.back(size/4)
        turtle.left(90)


def draw_board(turtle: Turtle, size: float):
    turtle.up()
    turtle.back(size/2)
    turtle.right(90)
    turtle.back(size/2)
    turtle.left(90)
    turtle.forward(size/40)
    turtle.down()

    turtle.color('black', 'cornsilk')
    turtle.pensize(int(size/100))
    turtle.begin_fill()
    for _ in range(4):
        turtle.forward(size * 38/40)
        turtle.circle(-size/40, 90)
    turtle.end_fill()
    turtle.up()
    turtle.back(size/40)
    draw_dividers(turtle, size)

    turtle.forward(size/4)
    turtle.right(90)
    draw_dividers(turtle, size)
    turtle.right(90)
    turtle.forward(size)
    turtle.right(90)
    turtle.forward(size)
    turtle.right(90)


def draw_dividers(turtle, size):
    for _ in range(3):
        turtle.forward(size / 4)
        turtle.right(90)
        turtle.down()
        turtle.forward(size)
        turtle.up()
        turtle.back(size)
        turtle.left(90)


def generate_flags():
    for i in range(16):
        bit_string = bin(16+i)[3:]
        params = [c == '1' for c in bit_string]
        yield bit_string, params


def draw_icon(turtle: Turtle, size: float):
    turtle.up()
    turtle.back(size/2)
    turtle.right(90)
    turtle.back(size/2)
    turtle.left(90)
    draw_piece(turtle, size/2.1, True, True, True, True)
    turtle.up()
    turtle.forward(size/2)
    draw_piece(turtle, size/2.1, True, False, False, False)
    turtle.up()
    turtle.back(size/2)
    turtle.right(90)
    turtle.forward(size/2)
    turtle.left(90)
    draw_piece(turtle, size/2.1, True, True, False, False)
    turtle.up()
    turtle.forward(size/2)
    draw_piece(turtle, size/2.1, True, False, True, True)


def demo():
    turtle = Turtle()
    screen = turtle.getscreen()
    size = min(screen.window_width(), screen.window_height())
    size *= 0.95
    draw_board(turtle, size)
    for i, (name, flags) in enumerate(generate_flags()):
        row = i // 4
        column = i % 4
        turtle.up()
        turtle.goto(size*(column-2)/4, size*(row-1)/4)
        turtle.forward(size/32)
        turtle.right(90)
        turtle.forward(size/32)
        turtle.left(90)
        # turtle.stamp()
        draw_piece(turtle, size*3/16, *flags)


def main():
    output_path = Path(__file__).parent
    for name, flags in generate_flags():
        file_name = f'quarto{name}.svg'
        file_path = output_path / file_name
        size = 62
        turtle = SvgTurtle.create("64px", "64px")
        turtle.up()
        turtle.back(size/2)
        turtle.right(90)
        turtle.back(size/2)
        turtle.left(90)
        # noinspection PyTypeChecker
        draw_piece(turtle, size, *flags)
        turtle.save_as(file_path)

    board_path = output_path / 'quarto_board.svg'
    size = 170
    turtle = SvgTurtle.create("172px", "172px")
    # noinspection PyTypeChecker
    draw_board(turtle, size)
    turtle.save_as(board_path)

    icon_svg_path = output_path / 'quarto_icon.svg'
    icon_png_path = output_path / 'quarto_icon.png'
    size = 30
    turtle = SvgTurtle.create("32px", "32px")
    # noinspection PyTypeChecker
    draw_icon(turtle, size)
    turtle.save_as(icon_svg_path)
    svg2png(icon_svg_path.read_text(), write_to=str(icon_png_path))


if __name__ == '__main__':
    main()
else:
    demo()
