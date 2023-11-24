import heapq

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

        # Atribut baru

        # Untuk board size, player dapat mengetahui dari apakah move dia sebelumnya menempatkan pada posisi yang sama atau tidak
        # Setelah tau informasi baru ini, player menempatkan pada board_nbrows atau board_nbcols
        self.cell_should_be: tuple = (x, y)
        self.move_str: str = ""
        self.board_nbrows: int = -1
        self.board_nbcols: int = -1

        # Untuk keperluan Search dan memori player akan potensi cell
        self.memory: dict[tuple[int, int], tuple[int, int, bool]] = {(x, y): (0, 0, False)}
        # Nilai pertama dalam tuple berisi bitmask 4 nilai dengan detail:
        # 0 untuk safe cell
        # 1 untuk safe atau Wumpus cell
        # 2 untuk safe atau Pit cell
        # 3 untuk bisa safe, Wumpus, atau Pit cell
        # Perhatikan bahwa operasi bitwise or dapat dimanfaatkan disini
        # Nilai kedua bernilai confidence dari bitmask tersebut 
        # (bernilai 1 hingga 4, tergantung banyaknya neighboring cell yang telah divisit)
        # Nilai ketiga bernilai apakah cell ini telah dipijak atau belum

        # Struktur tree
        self.root_cell: tuple = (x, y)
        self.cell_parent: dict[tuple[int, int], tuple[int, int]] = {(x, y): None}
        self.cell_depth: dict[tuple[int, int], int] = {(x, y): 0}
        self.unvisited_cells: list[list[tuple[int, int]]] = [[] for i in range(5)] 

        self.mode: str = "DFS"
        # self.mode: str = "BFS"
    
    # Metode baru
    def check_current_cell(self):
        if self.cell_should_be == (self.x, self.y):
            return True
        if self.cell_should_be[0] > self.x:
            self.board_nbrows = self.cell_should_be[0]
        else: # self.cell_should_be[1] > self.y
            self.board_nbcols = self.cell_should_be[1]
        self.memory.pop(self.cell_should_be, "")
        self.cell_parent.pop(self.cell_should_be, "")
        self.cell_depth.pop(self.cell_should_be, "")
        return False

    def update_near_cells(self):
        if self.memory[(self.x, self.y)][2]: # Sudah diexpand sebelumnya
            return
        # Belum diexpand sebelumnya
        to_apply = 0
        if self.percept["stench"]:
            to_apply += 1
        if self.percept["breeze"]:
            to_apply += 2
        # Mengumpulkan semua koordinat tetangga yang akan diupdate nilainya
        updated_coordinates: list[tuple[int, int]] = []
        if self.x > 0:
            updated_coordinates.append((self.x-1, self.y))
        if self.y > 0:
            updated_coordinates.append((self.x, self.y-1))
        if self.board_nbrows < 0 or self.x < self.board_nbrows - 1:
            updated_coordinates.append((self.x+1, self.y))
        if self.board_nbcols < 0 or self.y < self.board_nbcols - 1:
            updated_coordinates.append((self.x, self.y+1))
        for pos in updated_coordinates: # Iterasi untuk semua tetangga
            if pos in self.memory:
                # Jika tetangga belum pernah diexpand, hapus dari unvisited_cells
                info: tuple[int, int, bool] = self.memory[pos]
                if not info[2]:
                    if info[0] > 0:
                        self.unvisited_cells[info[1]].remove(pos)
                    self.cell_parent[pos] = (self.x, self.y)
                    self.cell_depth[pos] = self.cell_depth[(self.x, self.y)]+1
            else: # Tetangga belum ada dalam memori, tambahkan dalam tree
                self.memory[pos] = (3, 0, False)
                self.cell_parent[pos] = (self.x, self.y)
                self.cell_depth[pos] = self.cell_depth[(self.x, self.y)]+1
            # Update dan masukkan dalam unvisited_cells
            new_memory: tuple[int, int, bool] = ((self.memory[pos][0] & to_apply), self.memory[pos][1] + 1, self.memory[pos][2])
            if not new_memory[2]:
                if new_memory[0] > 0:
                    self.unvisited_cells[new_memory[1]].append(pos)
                elif self.memory[pos][0] > 0:
                    self.unvisited_cells[0].append(pos)
            self.memory[pos] = new_memory
        info: tuple[int, int, bool] = self.memory[(self.x, self.y)]
        self.memory[(self.x, self.y)] = (info[0], info[1], True)

    def determine_cell_to_move(self):
        unvisited_cells_idx: int = 0
        while unvisited_cells_idx < 5 and len(self.unvisited_cells[unvisited_cells_idx]) == 0:
            unvisited_cells_idx += 1
        if unvisited_cells_idx > 4:
            raise Exception("No gold in board")
        
        if self.mode == "DFS": # Perlakukan unvisited_cells layaknya stack
            destination: tuple[int, int] = self.unvisited_cells[unvisited_cells_idx][-1]
        elif self.mode == "BFS": # Perlakukan unvisited_cells layaknya queue
            destination: tuple[int, int] = self.unvisited_cells[unvisited_cells_idx][0]
        else:
            raise Exception("Invalid search mode")
        # print("destinasi", destination)
        
        if self.cell_parent[destination] == (self.x, self.y): # Bisa langsung menuju unvisited cell
            self.cell_should_be = destination
            if self.mode == "DFS": # Perlakukan unvisited_cells layaknya stack
                self.unvisited_cells[unvisited_cells_idx].pop()
            elif self.mode == "BFS": # Perlakukan unvisited_cells layaknya queue
                self.unvisited_cells[unvisited_cells_idx].pop(0)
        else: # Cek apakah posisi sekarang merupakan ancestor dari destination
            while self.cell_depth[destination] > self.cell_depth[(self.x, self.y)] + 1:
                destination = self.cell_parent[destination]
            if self.cell_parent[destination] == (self.x, self.y):
                self.cell_should_be = destination
            else:
                self.cell_should_be = self.cell_parent[(self.x, self.y)]
        self.move_str: dict[tuple[int, int], str] = {
            (self.x-1, self.y): "W",
            (self.x, self.y-1): "A",
            (self.x+1, self.y): "S",
            (self.x, self.y+1): "D",
        }[self.cell_should_be]
    
    def print_tree(self):
        nbrows: int = 0
        nbcols: int = 0
        for pos in self.memory:
            nbrows = max(nbrows, pos[0])
            nbcols = max(nbcols, pos[1])
        digrows: int = len(str(nbrows))
        digcols: int = len(str(nbcols))
        for i in range(nbrows + 1):
            for j in range(nbcols + 1):
                if i>0:
                    if self.cell_parent.get((i,j), None) == (i-1,j):
                        print(' '*(digrows+1) + '|' + ' '*(digcols+2), end='')
                    elif self.cell_parent.get((i-1,j), None) == (i,j):
                        print(' '*(digrows+1) + '|' + ' '*(digcols+2), end='')
                    else:
                        print(' '*(digrows + digcols + 4), end='')
                else:
                    print(' '*(digrows + digcols + 4), end='')
            print()
            for j in range(nbcols + 1):
                if j>0:
                    if self.cell_parent.get((i,j), None) == (i,j-1):
                        print('-', end='')
                    elif self.cell_parent.get((i,j-1), None) == (i,j):
                        print('-', end='')
                    else:
                        print(' ', end='')

                if (i,j) in self.memory:
                    print(' '*(digrows - len(str(i)) + 1) + str(i) + ',' + str(j) + ' '*(digcols - len(str(j)) + 1), end='')
                else:
                    print(' '*(digrows + digcols + 3), end='')
            print()
            

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
                self.print_tree()
                return True
        for pit in listPit:
            if self.x == pit.x and self.y == pit.y:
                print("======================\nYou fall into the pit. You lose 😭")
                self.print_tree()
                return True
        if self.x == gold.x and self.y == gold.y:
            print("======================\nCongratulations, you win 😄")
            self.print_tree()
            return True
        return False
    