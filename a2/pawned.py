#! /usr/bin/python

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

class InvalidMove(Exception): pass

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
        s = '  ' + ' '.join(letters[c] for c in columns) + '\n'
        for r in rows:
            row = ' '.join(self[(c, r)] for c in columns)
            s += '{num} {row}'.format(num=r, row=row) + '\n'
        return s

    # Print the same way
    __repr__ = __str__

    def next_positions(self, team):
        direction = DOWN if team == WHITE else UP
        enemy = WHITE if team == BLACK else BLACK
        our_pieces = [location for (location, value) in self.iteritems()
                                    if value == team]
        for piece in our_pieces:
            moves = self.valid_moves(piece)
            for move in moves:
                new_state = self.copy()
                new_state.move(piece, move)
                yield new_state

    def valid_moves(self, location):
        c, r = location
        piece = self[location]
        if piece == EMPTY:
            raise InvalidMove("Can't move an empty square!")
        enemy = BLACK if piece == WHITE else WHITE
        direction = DOWN if piece == WHITE else UP
        forward = (c, r + direction)
        diag_left = (c - 1, r + direction)
        diag_right = (c + 1, r + direction)
        moves = []
        if self.is_in_grid(forward) and self[forward] == EMPTY:
            moves.append(forward)
        if self.is_in_grid(diag_left) and self[diag_left] == enemy:
            moves.append(diag_left)
        if self.is_in_grid(diag_right) and self[diag_right] == enemy:
            moves.append(diag_right)
        return moves

    def is_in_grid(self, location):
        c, r = location
        return c in columns and r in rows

    def move(self, current, to):
        if to in self.valid_moves(current):
            self[to] = self[current]
            self[current] = EMPTY
        else:
            raise InvalidMove("Invalid Move: {}".format((current, to)))

state_count = 0
def next_move(state, team=WHITE, depth_limit=5):
    global state_count
    state_count = 0
    move, score = next(get_best_move(state, depth_limit=depth_limit, team=team, prune=None), None)
    print 'States:', state_count
    return move

def get_best_move(state, depth_limit=None, team=WHITE, prune=None):
    global state_count
    state_count += 1
    # Base condition, back out
    if depth_limit == 0:
        yield heuristic(state), state
        return

    minimize = True if team == BLACK else False
    min_or_max = min if minimize else max
    next_team = BLACK if team == WHITE else WHITE
    possible_moves = list(state.next_positions(team))
    if not possible_moves:
        yield heuristic(state), state
        return

    recurse = partial(get_best_move,
                      team=next_team,
                      depth_limit=depth_limit-1,
                      )

    # If we can't prune, then just min/max the whole lot and get the best
    if prune is None:
        best_score = None
        for move in possible_moves:
            results = list(recurse(state=move, prune=prune))
            if not results:
                continue
            result = min_or_max(results)
            score, move = result
            if best_score is None:
                best_score = score
            if minimize and score < best_score:
                best_score = score
            if not minimize and best_score < score:
                best_score = score
            # if prune is None:
            #     prune = score
            # elif minimize and score < prune:
            #     prune = score
            # elif not minimize and score > prune:
            #     prune = score
        yield best_score, state
        return

    # The pruning break condition depends on whether we're on max or min
    if minimize:
        break_out_cond = lambda x: x <= prune
    else:
        break_out_cond = lambda x: x >= prune

    nexts = (n for n in recurse(state=state) for state in possible_moves)

    for (score, board) in nexts:
        # Be smart and quit if we're going to get pruned
        if break_out_cond(score):
            return
        else:
            yield score, board

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
        try:
            board.move(*moves)
        except InvalidMove:
            print 'Invalid Move!'
            print "Type a move like this: 'a1 a2'"
            continue
        print board
        move = next_move(board, team=BLACK, depth_limit=10)
        if not move and not board.next_positions(WHITE):
            print 'No more moves!'
            break
        else:
            next_board = move
            if next_board:
                board = next_board
            print board
            continue

if __name__ == '__main__':
    play()
