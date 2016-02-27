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
    def __init__(self, state=None):
        if state:
            super(GameBoard, self).__init__(lambda : EMPTY, state)
        else:
            super(GameBoard, self).__init__(lambda : EMPTY)
            self.update({((c, rows[0]), WHITE) for c in columns})
            self.update({((c, rows[-1]), BLACK) for c in columns})


    def copy(self):
        return GameBoard(state=self)

    def __str__(self):
        s = ''
        s += '  ' + ' '.join(str(c) for c in columns) + '\n'
        for r in rows:
            row = ' '.join(self[(c, r)] for c in columns)
            s += '{num} {row}'.format(num=r, row=row) + '\n'
        return s

    # Print the same way
    __repr__ = __str__

    def next_positions(self, team):
        direction = DOWN if team == WHITE else UP
        enemy = WHITE if team == BLACK else BLACK
        for ((c, r), v) in self.iteritems():
            if v != team:
                continue
            current_pos = (c, r)
            forward = (c, r + direction)
            diag_left = (c - 1, r + direction)
            diag_right = (c + 1, r + direction)
            if self.is_in_grid(forward) and self[forward] == EMPTY:
                new_state = self.copy()
                new_state.move(current_pos, forward)
                yield new_state
            if self.is_in_grid(diag_right) and self[diag_right] == enemy:
                new_state = self.copy()
                new_state.move(current_pos, diag_right)
                yield new_state
            if self.is_in_grid(diag_left) and self[diag_left] == enemy:
                new_state = self.copy()
                new_state.move(current_pos, diag_left)
                yield new_state

    def is_in_grid(self, square):
        c, r = square
        return c in columns and r in rows

    def move(self, current, to):
        self[to] = self[current]
        self[current] = EMPTY

def get_best_move(team, game_board, depth_limit=None): pass
def get_max(team, heuristic, game_board): pass
def get_min(): pass
