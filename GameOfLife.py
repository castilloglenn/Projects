import numpy as np
import time, os


# BOARD DIMENSIONS / STATEMENTS
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
    for row in current:
        for column in row:
            if column == 1:
                print("◼", end=" ")
            else:
                print(" ", end=" ")
        print()     # end row


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


def setup_board():
    # BLINKER
    #board[5][5] = 1
    #board[5][6] = 1
    #board[5][7] = 1
    # GLIDER #1
    board[6][5] = 1
    board[7][5] = 1
    board[8][5] = 1
    board[8][4] = 1
    board[7][3] = 1
    # GLIDER #2
    board[16][15] = 1
    board[17][15] = 1
    board[18][15] = 1
    board[18][14] = 1
    board[17][13] = 1


def main():
    setup_board()
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print_gen(board)
        alive = get_alive_coordinates()
        valid = get_all_valid_coordinates(alive)
        evaluate_cells(valid)
        copy_board()
        time.sleep(0.2)


if __name__ == "__main__":
    main()
