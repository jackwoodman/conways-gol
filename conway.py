import time
import math
import random
import copy

CELL_ALIVE = "#"
CELL_DEAD = " "
NEW_LINE = "\n"
LINE = "="
BOARD_SIZE = 55

class Cell:
    board_max = -1

    def __init__(self, position, board_max):
        self.x, self.y = position
        self.board_max = board_max
        self.neighbours = []
        self.isAlive = False

        self.computeNeighbours()


    def computeNeighbours(self):
        # calculate 8 neighbours of this cell
        deltas = [
                (-1, -1), (0, -1), (1, -1),
                (-1, 0),            (1, 0),
                (-1, 1),  (0, 1),  (1, 1)
        ]

        for delt in deltas:
            new_coord = (self.x + delt[0], self.y + delt[1])

            # make sure neighbour would fall within bounds of board
            if (new_coord[0] < self.board_max and new_coord[1] < self.board_max):
                if ((new_coord[0] >= 0 and new_coord[1] >= 0)):
                    self.neighbours.append(new_coord)



def aliveNeighbours(cell, board):
    # count the number of adjacent cells that are alive
    alive_count = 0

    for neighbour in cell.neighbours:
        n_x, n_y = neighbour

        alive_count += (1 if board[n_x][n_y].isAlive else 0)


    return alive_count


def cellSurvives(cell, board):
    # compute whether cell should survive using CGOL rules from Wikipedia

    if (cell.isAlive):
        # if cell is alive and has 2 or 3 neighbours (reproduction)
        if (2 <= aliveNeighbours(cell, board) <= 3):
            return True

    else:
        # if cell is dead but has 3 neighbours (repopulation)
        if (aliveNeighbours(cell, board) == 3):
            return True

    # all other cases, the cell shouldn't survive
    return False


def constructBoard(size):
    # build initial board of given size
    c_board = []

    for x in range(size):
        row = []
        for y in range(size):
            position = (x, y)
            row.append(Cell(position, size))
        c_board.append(row)

    return c_board



def printBoard(board):
    # display board with cells at current state
    board_disp = ""
    line_disp = " " + len(board) * LINE
    print(line_disp)

    for row in board:
        row_disp = "|"

        for cell in row:
            # set pixel based on alive status
            row_disp += (CELL_ALIVE if cell.isAlive else CELL_DEAD)

        row_disp += "|"+ NEW_LINE
        board_disp += row_disp

    # remove trailing newline
    board_disp = board_disp[:-1]
    print(board_disp)
    print(line_disp + "\n")

def updateBoard(board):
    # update whether each cell survives or dies

    init_board = copy.deepcopy(board)

    for row in init_board:
        for cell in row:
            # calculate whether cell should survived based on neighbour status
            board[cell.x][cell.y].isAlive = cellSurvives(cell, init_board)


    return board

def updateCells(board, list, set_to=True):
    # set all cells in list to set_to

    for cell in list:
        board[cell[1]][cell[0]].isAlive = set_to

    return board

def spawnGlider(board, center, go_right=1, go_down=1):
    # spawn a glider at given location
    # go_right = 1 for glider moving right, -1 for moving left
    # go_down = 1 for glider moving down, -1 for moving up

    glider_template = [
                                (1, -1),
                (-1, 0),         (1, 0),
                        (0, 1),  (1, 1)
    ]

    for delt in glider_template:
        new_coord = (center[0] + (go_right * delt[0]), center[1] + (go_down * delt[1]))

        board[new_coord[1]][new_coord[0]].isAlive = True

    return board

def spawnBlinker(board, center):
    # spawn blinkert oscillator at given location

    blinker_template = [
        (-1, 0), (0, 0), (1, 0)
    ]

    for delt in blinker_template:
        new_coord = (center[0] + delt[0], center[1] + delt[1])

        board[new_coord[1]][new_coord[0]].isAlive = True

    return board

# =========================================================================

# build initial board
board = constructBoard(BOARD_SIZE)

# spawn some oscillators randomly
blinker_count = 3
for b in range(blinker_count):
    rand_co = (random.randint(1, BOARD_SIZE - 1), random.randint(1, BOARD_SIZE - 1))
    board = spawnBlinker(board, rand_co)

# spawn some gliders randomly
glider_count, glider_border = 5, 4
for g in range(glider_count):
    vert, hori = random.choice([-1,1]), random.choice([-1,1])
    rand_co = (random.randint(1, BOARD_SIZE - glider_border), random.randint(1, BOARD_SIZE - glider_border))
    board = spawnGlider(board, rand_co, vert, hori)

printBoard(board)
while True:
    time.sleep(0.1)
    board = updateBoard(board)
    printBoard(board)
