""" Rules at http://www.marksteeregames.com/Zola.pdf """
import math
from pathlib import Path
from turtle import Turtle

from cairosvg import svg2png
from matplotlib import pyplot as plt
from quarto.svg_turtle import SvgTurtle


class ZolaBoard:
    def __init__(self,
                 turtle: Turtle,
                 n: int,
                 board_size: float,
                 centre: float = None):
        self.turtle = turtle
        self.n = n
        self.centre = (n-1)/2 if centre is None else centre
        self.board_size = board_size
        schemes = [('magma', 0, 0.95),
                   ('viridis', 0, 0.92),
                   ('plasma', 0, 0.94),
                   ('inferno', 0, 1),
                   ('Pastel1', 0, 1)]
        map_name, self.min_colour, self.max_colour = schemes[0]
        self.cm = plt.get_cmap(map_name)

    def draw(self):
        t = self.turtle
        n = self.n
        max_distance = max(math.sqrt(2*(i-self.centre)**2) for i in range(n))
        square_size = self.board_size / n
        t.up()
        t.back((self.board_size-square_size)/2)
        t.right(90)
        t.back((self.board_size-square_size)/2)
        t.left(90)
        centre = self.centre
        for row in range(n):
            for column in range(n):
                is_light = (row + column) % 2
                distance = math.sqrt((row-centre)**2 + (column-centre)**2)

                level = distance / max_distance
                self.draw_space(square_size, level, is_light)
                t.up()
                t.forward(square_size)
            t.back(self.board_size)
            t.right(90)
            t.forward(square_size)
            t.left(90)
        t.left(90)
        t.forward(square_size/2)
        t.right(90)
        t.back(square_size/2)
        self.draw_lines(square_size)

    def draw_lines(self, square_size):
        t = self.turtle
        t.pensize(round(square_size*6 / 100))
        t.color('gray60')
        for _ in range(2):
            for _ in range(self.n + 1):
                t.down()
                t.forward(self.board_size)
                t.up()
                t.back(self.board_size)
                t.left(90)
                t.forward(square_size)
                t.right(90)
            t.right(90)
            t.forward(square_size)

    def draw_space(self, square_size, level, is_light):
        colour_point = (level *
                        (self.max_colour - self.min_colour) +
                        self.min_colour)
        colour = self.cm(colour_point)
        rgb_colour = colour[:3]
        if is_light:
            self.turtle.color('gray70')
        else:
            self.turtle.color('gray50')
        self.draw_square(square_size)
        self.turtle.fillcolor(rgb_colour)
        self.draw_square(square_size * 0.7)

    def draw_square(self, size: float):
        t = self.turtle
        t.up()
        t.back(size/2)
        t.left(90)
        t.forward(size/2)
        t.right(90)
        t.down()
        t.begin_fill()
        for _ in range(4):
            t.forward(size)
            t.right(90)
        t.end_fill()
        t.up()
        t.forward(size/2)
        t.right(90)
        t.forward(size/2)
        t.left(90)


def demo():
    t = Turtle()
    screen = t.getscreen()
    screen_size = min(screen.window_width(), screen.window_height())
    board = ZolaBoard(t, 2, 0.5*screen_size, -0.5)
    board.draw()


def main():
    output_path = Path(__file__).parent
    board_path = output_path / 'zola_board.svg'
    size = 170
    turtle = SvgTurtle.create("172px", "172px")
    # noinspection PyTypeChecker
    board = ZolaBoard(turtle, 6, size)
    board.draw()
    turtle.save_as(board_path)

    icon_svg_path = output_path / 'zola_icon.svg'
    icon_png_path = output_path / 'zola_icon.png'
    size = 30
    turtle = SvgTurtle.create("32px", "32px")
    # noinspection PyTypeChecker
    board = ZolaBoard(turtle, 2, size, -0.5)
    board.draw()
    turtle.save_as(icon_svg_path)
    svg2png(icon_svg_path.read_text(), write_to=str(icon_png_path))


if __name__ == '__main__':
    main()
elif __name__ == '__live_coding__':
    demo()
