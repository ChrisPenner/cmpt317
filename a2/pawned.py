#! /usr/bin/python

from collections import defaultdict, Counter
from operator import itemgetter
from functools import partial
import re
import time

BOARD_SIZE = 6
columns = range(BOARD_SIZE)
rows = range(BOARD_SIZE)
letters = [chr(n) for n in range(ord('A'), ord('z') + 1)]

WHITE = 'w'
BLACK = 'b'
SPECTATOR = '-'
EMPTY = '.'
UP = -1
DOWN = 1

move_regex = re.compile(r'[a-zA-Z]\d')

class InvalidMove(Exception): pass

class GameBoard(defaultdict):
    def __init__(self, state=None):
        """ Set up the board to the starting state. """
        if state:
            super(GameBoard, self).__init__(lambda : EMPTY, state)
        else:
            super(GameBoard, self).__init__(lambda : EMPTY)
            self.update({((c, rows[0]), WHITE) for c in columns})
            self.update({((c, rows[-1]), BLACK) for c in columns})

    def copy(self):
        """ Return a new version of the board """
        return GameBoard(state=self)

    def __str__(self):
        """ Print out the board in a human readable form"""
        s = '  ' + ' '.join(letters[c] for c in columns) + '\n'
        for r in rows:
            row = ' '.join(self[(c, r)] for c in columns)
            s += '{num} {row}'.format(num=r, row=row) + '\n'
        return s

    # Print the same way
    __repr__ = __str__
    
    def has_winner(self):
        """ Return a 1 if white has won, -1 if black has won, 0 otherwise"""
        points = 0
        first = 0
        last = rows[-1]

        for c in columns:
            if self[(c,first)] == BLACK:
                points -= 1
            if self[(c,last)] == WHITE:
                points += 1
        return points

    def next_positions(self, team):
        """ A generator yielding all possible next game boards for 'team'"""
        if self.has_winner() != 0:
            return

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
        """ A generator yielding all possible next valid moves for the piece at 'location'"""
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

    def can_move(self, team):
        """ Returns whether moves exist for 'team'"""
        return bool(list(self.next_positions(team)))

    def is_in_grid(self, location):
        """ Returns whether location is on the board"""
        c, r = location
        return c in columns and r in rows

    def move(self, current, to):
        """ Moves the piece at current -> to"""
        if to in self.valid_moves(current):
            self[to] = self[current]
            self[current] = EMPTY
        else:
            raise InvalidMove("Invalid Move: {}".format((current, to)))

states = 0
def get_best_score(state, team, heuristic, depth_limit=6, prune=None):
    """ 
    Recursively searches returns the best possible score we can find by
    starting at 'state' given a team, heuristic and depth_limit.
    Does alpha-beta pruning when possible.
    """
    global states
    states += 1
    if depth_limit == 0:
        return heuristic(state)

    minimize = True if team == BLACK else False
    next_team = BLACK if team == WHITE else WHITE
    possible_moves = state.next_positions(team)
    best_score = None

    for move in possible_moves:
        score = get_best_score(move,
                               depth_limit=depth_limit-1,
                               team=next_team,
                               heuristic=heuristic,
                               prune=best_score,
                               )
        # This is where pruning happens
        if best_score is None:
            best_score = score
        if minimize and score < best_score:
            best_score = score
        if not minimize and best_score < score:
            best_score = score
        if prune is not None:
            if minimize and best_score <= prune:
                return best_score
            if not minimize and best_score >= prune:
                return best_score
    if best_score is None:
        return heuristic(state)
    return best_score

def get_best_move(state, team, heuristic):
    """
    Returns a board state representing the 'move' that the AI would like to make
    """
    print 'Thinking...'
    next_moves = list(state.next_positions(team))
    next_team = WHITE if team == BLACK else BLACK
    if not next_moves:
        return None
    compare_func = max if team == WHITE else min
    global states
    states = 0
    best_score, best_move = compare_func((get_best_score(move, next_team, heuristic), move) 
                                for move in next_moves)
    print 'Total States Checked: {}'.format(states)
    print "Best Guess for Score:", best_score
    return best_move

