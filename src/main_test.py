import random

from board import *
from gold import *
from player import *
from wumpus import *
from movement import *
from pit import *

def main():
    # Print header
    print("⭐⭐WELCOME TO IF5080 SIMPLE WUMPUS WORLD⭐⭐")

    # Set board and player
    board_size = 5
    myBoard = Board(board_size)
    myPlayer = Player()

    # create wumpuses and pits
    listWumpus = []
    listPit = []
    enemyPoint = []
    while len(listWumpus) < 1:
        point = [random.randint(2, board_size - 1), random.randint(2, board_size - 1)]
        point = 2,2
        if point not in enemyPoint:
            enemyPoint.append(point)
            wumpus = Wumpus(point[0], point[1])
            listWumpus.append(wumpus)
    while len(listPit) < 1:
        point = [random.randint(2, board_size - 1), random.randint(2, board_size - 1)]
        point = 3,4
        if point not in enemyPoint:
            enemyPoint.append(point)
            pit = Pit(point[0], point[1])
            listPit.append(pit)

    #create gold
    while True:
        #goldPoint = [random.randint(7, board_size - 1), random.randint(4, board_size - 1)]
        goldPoint = 4,3
        if goldPoint not in enemyPoint:
            gold = Gold(goldPoint[0], goldPoint[1])
            break

    myBoard.init_board(myPlayer, listWumpus, listPit, gold)

    while True:
        print()
        myBoard.print_board()
        print("Number of player moves:", myPlayer.num_movement)
        print("Player perception:", myPlayer.percept)
        dir = movement(myPlayer)
        myPlayer.num_movement += 1
        myPlayer.move(myBoard, dir)

        if myPlayer.is_finished(listWumpus, listPit, gold):
            break
main()