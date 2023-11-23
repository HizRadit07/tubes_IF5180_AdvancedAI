import random

def movement(myPlayer):
    while True:
        print("Chosen move: ", end="")
        move = select_movement(myPlayer).upper()
        if move in ["W", "A", "S", "D"]:
            print(move)
            break

    return move

def select_movement(myPlayer):
    myPlayer.check_current_cell()
    myPlayer.update_near_cells()
    myPlayer.determine_cell_to_move()
    # for i in range(4):
    #     print(i, ":", myPlayer.unvisited_cells[i])
    # print("Mau jalan ke", myPlayer.cell_should_be)
    # input("Lanjut?")
    return myPlayer.move_str