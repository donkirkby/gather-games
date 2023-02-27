import typing
from itertools import product
from json import loads, dumps
from math import cos, sin, pi, sqrt
from pathlib import Path
from zipfile import ZipFile

from PIL import Image, ImageDraw, ImageColor
from PIL.ImageDraw import floodfill
from space_tracer import LivePillowImage

# {code: (colour, size)}
OPTIONS = {'A': ('red', 0),
           'a': ('red', -1),
           'e': ('red', -2),
           'B': ('blue', 0),
           'b': ('blue', -1),
           'c': ('blue', -2),
           'X': ('grey', 0),
           'x': ('grey', -1),
           'y': ('grey', -2)}


class SpinDraw:
    def __init__(self, r: float):
        r *= 2
        self.r = r
        self.line_width = round(r * 0.02)
        width = round(r * 2)
        height = round(2 * r * sin(pi / 3))
        self.image = Image.new('RGBA', (width, height))
        self.draw = ImageDraw.Draw(self.image)
        self.cx = width / 2
        self.cy = height / 2
        self.angle = 0
        self.draw.regular_polygon((width/2, height/2, r),
                                  6,
                                  fill='black')
        self.draw.regular_polygon((width/2, height/2, r - self.line_width),
                                  6,
                                  fill='white')

    def spin(self, angle):
        self.angle += angle

    def transform(self, x, y):
        theta = self.angle * pi / 180

        return x*cos(theta) - y*sin(theta), x*sin(theta) + y*cos(theta)

    def arc(self, size: int = 0):
        r = (3+size)*self.r/6
        x, y = self.transform(self.r, 0)
        x += self.cx
        y += self.cy

        self.draw.arc(((x - r, y - r),
                       (x + r, y + r)),
                      120 + self.angle,
                      240 + self.angle,
                      fill='black',
                      width=self.line_width)

    def line(self, offset: int = 0):
        self.spin(-30)
        x1, y1 = self.transform(-self.r*sqrt(3)/2, -self.r*offset/10)
        x2, y2 = self.transform(self.r*sqrt(3)/2, -self.r*offset/10)
        self.spin(30)
        self.draw.line(((self.cx + x1, self.cy + y1),
                        (self.cx + x2, self.cy + y2)),
                       fill='black',
                       width=self.line_width)

    def fill(self, colour_name):
        x, y = self.transform(self.r*8/9, 0)

        fill = ImageColor.getcolor(colour_name, 'RGBA')
        floodfill(self.image, (self.cx + x, self.cy + y), fill)

    def resize(self):
        image = self.image
        return image.resize((image.width // 2, image.height // 2),
                            Image.LANCZOS)


def build_back(r: float) -> Image.Image:
    colour, _ = OPTIONS['X']
    spin_draw = SpinDraw(r)
    spin_draw.fill(colour)
    for code in 'ABABAB':
        colour, _ = OPTIONS[code]

        spin_draw.arc()
        spin_draw.fill(colour)
        spin_draw.spin(60)

    return spin_draw.resize()


def build_tile(points: str, r: float) -> Image.Image:
    spin_draw = SpinDraw(r)
    sizes = [OPTIONS[point][1] for point in points]
    if points[0] != points[1]:
        spin_draw.arc(sizes[0])
        if points[1] != points[2]:
            spin_draw.spin(120)
            spin_draw.arc(sizes[1])
            spin_draw.spin(120)
            spin_draw.arc(sizes[2])
            spin_draw.spin(120)
        else:
            spin_draw.spin(120)
            spin_draw.line(sizes[1])
            spin_draw.spin(60)
            spin_draw.arc(-sizes[1])
            spin_draw.spin(-180)
    else:
        spin_draw.spin(60)
        spin_draw.arc(-sizes[0])
        spin_draw.spin((-60))
        if points[0] != points[2]:
            spin_draw.line(sizes[0])
            spin_draw.spin(-120)
            spin_draw.arc(sizes[2])
            spin_draw.spin(120)
        else:
            spin_draw.spin(180)
            spin_draw.arc(-sizes[0])
            spin_draw.spin(120)
            spin_draw.arc(-sizes[0])
            spin_draw.spin(60)

    for point in points:
        colour, size = OPTIONS[point]
        spin_draw.fill(colour)
        spin_draw.spin(120)

    return spin_draw.resize()


def generate_combinations(colours: str) -> typing.List[str]:
    combinations = set()
    for combo in product(colours, repeat=3):
        double_combo = ''.join(combo * 2)
        min_combo = min(double_combo[i:i + 3] for i in range(3))
        combinations.add(min_combo)
    return sorted(combinations)


def generate_tiles(combinations):
    size = 400
    for combo in combinations:
        image = build_tile(combo, size / 2)
        image = image.rotate(90, expand=True)
        image.save(f'gamutile-{combo}.png')
    image = build_back(size / 2)
    image = image.rotate(90, expand=True)
    image.save(f'gamutile-back.png')
    print(f'Generated {len(combinations)} tiles.')


def demo_main():
    size = 400
    image = build_tile('Aae', size / 2)
    live_image = LivePillowImage(image)
    live_image.display((-size/2, size/2))


# noinspection DuplicatedCode
def main():
    combinations = list(generate_combinations('AaeBbc'))
    generate_tiles(combinations)

    folder_path = Path(__file__).parent
    button = loads((folder_path/'button.json').read_text())
    deck = loads((folder_path/'deck1.json').read_text())
    all_widgets = []
    all_widgets.extend(deck)
    all_widgets.append(button)
    holder, template = deck
    card_types = template['cardTypes']
    for combo in combinations:
        card_type_id = f'card-type-{combo}'
        card_type = dict(face=f'package://userassets/gamutile-{combo}.png',
                         label=f'gamutile-{combo}.png')
        card_types[card_type_id] = card_type
        piece = dict(id=f'piece{combo}',
                     type='piece',
                     cardType=card_type_id,
                     deck=template['id'],
                     parent=holder['id'],
                     x=holder['x'],
                     y=holder['y'],
                     z=holder['z'])
        all_widgets.append(piece)
    widgets_hex_hex = all_widgets[:]
    for i in range(11):
        latitude = abs(i - 5)
        start = (latitude + 1) // 2
        end = start + 9 - latitude
        for j in range(14):
            pile = dict(id=f'pile_{i}_{j}',
                        x=200 + j*92 + (i % 2)*46,
                        y=50 + i*78,
                        z=1630,
                        type='cardPile',
                        height=105,
                        r=0,
                        width=92)
            all_widgets.append(pile)
            if latitude < 5 and start <= j < end:
                widgets_hex_hex.append(pile)

    for name, widgets in (('gamutile.pcio', all_widgets),
                          ('gamutile-hex-hex.pcio', widgets_hex_hex)):
        with ZipFile(folder_path/name, 'w') as zf:
            zf.writestr('widgets.json', dumps(widgets))
            for combo in combinations + ['back']:
                zf.write(f'gamutile-{combo}.png',
                         f'userassets/gamutile-{combo}.png')


if __name__ == '__live_coding__':
    demo_main()
elif __name__ == '__main__':
    main()
