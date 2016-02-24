from collections import defaultdict

BOARD_SIZE = 6
columns = 'abcdef'
rows = range(6)

class GameBoard(defaultdict):
    def __init__(self):
        super(GameBoard, self).__init__(lambda: '.')
        self.update({((n, c), 'w') for n in rows[:2] for c in columns})
        self.update({((n, c), 'b') for n in rows[-2:] for c in columns})

    def __str__(self):
        s = ''
        for n in rows:
            row = ' '.join(self[(n, c)] for c in columns)
            s += '{}'.format(row) + '\n'
        return s
