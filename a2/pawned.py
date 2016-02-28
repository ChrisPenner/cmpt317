from collections import defaultdict, Counter
from operator import itemgetter
from functools import partial
import re

BOARD_SIZE = 4
columns = range(BOARD_SIZE)
rows = range(BOARD_SIZE)
letters = [chr(n) for n in range(ord('A'), ord('z') + 1)]

WHITE = 'w'
BLACK = 'b'
EMPTY = '.'
UP = -1
DOWN = 1

move_regex = re.compile(r'[a-zA-Z]\d')

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
        s += '  ' + ' '.join(letters[c] for c in columns) + '\n'
        for r in rows:
            row = ' '.join(self[(c, r)] for c in columns)
            s += '{num} {row}'.format(num=r, row=row) + '\n'
        return s

    # Print the same way
    __repr__ = __str__

    def next_positions(self, team):
        direction = DOWN if team == WHITE else UP
        enemy = WHITE if team == BLACK else BLACK
        for ((c, r), v) in self.items():
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

# def get_best_move(game_board, depth_limit=None, team=WHITE):
#     min_or_max = min if team==BLACK else max
#     next_team = BLACK if team == WHITE else WHITE
#     possible_moves = game_board.next_positions(team)
#     if depth_limit == 0:
#         return min_or_max((board, heuristic(board)) for board in possible_moves)
#     recurse = partial(get_best_move,
#                       team=next_team,
#                       depth_limit=depth_limit-1)

    # next_set = ((board, recurse(game_board=board)[1]) for board in possible_moves)
    # board, score = min_or_max(next_set, key=itemgetter(1))
    # return board, score

state_count = 0
def next_move(state, team=WHITE, depth_limit=5):
    global state_count
    v = next(get_best_move(state, depth_limit=depth_limit, team=team, prune=None))
    print 'States:', state_count
    return v

def get_best_move(state, depth_limit=None, team=WHITE, prune=None):
    global state_count
    state_count += 1
    # Base condition, back out
    if depth_limit == 0:
        yield (None, heuristic(state))
        return

    minimize = True if team==BLACK else False
    min_or_max = min if minimize else max
    next_team = BLACK if team == WHITE else WHITE
    possible_moves = state.next_positions(team)

    recurse = partial(get_best_move,
                      team=next_team,
                      depth_limit=depth_limit-1)

    if prune is None:
    # If we can't prune, then just min/max the whole lot and get the best
        def g():
            prune = None
            for s in possible_moves:
                r = list(recurse(state=s, prune=prune))
                if not r:
                    continue
                board, score = min_or_max(r)
                yield s, score
                if prune is None:
                    prune = score
                elif minimize and score < prune:
                    prune = score
                elif not minimize and score > prune:
                    prune = score
        r = list(g())
        if r:
            yield min_or_max(r)
        return

        # yield min_or_max(min_or_max(n) for n in nexts)
        # return

    # The pruning break condition depends on whether we're on max or min
    if minimize:
        break_out_cond = lambda x: x <= prune
    else:
        break_out_cond = lambda x: x >= prune

    nexts = (n for n in recurse(state=state) for state in possible_moves)

    for (board, score) in nexts:
        # Be smart and quit if we're going to get pruned
        if break_out_cond(score):
            return
        else:
            yield (board, score)

def heuristic(game_board):
    num_pieces = Counter(game_board.itervalues())
    white = num_pieces[WHITE]
    black = num_pieces[BLACK]
    return white - black

def to_coord(s):
    c = ord(s[0].lower()) - ord('a')
    r = int(s[1])
    return (c, r)

def play():
    board = GameBoard()
    print board
    while True:
        inp = raw_input('> ')
        if inp == 'exit':
            return
        moves = move_regex.findall(inp)
        if len(moves) != 2:
            print "Type a move like this: 'a1 b1'"
            continue
        moves = [to_coord(m) for m in moves]
        board.move(*moves)
        print board
        board = next_move(board, team=BLACK, depth_limit=10)[0]
        print board
