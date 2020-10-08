import numpy as np
from copy import deepcopy
from collections import deque, defaultdict
import sys

# Class to generate an output file

class Logger(object):
    def __init__(self):
        self.terminal = sys.stdout
        self.log = open("output.txt", "wt")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        #this flush method is needed for python 3 compatibility.
        #this handles the flush command by doing nothing.
        #you might want to specify some extra behavior here.
        pass

############# global variables ##############

# to track which players have won
winners_dict = defaultdict(int)

# initial state/node of the game (root)
initial_state = [[1, None, None, 2], [None, None, None, None], [None, None, None, None], [4, None, None, 3]]

# to store all generated nodes/states of the game
all_states = []

# to count the number of turn levels covered
levels = 0

# flag to set drawing mode: True=draw board, False=print node
draw = False

# flag set to write output to a file
to_file = True

############## functions ###################

# get current position of a player

def get_pos(state, player):
    pos = np.argwhere(np.array(state) == player)[0]
    i = pos[0]
    j = pos[1]
    return i, j

# Define the moves

def move_up(i, j):
    return i-1, j

def move_down(i, j):
    return i+1, j

def move_left(i, j):
    return i, j-1

def move_right(i, j):
    return i, j+1

# Determines if the made move is a legal move

def is_move_valid(i, j, state):
    if i < 0 or i > 3 or j < 0 or j > 3:
        return False
    elif state[i][j] is not None:
        return False
    else:
        return True

# Get list of all possible actions

def available_moves(state, i, j):
    if is_end(state):
        return None
    moves = []
    ui, uj = move_up(i, j)
    if is_move_valid(ui, uj, state):
        moves.append('up')
    di, dj = move_down(i, j)
    if is_move_valid(di, dj, state):
        moves.append('down')
    li, lj = move_left(i, j)
    if is_move_valid(li, lj, state):
        moves.append('left')
    ri, rj = move_right(i, j)
    if is_move_valid(ri, rj, state):
        moves.append('right')
    return moves

# define the action

def move(state, player, action):
    new_state = deepcopy(state)
    i, j = get_pos(state, player)
    new_state[i][j] = None
    if action == 'left':
        i_n, j_n = move_left(i, j)
    elif action == 'right':
        i_n, j_n = move_right(i, j)
    elif action == 'up':
        i_n, j_n = move_up(i, j)
    elif action == 'down':
        i_n, j_n = move_down(i, j)
    else:
        i_n, j_n = i, j
    new_state[i_n][j_n] = player
    return new_state

# Check if a player won

def is_win_p1(state):
    if state[3][3] == 1:
        winners_dict[1] += 1
        return True  # P1 wins
    else:
        return False

def is_win_p2(state):
    if state[3][0] == 2:
        winners_dict[2] += 1
        return True  # P2 wins
    else:
        return False

def is_win_p3(state):
    if state[0][0] == 3:
        winners_dict[3] += 1
        return True  # P3 wins
    else:
        return False

def is_win_p4(state):
    if state[0][3] == 4:
        winners_dict[4] += 1
        return True  # P4 wins
    else:
        return False

# find the winner

def winner(state):
    if is_win_p1(state):
        return "WINS[PLAYER{}]".format(1)
    elif is_win_p2(state):
        return "WINS[PLAYER{}]".format(2)
    elif is_win_p3(state):
        return "WINS[PLAYER{}]".format(3)
    elif is_win_p4(state):
        return "WINS[PLAYER{}]".format(4)
    else:
        return ""

# Check if the game has ended

def is_end(state):
    if is_win_p1(state) or is_win_p2(state) or is_win_p3(state) or is_win_p4(state):
        return True
    else:
        return False

# check if a state repeats

def is_repeated(state):
    if state in all_states:
        return "REPEATED"
    else:
        return ""

# Print the state

def draw_board(state):
    for i in range(0, 4):
        for j in range(0, 4):
            print("{}\t".format(state[i][j]), end=" ")
        print()
    print()

def print_node(current_player, father_node, action, current_node):
    print("[Current_player={} | Father_node={} | Action={} | Current_node={} | {} {}]".format(
        current_player, father_node, action, current_node, "REPEATED" if is_repeated(current_node) else "", winner(current_node))
    )

