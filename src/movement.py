import random
from player import *
import time

def movement(myPlayer: Player):
    while True:
        time.sleep(.3)
        print("Chosen move: ", end="")
        move = select_movement(myPlayer).upper()
        # move = input("select move: ").upper()
        # move = select_movement(myPlayer)
        if move in ["W", "A", "S", "D"]:
            print(move)
            break

    return move

def select_movement(myPlayer: Player):
    cur_position = (myPlayer.x, myPlayer.y)
    if cur_position not in myPlayer.is_visited:
        myPlayer.is_visited.append(cur_position)

    possible_moves = [
        (myPlayer.x, myPlayer.y - 1),
        (myPlayer.x - 1, myPlayer.y),
        (myPlayer.x, myPlayer.y + 1),
        (myPlayer.x + 1, myPlayer.y),
    ]  # positions for W, A, S, D

    myPlayer.last_move_is_bump = myPlayer.num_movement > 0 and myPlayer.previous_position == cur_position
    if myPlayer.last_move_is_bump:
        myPlayer.previous_move.pop()

    can_move = False

    for move in possible_moves:
        if move not in myPlayer.is_visited:
            next_move = move
            can_move = True
            break
    
    if myPlayer.percept['stench'] or myPlayer.percept['breeze']:
        can_move = False

    if can_move:
        # Update is_visited
        if next_move not in myPlayer.is_visited:
            myPlayer.is_visited.append(next_move)

        myPlayer.previous_position = cur_position

        # Calculate movement direction based on the difference between current position and next move
        movement_diff = (next_move[0] - myPlayer.x, next_move[1] - myPlayer.y)
        
        if movement_diff == (0, 1):
            myPlayer.previous_move.append("D")
            return "D"
        elif movement_diff == (-1, 0):
            myPlayer.previous_move.append("W")
            return "W"
        elif movement_diff == (0, -1):
            myPlayer.previous_move.append("A")
            return "A"
        else:
            # if not(myPlayer.last_move_is_bump):
            myPlayer.previous_move.append("S")
            return "S"
    else:
        last_move = myPlayer.previous_move.pop()
        return backtrack_one_move(last_move)


def backtrack_one_move(last_move):
    if last_move == "W":
        return "S"
    elif last_move == "S":
        return "W"
    elif last_move == "D":
        return "A"
    elif last_move == "A":
        return "D"
    
    return random.choice(['W','A','S','D'])

def find_closest_node(myPlayer:Player):
    closest_loc = [(myPlayer.x+1,myPlayer.y), (myPlayer.x-1,myPlayer.y), (myPlayer.x,myPlayer.y+1), (myPlayer.x,myPlayer.y-1)]


    # move = input("input a move: ").upper()

    # cur_loc = (myPlayer.x, myPlayer.y)

    # if not(cur_loc) in myPlayer.visited:
    #     myPlayer.visited.append(cur_loc)

    # safe_locs = [(myPlayer.x+1,myPlayer.y), (myPlayer.x-1,myPlayer.y), (myPlayer.x,myPlayer.y+1), (myPlayer.x,myPlayer.y-1)]
    
    # if (not(myPlayer.percept['stench']) and not(myPlayer.percept['breeze'])):
    #     for item in safe_locs:
    #         if not(item in myPlayer.safe_loc):
    #             myPlayer.safe_loc.append(item)
    # else: #either stench or breeze is percepted
    #     unsafe_loc = safe_locs.copy()
    #     if myPlayer.percept['stench']:
    #         for item in unsafe_loc:
    #             if not(item in myPlayer.visited) and not(item in myPlayer.potential_wumpus_loc):
    #                 myPlayer.potential_wumpus_loc.append(item)
    #     if myPlayer.percept['breeze']:
    #         for item in unsafe_loc:
    #             if not(item in myPlayer.visited) and not(item in myPlayer.potential_pit_loc):
    #                 myPlayer.potential_pit_loc.append(item)
    