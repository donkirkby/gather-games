from io import BytesIO
from json import loads, dumps
from pathlib import Path
from zipfile import ZipFile

from tetrominoes import draw_tetromino


def main():
    folder_path = Path(__file__).parent
    deck = loads((folder_path/'deck.json').read_text())
    deck2 = loads((folder_path/'deck2.json').read_text())
    widgets = [deck2]
    widgets.extend(deck)
    widgets.append(dict(id="hand", type="hand", x=50, y=820, z=1, dragging=None))
    holder, template = deck
    card_types = template['cardTypes']
    for num1 in range(16):
        for num2 in range(num1, 16):
            type_name = f'type-{num1}-{num2}'
            card_type = dict(image=f"/img/dominoes/{num1}-{num2}.svg",
                             label=f"{num1}-{num2}")
            card_types[type_name] = card_type
            if num2 <= 6:
                piece = dict(id=f'piece-{num1}-{num2}',
                             type='card',
                             cardType=type_name,
                             deck=template['id'],
                             parent=holder['id'],
                             x=holder['x'],
                             y=holder['y'],
                             z=holder['z'])
                widgets.append(piece)
    row_count = 18
    col_count = 30
    for i in range(row_count):
        for j in range(col_count):
            id_root = f'pile_{i}_{j}'
            v_pile = dict(id=id_root+'_v',
                          x=200 + j*44,
                          y=50 + i*42,
                          z=1630,
                          type='cardPile',
                          height=84,
                          r=0,
                          width=44,
                          hasShuffleButton=True,
                          dragging=None)
            if i < row_count - 1:
                widgets.append(v_pile)
            h_pile = dict(v_pile,
                          id=id_root+'_h',
                          r=90)
            h_pile['x'] += 22
            h_pile['y'] -= 22
            if j < col_count - 1:
                widgets.append(h_pile)
    tetrominoes = {}
    for letter in 'ijlotsz':
        for colour in ('cornsilk', 'black'):
            name = f'tetromino-{letter}-{colour}.png'
            image = draw_tetromino(letter.upper(), colour)
            tetrominoes[name] = image

    tetromino_types = deck2['cardTypes']
    for i, (front, back) in enumerate((('o', 'o'),
                                       ('l', 'j'),
                                       ('j', 'l'),
                                       ('t', 't'),
                                       ('s', 'z'),
                                       ('z', 's'),
                                       ('i', 'i'))):
        type_name = f'type-tetromino-{front}'
        tetromino_type = dict(
            face=f'package://userassets/tetromino-{front}-black.png',
            back=f'package://userassets/tetromino-{back}-cornsilk.png',
            label=f'Tetromino {front.upper()}')
        tetromino_types[type_name] = tetromino_type
        piece = dict(id=f'tetromino-{front}',
                     type='piece',
                     cardType=type_name,
                     deck=deck2['id'],
                     x=40,
                     y=200+i*84,
                     z=1800,
                     faceup=True,
                     r=0)
        widgets.append(piece)

    with ZipFile(folder_path/'dominoes.pcio', 'w') as zf:
        zf.writestr('widgets.json', dumps(widgets))
        for name, image in tetrominoes.items():
            f = BytesIO()
            image.save(f, 'PNG')
            zf.writestr('userassets/' + name, f.getvalue())


main()
