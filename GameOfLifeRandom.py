import numpy as np
import random as r
import time, os


# BOARD DIMENSIONS / STATEMENTS
gen = 1
BOARD_LENGTH = 60
BOARD_WIDTH = 40
board = [[0 for y in range(0, BOARD_LENGTH)] for x in range(0, BOARD_WIDTH)]
next_board = np.copy(board)
# adjacent identifier arranged as follows: NW, N, NE, W, E, SW, S, SE
adjacent = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


def copy_board():
    global board
    board = np.copy(next_board)


def print_gen(current):
    global gen
    for row in current:
        for column in row:
            if column == 1:
                print("◼", end=" ")
            else:
                print(" ", end=" ")
        print()     # end row
    print("GENERATION ", gen)
    gen += 1


def get_alive_coordinates():
    alive_coordinates = []
    for x in range(0, BOARD_WIDTH):
        for y in range(0, BOARD_LENGTH):
            if board[x][y] == 1:
                alive_coordinates.append((x, y))
    return alive_coordinates


# this function gathers all alive cells and their neighbors to be evaluated
def get_all_valid_coordinates(alive_coordinates):
    cells = []
    for coordinate in alive_coordinates:
        for calculation in adjacent:
            try:
                if (coordinate[0] + calculation[0], coordinate[1] + calculation[1]) not in cells:
                    cells.append((coordinate[0] + calculation[0], coordinate[1] + calculation[1]))
            except IndexError:
                pass
    return cells


def get_neighbors_count(coordinate):
    count = 0
    for calculation in adjacent:
        try:
            if board[coordinate[0] + calculation[0]][coordinate[1] + calculation[1]] == 1:
                count += 1
        except IndexError:
            pass
    return count


def evaluate_cells(cells):
    for cell in cells:
        neighbor_count = get_neighbors_count(cell)
        try:
            if board[cell[0]][cell[1]] == 0 and neighbor_count == 3:
                next_board[cell[0]][cell[1]] = 1
            elif board[cell[0]][cell[1]] == 1 and (neighbor_count < 2 or neighbor_count > 3):
                next_board[cell[0]][cell[1]] = 0
            else:
                next_board[cell[0]][cell[1]] = board[cell[0]][cell[1]]
        except IndexError:
            pass


def setup_board(quantity):
    added = []
    while quantity > 0:
        x = r.randint(0, BOARD_WIDTH - 1)
        y = r.randint(0, BOARD_LENGTH - 1)
        if (x, y) not in added:
            board[x][y] = 1
            added.append((x, y))
        quantity -= 1


def main():
    setup_board(400)
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print_gen(board)
        alive = get_alive_coordinates()
        valid = get_all_valid_coordinates(alive)
        evaluate_cells(valid)
        copy_board()


if __name__ == "__main__":
    main()
