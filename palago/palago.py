from json import loads, dumps
from pathlib import Path
from zipfile import ZipFile


# noinspection HttpUrlsUsage
def main():
    """ Rules online:

    http://cambolbro.com/games/mambo/
    http://cambolbro.com/games/palago/
    """

    folder_path = Path(__file__).parent
    button = loads((folder_path/'button.json').read_text())
    deck1 = loads((folder_path/'deck1.json').read_text())
    deck2 = loads((folder_path/'deck2.json').read_text())
    all_widgets = []
    all_widgets.extend(deck1)
    all_widgets.extend(deck2)
    all_widgets.append(button)
    for deck_num, deck in enumerate((deck1, deck2)):
        holder, template = deck
        piece_count = 48
        for piece_num in range(piece_count):
            piece = dict(id=f'deck{deck_num}_piece{piece_num}',
                         type='piece',
                         cardType='type-3ac2414b-e269-4912-919c-4102c29b6987',
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

    for name, widgets in (('palago.pcio', all_widgets),
                          ('palago-hex-hex.pcio', widgets_hex_hex)):
        with ZipFile(folder_path/name, 'w') as zf:
            zf.writestr('widgets.json', dumps(widgets))
            zf.write('mambo-blue.png', 'userassets/mambo-blue.png')
            zf.write('mambo-red.png', 'userassets/mambo-red.png')
            zf.write('palago-blue.png', 'userassets/palago-blue.png')
            zf.write('palago-red.png', 'userassets/palago-red.png')


main()
