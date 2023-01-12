from json import loads, dumps
from pathlib import Path
from zipfile import ZipFile


def main():
    folder_path = Path(__file__).parent
    deck = loads((folder_path/'deck.json').read_text())
    widgets = []
    widgets.extend(deck)
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
    row_count = 20
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

    with ZipFile(folder_path/'dominoes.pcio', 'w') as zf:
        zf.writestr('widgets.json', dumps(widgets))


main()