# Check utility value of players

def utility(state):
    if is_win_p1(state):
        return 20, 10, 30, 10
    elif is_win_p2(state):
        return 100, 300, 150, 200
    elif is_win_p3(state):
        return 150, 200, 400, 300
    elif is_win_p4(state):
        return 220, 330, 440, 500
    else:
        return 0, 0, 0, 0

############### main ######################

# to check if output is to be written to a file
if to_file:
    sys.stdout = Logger()

# queue to hold the states generated at end of each ply
ply_states = deque()

# the original state of the game
root = deepcopy(initial_state)
if(draw):
    draw_board(root)
else:
    print_node(1, None, None, root)

all_states.append(root)

ply_states.append(root)

while(ply_states):

    # DFS
    state = ply_states.popleft()

    current_state1 = deepcopy(state)
    # Check if game end
    if is_end(current_state1):
        continue
    # check moves available for 1
    x, y = get_pos(current_state1, 1)
    moves_for_1 = available_moves(current_state1, x, y)
    # check for stagnation (no moves available for 1)
    if len(moves_for_1) == 0:
        continue
    # for all moves available for 1
    for m1 in moves_for_1:
        # move 1
        parent_state1 = deepcopy(current_state1)
        new_state1 = move(parent_state1, 1, m1)
        if draw:
            draw_board(new_state1)
        else:
            print_node(1, parent_state1, m1, new_state1)
        # check if repeated state
        if is_repeated(new_state1):
            continue
        # save the state
        all_states.append(new_state1)

        current_state2 = deepcopy(new_state1)
        # Check if game end
        if is_end(current_state2):
            continue
        # check moves available for 2
        x, y = get_pos(current_state2, 2)
        moves_for_2 = available_moves(current_state2, x, y)
        # check for stagnation (no moves available for 2)
        if len(moves_for_2) == 0:
            continue
        # for all moves available for 2
        for m2 in moves_for_2:
            # move 2
            parent_state2 = deepcopy(current_state2)
            new_state2 = move(parent_state2, 2, m2)
            if draw:
                draw_board(new_state2)
            else:
                print_node(2, parent_state2, m2, new_state2)
            # check if repeated state
            if is_repeated(new_state2):
                continue
            # save the state
            all_states.append(new_state2)

            current_state3 = deepcopy(new_state2)
            # Check if game end
            if is_end(current_state3):
                continue
            # check moves available for 3
            x, y = get_pos(current_state3, 3)
            moves_for_3 = available_moves(current_state3, x, y)
            # check for stagnation (no moves available for 3)
            if len(moves_for_3) == 0:
                continue
            # for all moves available for 3
            for m3 in moves_for_3:
                # move 3
                parent_state3 = deepcopy(current_state3)
                new_state3 = move(parent_state3, 3, m3)
                if draw:
                    draw_board(new_state3)
                else:
                    print_node(3, parent_state3, m3, new_state3)
                # check if repeated state
                if is_repeated(new_state3):
                    continue
                # save the state
                all_states.append(new_state3)

                current_state4 = deepcopy(new_state3)
                # check if game end
                if is_end(current_state4):
                    continue
                # check moves available for 4
                x, y = get_pos(current_state4, 4)
                moves_for_4 = available_moves(current_state4, x, y)
                # check for stagnation (no moves available for 4)
                if len(moves_for_4) == 0:
                    continue
                # for all moves available for 4
                for m4 in moves_for_4:
                    # move 4
                    parent_state4 = deepcopy(current_state4)
                    new_state4 = move(parent_state4, 4, m4)
                    if draw:
                        draw_board(new_state4)
                    else:
                        print_node(4, parent_state4, m4, new_state4)
                    # check if repeated state
                    if is_repeated(new_state4):
                        continue
                    # save the state
                    all_states.append(new_state4)

                    # add to ply states
                    ply_states.append(new_state4)

    levels += 1

    #if levels == 1: break

    #if all(value != 0 for value in winners_dict.values()) and len(winners_dict) >= 4: break


print("Number of levels covered: ", levels)
print("Number of nodes generated: ", len(all_states))
print("Number of winning states (player, wins)",end=": ")
for w in winners_dict.items():
    print(w, end=" ")
print()