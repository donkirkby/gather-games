""" Connect three of your pieces while building the board.

Rules at https://www.archive.org/stream/youngfolkscyclop00chamiala#page/540/mode/2up
"""
import typing
from pathlib import Path
from turtle import Turtle

from cairosvg import svg2png
from matplotlib import pyplot as plt

from quarto.svg_turtle import SvgTurtle


class PlankSet:
    def __init__(self, turtle: typing.Union[Turtle, SvgTurtle], size: float):
        """ Initialize the object.

        :param turtle: used to draw the pieces
        :param size: size of a space on each plank
        """
        self.turtle = turtle
        self.size = size
        cm = plt.get_cmap('Paired', 12)
        self.plank_colours = tuple(cm(i/12)[:3] for i in range(0, 6, 2))
        self.piece_colours = tuple(cm(i/12)[:3] for i in range(1, 7, 2))

    def draw_plank(self, colour_num: int):
        t = self.turtle
        t.pensize(max(1, round(self.size/50)))
        colours1 = list(self.plank_colours)
        colour1 = colours1.pop(colour_num)
        colours1.insert(1, colour1)
        colours = colours1
        t.up()
        t.back(self.size*1.5)
        t.left(90)
        t.forward(self.size/2)
        t.right(90)
        for colour in colours:
            t.down()
            t.fillcolor(colour)
            t.begin_fill()
            for _ in range(4):
                t.forward(self.size)
                t.right(90)
            t.end_fill()
            t.up()
            t.forward(self.size)
        t.back(self.size*1.5)
        t.right(90)
        t.forward(self.size/2)
        t.left(90)

    def draw_piece(self, colour_num: int, side_count: int = None):
        t = self.turtle
        t.right(90)
        t.fillcolor(self.piece_colours[colour_num])
        radius = self.size * 0.4
        t.forward(radius)
        t.left(90)
        if side_count:
            t.circle(radius, 360/side_count/2)
        t.down()
        t.begin_fill()
        t.circle(radius, steps=side_count)
        t.end_fill()
        t.up()
        if side_count:
            t.circle(radius, -360/side_count/2)
        t.left(90)
        t.forward(radius)
        t.right(90)

    def draw_icon(self):
        t = self.turtle
        t.up()
        t.left(90)
        t.forward(self.size)
        t.right(90)
        pieces = [[0, 4, 0],
                  [6, 4, 6],
                  [0, 4, 0]]
        for colour_num, plank_pieces in enumerate(pieces):
            self.draw_plank(colour_num)
            t.back(self.size)
            colours = list(range(3))
            colour = colours.pop(colour_num)
            colours.insert(1, colour)
            for side_count, piece_colour_num in zip(plank_pieces, colours):
                if side_count:
                    self.draw_piece(piece_colour_num, side_count)
                t.forward(self.size)
            t.back(self.size*2)
            t.right(90)
            t.forward(self.size*1.05)
            t.left(90)
        pass


def demo():
    t = Turtle()
    screen = t.getscreen()
    screen_size = min(screen.window_width(), screen.window_height())
    space_size = screen_size / 10
    plank_set = PlankSet(t, space_size)
    plank_set.draw_plank(colour_num=0)
    plank_set.draw_piece(colour_num=0, side_count=6)
    t.right(90)
    t.forward(space_size*1.05)
    t.left(90)
    plank_set.draw_plank(colour_num=1)
    plank_set.draw_piece(colour_num=1)
    t.right(90)
    t.forward(space_size*2.2)
    t.left(90)
    plank_set.draw_icon()
    t.stamp()


def main():
    output_path = Path(__file__).parent
    size = 300
    space_size = size * 0.95 / 3
    colour_names = 'bgr'
    for colour_num, colour_name in enumerate(colour_names):
        plank_path = output_path / f'plank_{colour_name}.svg'
        turtle = SvgTurtle.create("100px", "300px")
        board = PlankSet(turtle, space_size)
        turtle.right(90)
        board.draw_plank(colour_num)
        turtle.save_as(plank_path)

        for side_count in (3, 4, 6, None):
            piece_name = side_count or 'c'
            piece_path = output_path / f'piece_{colour_name}_{piece_name}.svg'
            turtle = SvgTurtle.create("100px", "100px")
            turtle.up()
            board = PlankSet(turtle, space_size)
            board.draw_piece(colour_num, side_count)
            turtle.save_as(piece_path)

    icon_svg_path = output_path / 'plank_icon.svg'
    icon_png_path = output_path / 'plank_icon.png'
    turtle = SvgTurtle.create("32px", "32px")
    board = PlankSet(turtle, 10)
    board.draw_icon()
    turtle.save_as(icon_svg_path)
    svg2png(icon_svg_path.read_text(), write_to=str(icon_png_path))


if __name__ == '__main__':
    main()
elif __name__ == '__live_coding__':
    demo()
