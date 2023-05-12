""" Rules at http://www.marksteeregames.com/Monkey_Queen_rules.html """
import typing
from math import sqrt, ceil
from pathlib import Path
from turtle import Turtle

from cairosvg import svg2png
from quarto.svg_turtle import SvgTurtle


class HanoiBoard:
    def __init__(self,
                 turtle: typing.Union[Turtle, SvgTurtle],
                 n: int,
                 board_size: float):
        self.turtle = turtle
        self.n = n
        self.board_size = board_size
        self.radius = board_size / n / sqrt(3)

    def draw(self):
        t = self.turtle
        n = self.n
        radius = self.radius
        t.pensize(ceil(radius / 20))
        t.up()
        t.back(round(self.board_size / 2) - radius*sqrt(3)/2)
        t.right(90)
        t.back(radius*(3*n-5)/2)
        t.left(90)
        for row in range(2*n - 1):
            column_count = n + row
            if row >= n:
                offset = (row - n + 1)*2
                column_count -= offset
                t.forward(radius*sqrt(3))
            for column in range(column_count):
                t.down()
                t.fillcolor('antique white')
                t.begin_fill()
                t.circle(radius, steps=6)
                t.end_fill()
                t.up()
                t.forward(radius*sqrt(3))
            t.back(radius*sqrt(3)*column_count)
            t.right(120)
            t.forward(radius*sqrt(3))
            t.left(120)
        t.left(90)
        t.forward(radius/2)
        t.right(90)
        t.back(radius/2)
        t.home()


class HanoiPiece:
    def __init__(self,
                 t: typing.Union[Turtle, SvgTurtle],
                 colour: str,
                 size: int = 1,
                 scale: int = 100):
        self.t = t
        self.colour = colour
        self.size = size
        self.scale = scale

    def draw(self):
        t = self.t
        for i in range(self.size, 0, -1):
            if i == self.size:
                edge = 0.3
            else:
                edge = 0.1
            t.color('black')
            t.dot(i * self.scale)
            t.color(self.colour)
            t.dot(round((i - edge) * self.scale))


def demo():
    t = Turtle()
    screen = t.getscreen()
    screen_size = min(screen.window_width(), screen.window_height())
    # screen_size = 32
    board = HanoiBoard(t, 4, 0.55 * screen_size)
    board.draw()
    scale = round(board.radius / 4)
    piece = HanoiPiece(t, 'cornflower blue', size=5, scale=scale)
    piece.draw()
    t.forward(board.radius * sqrt(3))
    piece = HanoiPiece(t, 'cornflower blue', size=4, scale=scale)
    piece.draw()
    t.forward(board.radius * sqrt(3))
    piece = HanoiPiece(t, 'ivory', size=3, scale=scale)
    piece.draw()


def main():
    output_path = Path(__file__).parent
    board_path = output_path / 'hanoi_board.svg'
    size = 170
    turtle = SvgTurtle.create("172px", "172px")
    board = HanoiBoard(turtle, 3, 0.55 * size)
    board.draw()
    turtle.save_as(board_path)

    for colour, suffix in (('cornflower blue', 'b'), ('ivory', 'w')):
        for rank in range(1, 6):
            turtle = SvgTurtle.create("500px", "500px")
            size = 500
            piece_path = output_path / f'hanoi_piece_{suffix}{rank}.svg'
            piece = HanoiPiece(turtle, colour, rank, round(size/6))
            piece.draw()
            turtle.save_as(piece_path)

    icon_svg_path = output_path / 'hanoi_icon.svg'
    icon_png_path = output_path / 'hanoi_icon.png'
    size = round(32*0.6)
    turtle = SvgTurtle.create("32px", "32px")
    board = HanoiBoard(turtle, 2, size)
    board.draw()
    scale = round(board.radius / 4)
    piece = HanoiPiece(turtle, 'cornflower blue', size=2, scale=scale)
    piece.draw()
    turtle.forward(board.radius * sqrt(3))
    piece = HanoiPiece(turtle, 'ivory', size=3, scale=scale)
    piece.draw()
    turtle.save_as(icon_svg_path)
    svg2png(icon_svg_path.read_text(), write_to=str(icon_png_path))


if __name__ == '__main__':
    main()
elif __name__ == '__live_coding__':
    demo()
