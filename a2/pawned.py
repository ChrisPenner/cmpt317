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

states_travelled = 0
def get_best_score(state, team, depth_limit=10):
    global states_travelled
    states_travelled += 1
    if depth_limit == 0:
        return heuristic(state)

    minimize = True if team == BLACK else False
    min_or_max = min if minimize else max
    next_team = BLACK if team == WHITE else WHITE
    possible_moves = state.next_positions(team)
    best_score = None

    for move in possible_moves:
        score = get_best_score(move, depth_limit=depth_limit-1, team=next_team)
        if best_score is None:
            best_score = score
        if minimize and score < best_score:
            best_score = score
        if not minimize and best_score < score:
            best_score = score
    return best_score

def get_best_move(state, team):
    next_moves = list(state.next_positions(team))
    if not next_moves:
        return None
    compare_func = max if team == WHITE else min
    global states_travelled
    states_travelled = 0
    _, best_move = compare_func((get_best_score(move, team), move) 
                                for move in next_moves)
    print states_travelled
    return best_move

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
        if list(board.next_positions(WHITE)):
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
        else:
            print "White has no moves, black's turn"
        move = get_best_move(board, team=BLACK)
        if move is None and not list(board.next_positions(WHITE)):
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
