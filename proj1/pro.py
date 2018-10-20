from search import *
import copy
# TAI content
def c_peg():
    return "O"

def c_empty():
    return "_"

def c_blocked():
    return "X"

def is_empty(e):
    return e == c_empty()

def is_peg(e):
    return e == c_peg()

def is_blocked(e):
    return e == c_blocked()

# TAI pos
# Tuplo (l, c)
def make_pos(l, c):
    return (l, c)

def pos_l(pos):
    return pos[0]

def pos_c(pos):
    return pos[1]

# TAI move
# Lista [p_initial, p_final]
def make_move(i, f):
    return [i, f]

def move_initial(move):
    return move[0]

def move_final(move):
    return move[1]

# TAI board
def get_board_pos(board, pos):
    line = pos_l(pos)
    column = pos_c(pos)
    return board[line][column]

def set_board_pos(board, pos, content):
    line = pos_l(pos)
    column = pos_c(pos)
    board[line][column] = content

def is_valid_move(board, move):
    pos_initial = move_initial(move)
    pos_final = move_final(move)

    line_middle = (pos_l(pos_initial) + pos_l(pos_final))//2
    column_middle = (pos_c(pos_initial) + pos_c(pos_final))//2
    pos_middle = make_pos(line_middle, column_middle)

    if is_peg(get_board_pos(board,pos_initial)) and is_peg(get_board_pos(board,pos_middle)) and is_empty(get_board_pos(board,pos_final)):
        return True
    else:
        return False

def board_moves(board):
    total_moves = []

    lines = len(board)
    columns = len(board[0])

    last_line = lines - 1
    last_column = columns - 1

    def get_pos_moves(line, column):
        pos_moves = []
        jump_size = 2
        current_pos = make_pos(line, column)

        def add_pos(pos):
            move = make_move(current_pos, move_pos)
            if is_valid_move(board, move):
                pos_moves.append(move)

        if column >= jump_size:
            move_pos = make_pos(line, column - jump_size)
            add_pos(move_pos)

        if column <= last_column - jump_size:
            move_pos = make_pos(line, column + jump_size)
            add_pos(move_pos)

        if line >= jump_size:
            #testa cima
            move_pos = make_pos(line - jump_size, column)
            add_pos(move_pos)

        if line <= last_line - jump_size:
            move_pos = make_pos(line + jump_size, column)
            add_pos(move_pos)

        return pos_moves

    for line in range(lines):
        for column in range(columns):
            total_moves += get_pos_moves(line, column)

    return total_moves

def board_perform_move(board, move):
    pos_initial = move_initial(move)
    pos_final = move_final(move)

    line_middle = (pos_l(pos_initial) + pos_l(pos_final))//2
    column_middle = (pos_c(pos_initial) + pos_c(pos_final))//2
    pos_middle = make_pos(line_middle, column_middle)

    new_board = copy.deepcopy(board)
    set_board_pos(new_board, pos_initial, c_empty())
    set_board_pos(new_board, pos_middle, c_empty())
    set_board_pos(new_board, pos_final, c_peg())
    return new_board

# TAI sol_state
class sol_state:
    def __init__(self, b):
     self.board = b
     self.number_of_pegs = self.count_pegs()

    def __repr__(self):
        return "<SOL_state {}>".format(self.board)

    def __lt__(self, other_state):
        return 1

    def __str__(self):
        return '\n'.join(str(line) for line in self.board)

    def count_pegs(self):
        number_of_pegs = 0
        for line in self.board:
            number_of_pegs += line.count(c_peg())
        return number_of_pegs

    def get_number_of_pegs(self):
        return self.number_of_pegs

    def get_board(self):
        return self.board


class solitaire(Problem):
    """Models a Solitaire problem as a satisfaction problem.
    A solution cannot have more than 1 peg left on the board."""

    def __init__(self, initial, goal=None):
        """The constructor specifies the initial state, and possibly a goal
        state, if there is a unique goal.  Your subclass's constructor can add
        other arguments."""
        self.initial = initial
        self.goal = goal

    def actions(self, state):
        return board_moves(state.get_board())

    def result(self, state, action):
        return sol_state(board_perform_move(board, action))

    def goal_test(self, state):
        if state.get_number_of_pegs() == 1:
            return True
        else:
            return False

    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2.  If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        return c + 1

    def value(self, state):
        """For optimization problems, each state has a value.  Hill-climbing
        and related algorithms try to maximize this value."""
        raise NotImplementedError


board = [["_","O","O","O","_"], ["O","_","O","_","O"], ["_","O","_","O","_"], ["O","_","O","_","_"], ["_","O","_","_","_"]]
state = sol_state(board)
problem = solitaire(state)
actions = problem.actions(state)
print(problem.result(state, actions[0]))
