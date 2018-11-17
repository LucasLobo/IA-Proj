from search import *
import hashlib
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
# Lista de listas [N X M]
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
    def __init__(self, b, number_of_pegs = None):
        self.board = b

        if number_of_pegs is not None:
            self.number_of_pegs = number_of_pegs
        else:
            self.number_of_pegs = self.count_pegs()

        self.actions = ''
        self.actions_len = ''

    # def __key(self):
    #     return str(self)
    #
    # def __hash__(self):
    #     return hash(self.__key())
    #
    # def __eq__(self, other):
    #     return self.__key() == other.__key()

    def __lt__(self, other):
        return self.number_of_pegs > other.number_of_pegs

    def __repr__(self):
        return "<SOL_state {}>".format(self.board)

    def __str__(self):
        return str(self.board)

    def count_pegs(self):
        number_of_pegs = 0
        for line in self.board:
            number_of_pegs += line.count(c_peg())
        return number_of_pegs

    def get_actions(self):
        if self.actions == '':
            self.actions = board_moves(self.board)
            self.actions_len = len(self.actions)
        return self.actions

    def get_actions_len(self):
        if self.actions == '':
            self.actions = board_moves(self.board)
            self.actions_len = len(self.actions)
        return self.actions_len


class solitaire(Problem):
    def __init__(self, initial, goal=None):
        self.initial = sol_state(initial)
        self.goal = goal
        if goal:
            self.goal = sol_state(goal)

    def actions(self, state):
        return state.get_actions()

    def result(self, state, action):
        return sol_state(board_perform_move(state.board, action), state.number_of_pegs - 1)

    def goal_test(self, state):
        if state.number_of_pegs == 1:
            return True
        else:
            return False

    def path_cost(self, c, state1, action, state2):
        return 1/max(1,state1.number_of_pegs - state1.get_actions_len())

    def h(self, node):
        return max(1,node.state.number_of_pegs - node.state.get_actions_len())

board_5_5 = [["_","O","O","O","_"],  ["O","_","O","_","O"],  ["_","O","_","O","_"],  ["O","_","O","_","_"],  ["_","O","_","_","_"]]

board_4_4 = [["O","O","O","X"],  ["O","O","O","O"],  ["O","_","O","O"],  ["O","O","O","O"]]

board_4_5 = [["O","O","O","X","X"],  ["O","O","O","O","O"],  ["O","_","O","_","O"],  ["O","O","O","O","O"]]

board_4_6 = [["O","O","O","X","X","X"],  ["O","_","O","O","O","O"],  ["O","O","O","O","O","O"],  ["O","O","O","O","O","O"]]

board = [["O","O","O","X","X","X"],["O","_","O","O","O","O"],["O","O","O","O","O","O"],["O","O","O","O","O","O"]]

def compare_searchers(problems, header,
                      searchers=[#depth_first_tree_search,
                                 greedy_search,
                                 astar_search
                                 ]):
    def do(searcher, problem):
        p = InstrumentedProblem(problem)
        searcher(p)
        return p
    table = [[name(s)] + [do(s, p) for p in problems] for s in searchers]
    print_table(table, header)


def compare_graph_searchers():
    """Prints a table of search results."""
    compare_searchers(problems=[solitaire(board_5_5), solitaire(board_4_4), solitaire(board_4_5), solitaire(board_4_6)],
                      header=['Searcher', '5x5', '4x4', '4x5', '4x6'])

#compare_graph_searchers()

#depth_first_tree_search(solitaire(board_4_6))
#greedy_search(solitaire(board_4_4))
astar_search(solitaire(board_4_4))
