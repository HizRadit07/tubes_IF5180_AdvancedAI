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
    if len(myPlayer.backtrack_stack) > 0 and myPlayer.backtrack_stack[-1] == (myPlayer.x, myPlayer.y):
        if myPlayer.prev_move == "S": # menabrak tembok bawah, sekarang player tahu jml baris board
            myPlayer.board_nbrows = myPlayer.x + 1
            myPlayer.memory.pop((myPlayer.x + 1, myPlayer.y), "")
        elif myPlayer.prev_move == "D": # menabrak tembok kanan, sekarang player tahu jml kolom board
            myPlayer.board_nbcols = myPlayer.y + 1
            myPlayer.memory.pop((myPlayer.x, myPlayer.y + 1), "")
        myPlayer.backtrack_stack.pop()
    else: # player berhasil bergerak pada move sebelumnya
        to_apply = 0
        if myPlayer.percept["stench"]:
            to_apply += 1
        if myPlayer.percept["breeze"]:
            to_apply += 2

        updated_coordinates: list[tuple[int, int]] = []
        if myPlayer.x > 0:
            updated_coordinates.append((myPlayer.x-1, myPlayer.y))
        if myPlayer.y > 0:
            updated_coordinates.append((myPlayer.x, myPlayer.y-1))
        if myPlayer.board_nbrows < 0 or myPlayer.x < myPlayer.board_nbrows - 1:
            updated_coordinates.append((myPlayer.x+1, myPlayer.y))
        if myPlayer.board_nbcols < 0 or myPlayer.y < myPlayer.board_nbcols - 1:
            updated_coordinates.append((myPlayer.x, myPlayer.y+1))

        for pos in updated_coordinates:
            if not(pos in myPlayer.memory):
                myPlayer.memory[pos] = 3
            # print(pos, ":", myPlayer.memory[pos])
            add_to_stack = (myPlayer.memory[pos] > 0)
            myPlayer.memory[pos] = (myPlayer.memory[pos] & to_apply)
            # print(pos, ":", myPlayer.memory[pos])
            add_to_stack = add_to_stack and (myPlayer.memory[pos] == 0)
            if add_to_stack:    
                myPlayer.safe_unvisited_stack.append(pos)
    
    # Memutuskan move
    myPlayer.prev_x = myPlayer.x
    myPlayer.prev_y = myPlayer.y
    possible_moves = {
        (myPlayer.x-1, myPlayer.y): "W",
        (myPlayer.x, myPlayer.y-1): "A",
        (myPlayer.x+1, myPlayer.y): "S",
        (myPlayer.x, myPlayer.y+1): "D",
    }

    while len(myPlayer.safe_unvisited_stack) > 0 and (
        myPlayer.safe_unvisited_stack[-1][0] == myPlayer.board_nbrows or myPlayer.safe_unvisited_stack[-1][1] == myPlayer.board_nbcols
    ):
        myPlayer.safe_unvisited_stack.pop()
    # print("myPlayer.safe_unvisited_stack", myPlayer.safe_unvisited_stack)
    if len(myPlayer.safe_unvisited_stack) == 0:
        # Player tidak punya cell yang 100% aman, kemungkinan kecil
        # Hanya terjadi saat wumpus dan pit mengelilingi posisi awal pemain, atau posisi akhir gold
        myPlayer.prev_move = random.choice(["W", "A", "S", "D"])
        myPlayer.backtrack_stack.append((myPlayer.x, myPlayer.y))
    elif myPlayer.safe_unvisited_stack[-1] in possible_moves: 
        # Jalan ke cell aman yang belum terkunjungi
        myPlayer.prev_move = possible_moves[myPlayer.safe_unvisited_stack[-1]]
        myPlayer.safe_unvisited_stack.pop()
        myPlayer.backtrack_stack.append((myPlayer.x, myPlayer.y))
    else: # Backtrack
        myPlayer.prev_move = possible_moves[myPlayer.backtrack_stack[-1]]
        myPlayer.backtrack_stack.pop()

    return myPlayer.prev_move