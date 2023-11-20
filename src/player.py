class Player(object):
    # Kelas Player ini boleh ditambahkan atribut/ method lain, tapi jangan menghapus/ mengubah kode yang sudah ada
    # You can add other attributes and/or methods to this Player class, but don't delete or change the existing code.
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.num_movement = 0
        self.percept = {
            "stench" : False,
            "breeze": False,
        }
        self.previous_move = [] # simulate a stack of moves
        self.previous_position = (0,0)
        self.is_visited = [(0,0)]
        self.last_move_is_bump = False

    def move(self, board, direction):
        board.update_board(self.x, self.y, board.board_static[self.x][self.y])

        if direction=="W" and self.x > 0:
            self.x = self.x-1
        elif direction=="A" and self.y > 0:
            self.y = self.y - 1
        elif direction=="S" and self.x < board.size-1:
            self.x = self.x + 1
        elif direction=="D" and self.y < board.size-1:
            self.y = self.y+1


        board.update_board(self.x, self.y, "P")
        self.percept["stench"] = board.board_static[self.x][self.y] == "~" or board.board_static[self.x][self.y] == "≌"
        self.percept["breeze"] = board.board_static[self.x][self.y] == "=" or board.board_static[self.x][self.y] == "≌"

    def is_finished(self, listWumpus, listPit, gold):
        for wumpus in listWumpus:
            if self.x == wumpus.x and self.y == wumpus.y:
                print("======================\nYou are eaten by Wumpus. You lose 😭")
                return True
        for pit in listPit:
            if self.x == pit.x and self.y == pit.y:
                print("======================\nYou fall into the pit. You lose 😭")
                return True
        if self.x == gold.x and self.y == gold.y:
            print("======================\nCongratulations, you win 😄")
            return True
        return False