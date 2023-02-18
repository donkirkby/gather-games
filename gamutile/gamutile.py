import typing
from itertools import product
from math import cos, sin, pi, sqrt

from PIL import Image, ImageDraw, ImageColor
from PIL.ImageDraw import floodfill
from space_tracer import LivePillowImage


class SpinDraw:
    def __init__(self, r: float):
        self.r = r
        self.line_width = round(r * 0.02)
        width = round(r * 2)
        height = round(2 * r * sin(pi / 3))
        self.image = Image.new('RGBA', (width, height))
        self.draw = ImageDraw.Draw(self.image)
        self.cx = width / 2
        self.cy = height / 2
        self.angle = 0
        self.draw.rectangle((0, 0, width, height), fill='cornsilk')
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

    def arc(self):
        r = self.r
        x, y = self.transform(r, 0)
        x += self.cx
        y += self.cy

        self.draw.arc(((x - r/2, y - r/2),
                       (x + r/2, y + r/2)),
                      120 + self.angle,
                      240 + self.angle,
                      fill='black',
                      width=self.line_width)

    def line(self):
        self.spin(-30)
        x, y = self.transform(self.r*sqrt(3)/2, 0)
        self.spin(30)
        self.draw.line(((self.cx - x, self.cy - y),
                        (self.cx + x, self.cy + y)),
                       fill='black',
                       width=self.line_width)

    def fill(self, colour_name):
        x, y = self.transform(self.r*3/4, 0)

        fill = ImageColor.getcolor(colour_name, 'RGBA')
        floodfill(self.image, (self.cx + x, self.cy + y), fill)


def build_tile(points: str, r: float) -> Image.Image:
    colour_names = {'R': 'red',
                    'r': 'coral',
                    'G': 'grey',
                    'B': 'blue',
                    'b': 'lightblue'}
    r *= 2
    spin_draw = SpinDraw(r)
    if points[0] != points[1]:
        spin_draw.arc()
        if points[1] != points[2]:
            spin_draw.spin(120)
            spin_draw.arc()
            spin_draw.spin(120)
            spin_draw.arc()
            spin_draw.spin(120)
        else:
            spin_draw.spin(120)
            spin_draw.line()
            spin_draw.spin(60)
            spin_draw.arc()
            spin_draw.spin(-180)
    else:
        spin_draw.spin(60)
        spin_draw.arc()
        spin_draw.spin((-60))
        if points[0] != points[2]:
            spin_draw.line()
            spin_draw.spin(-120)
            spin_draw.arc()
            spin_draw.spin(120)
        else:
            spin_draw.spin(60)
            spin_draw.arc()
            spin_draw.spin(120)
            spin_draw.arc()
            spin_draw.spin(120)
            spin_draw.arc()
            spin_draw.spin(60)

    for point in points:
        colour_name = colour_names[point]
        spin_draw.fill(colour_name)
        spin_draw.spin(120)

    image = spin_draw.image
    return image.resize((image.width // 2, image.height // 2), Image.LANCZOS)


def generate_combinations(colours: str) -> typing.List[str]:
    combinations = set()
    for combo in product(colours, repeat=3):
        double_combo = ''.join(combo * 2)
        min_combo = min(double_combo[i:i + 3] for i in range(3))
        combinations.add(min_combo)
    return sorted(combinations)


def demo_main():
    combinations = list(generate_combinations('RGB'))
    combo = combinations[10]
    size = 400
    image = build_tile(combo, size / 2)
    live_image = LivePillowImage(image)
    live_image.display((-size/2, size/2))


def main():
    combinations = list(generate_combinations('RrGBb'))
    for combo in combinations:
        size = 400
        image = build_tile(combo, size / 2)
        image.save(f'gamutile-{combo}.png')
    print(f'Generated {len(combinations)} tiles.')


if __name__ == '__live_coding__':
    demo_main()
elif __name__ == '__main__':
    main()