def to_coord(s):
    """ Changes a 'a2' string into a (column, row) coordinate """
    c = ord(s[0].lower()) - ord('a')
    r = int(s[1])
    return (c, r)

def get_move_from_player(board):
    """ Prompts the user for a move and returns the resultant game board """
    board = board.copy()
    while True:
        inp = raw_input('> ')
        if inp == 'exit':
            raise Exception('Quite by user')
        moves = move_regex.findall(inp)
        if len(moves) != 2:
            print "Type a move like this: 'a1 b1'"
            continue
        moves = [to_coord(m) for m in moves]
        try:
            board.move(*moves)
            return board
        except InvalidMove:
            print 'Invalid Move!'
            print "Type a move like this: 'a1 a2'"
            continue

def play():
    """ Kicks off a command line interface for the game. """
    player = None
    while not player:
        team_choice = raw_input('Choose a team: white, black, spectator:\n').lower()
        if team_choice.startswith('w'):
            player = WHITE
            print 'Good choice. You go first'
        elif team_choice.startswith('b'):
            player = BLACK
            print 'Good choice. You go second'
        elif team_choice.startswith('s'):
            player = SPECTATOR
        else:
            print "Sorry, didn't get that..."
    enemy = BLACK if player == WHITE else WHITE
    board = GameBoard()
    print board
    while True:
        white_can_move =  board.can_move(WHITE)
        if white_can_move:
            if player == WHITE:
                board = get_move_from_player(board)
            else:
                t = time.time()
                board = get_best_move(board, team=WHITE, heuristic=h1)
                print "Took {} seconds".format(time.time() - t)
            print board
        else:
            print "No moves, next turn"

        if board.has_winner() != 0:
            break

        black_can_move =  board.can_move(BLACK)
        if black_can_move:
            if player == BLACK:
                board = get_move_from_player(board)
            else:
                t = time.time()
                board = get_best_move(board, team=BLACK, heuristic=h2)
                print "Took {} seconds".format(time.time() - t)
            print board
        else:
            print "No moves, next turn"
        if not any([white_can_move, black_can_move]):
            break

        if board.has_winner() != 0:
            break

    if board.has_winner() == 1:
         print "White won"
         return
    elif board.has_winner() == -1:
         print "Black won"
         return

    final_score = h1(board)
    if final_score > 0:
        print "White won with a score of {}".format(final_score)
    elif final_score < 0:
        print "Black won with a score of {}".format(abs(final_score))
    else:
        print "It was a draw!"

def get_piece_difference(board):
    num_pieces = Counter(board.itervalues())
    white = num_pieces[WHITE]
    black = num_pieces[BLACK]
    return white - black

def get_positioning_score(board):
    positioning_score = 0
    for location, piece in board.items():
        if piece == EMPTY:
            continue
        c, r = location
        points = 0

        if board[(c + 1, r + 1)] == piece:
            points += 1
        if board[(c - 1, r + 1)] == piece:
            points += 1

        if piece == WHITE:
            positioning_score += points
        else:
            positioning_score -= points
        return positioning_score

# Heuristics...
def h1(board):
    """ 
    Simply counts the number of pieces each team has and returns the difference
    Heuristics are positive when white is doing well, negative when black is doing well.
    """
    return get_piece_difference(board)

def h2(board):
    """ 
    Counts difference between number of pieces but also gives a positioning score
    for each team. The score is better when the player has pieces aligned diagonally
    from each other.
    Heuristics are positive when white is doing well, negative when black is doing well.
    """
    difference = get_piece_difference(board)
    positioning_score = get_positioning_score(board)
    return (difference, positioning_score)

def h3(board):
    """ 
    Simply returns whether some team has won the game in this board state.
    """
    return board.has_winner()

def h4(board):
    """ 
    Combines h1 and h3 into one heuristic
    """
    return (board.has_winner(), get_piece_difference(board))

def h5(board):
    """ 
    Combines h1, h2 and h3 into one heuristic
    """
    difference = get_piece_difference(board)
    positioning_score = get_positioning_score(board)
    winner_score = board.has_winner()
    return (winner_score, difference, positioning_score)

if __name__ == '__main__':
    play()
