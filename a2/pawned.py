from collections import defaultdict

BOARD_SIZE = 6
columns = range(6)
rows = range(6)

WHITE = 'w'
BLACK = 'b'
EMPTY = '.'
UP = -1
DOWN = 1

class GameBoard(defaultdict):
    def __init__(self):
        super(GameBoard, self).__init__(lambda: EMPTY)
        self.update({((c, r), WHITE) for r in rows[:2] for c in columns})
        self.update({((c, r), BLACK) for r in rows[-2:] for c in columns})

    def __str__(self):
        s = ''
        s += '  ' + ' '.join(str(c) for c in columns) + '\n'
        for r in rows:
            row = ' '.join(self[(c, r)] for c in columns)
            s += '{num} {row}'.format(num=r, row=row) + '\n'
        return s

    def next_positions(self, team):
        direction = DOWN if team == WHITE else UP
        enemy = WHITE if team == BLACK else BLACK
        for ((c, r), v) in self.iteritems():
            if v != team:
                continue
            forward = (c, r + direction)
            diag_left = (c - 1, r + direction)
            diag_right = (c + 1, r + direction)
            if self.is_in_grid(forward) and self[forward] == EMPTY:
                yield forward
            if self.is_in_grid(diag_right) and self[diag_right] == enemy:
                yield diag_right
            if self.is_in_grid(diag_left) and self[diag_left] == enemy:
                yield diag_left

    def is_in_grid(self, square):
        c, r = square
        return c in columns and r in rows




