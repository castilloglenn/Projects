import numpy as np
import random as r
import time, os

# default values, snake length = 4, bait/snake initial position
SNAKE_LENGTH = 10
base_board = [[0 for x in range(30)] for y in range(15)]
head = (len(base_board) // 2, len(base_board[0]) // 3)
snake = [(head[0], head[1] - x) for x in range(1, SNAKE_LENGTH)]
snake.insert(0, head)
bait = [len(base_board) // 2, int(head[1] * 2.5)]
foods = ["♥"]
bait_logo = foods[0]


# =============VISUALS=================#
def display(board):
    print(" ┏" + "━━️" * (len(base_board) + 3) + "┓")
    for row in board:
        print(" |", end="")
        for column in row:
            if column == 1:
                print("◼️", end="")
            elif column == 2:
                print(bait_logo, end="")
            else:
                print(" ", end=" ")
        print("|")
    print(" ┗" + "━️━" * (len(base_board) + 3) + "┛")


def add_objects():
    for segment in snake:
        base_board[segment[0]][segment[1]] = 1
    base_board[bait[0]][bait[1]] = 2


def clear_board():
    for row in range(len(base_board)):
        for column in range(len(base_board[row])):
            base_board[row][column] = 0


# ==============LOGIC==================#
def pathfind():
    open = {}
    closed = {}
    trav = snake[0]
    while trav[0] != bait[0] or trav[1] != bait[1]:
        valids = get_valid_adjacent(trav)
        for valid in valids:
            fcost = calc_fcost(valid)
            if valid not in closed:
                open[valid] = fcost
        if open == {}:
            return -1
        lowest = min(open, key=open.get)
        closed[lowest] = open[lowest]
        del open[lowest]
        trav = lowest
    path = find_path(closed, [min(closed, key=closed.get)], 20, max(closed, key=closed.get))
    return path


def find_path(path, final, trav, first):
    path_list = [(k, v) for k, v in path.items()]  # list version
    batch = [x for x, y in path.items() if y == trav]  # traversal
    adjacent = get_adjacent(final[0])  # adjacent to the last

    if len(path_list) == 1:
        return path_list[0]

    if batch == []:  # wrong path / out of bounds
        return False

    adj = [x for x in batch if x in adjacent]
    if adj == []:
        find_path(path, final, trav - 20, first)
    else:
        for coord in adj:
            final.insert(0, coord)
            temp_path = path.copy()
            del temp_path[coord]
            result = find_path(temp_path, final, trav + 10, first)
            if result != False:
                break
    return final


def get_adjacent(coord):
    adjacents = [(coord[0] - 1, coord[1]), (coord[0], coord[1] + 1), (coord[0] + 1, coord[1]), (coord[0], coord[1] - 1)]
    return adjacents


def get_valid_adjacent(coord):
    valid = []
    corners = get_adjacent(coord)
    for corner in corners:
        try:
            if corner[0] < 0 or corner[1] < 0 or corner in snake:
                pass
            elif base_board[corner[0]][corner[1]] == 0 or base_board[corner[0]][corner[1]] == 2:
                valid.append(corner)
        except IndexError:
            pass
    return valid


def calc_fcost(coord):
    abs_x, abs_y = abs(bait[0] - coord[0]), abs(bait[1] - coord[1])
    gcost = 10  # 4-way direction only
    hcost = (abs_x + abs_y) * gcost
    fcost = gcost + hcost
    return fcost


def move(coord):
    global bait_logo
    if coord == -1:
        return coord
    if coord[0] == bait[0] and coord[1] == bait[1]:
        generate_bait()
        bait_logo = r.choice(foods)
        snake.append(snake[len(snake) - 1])
    for segment in range(1, len(snake)):
        snake[len(snake) - segment] = snake[len(snake) - segment - 1]
    snake[0] = coord


def generate_bait():
    while True:
        x, y = r.randint(0, len(base_board) - 1), r.randint(0, len(base_board[0]) - 1)
        if base_board[x][y] == 0:
            bait[0], bait[1] = x, y
            break


# ==============TESTS==================#
def test():
    while True:
        os.system("cls")
        display(base_board)
        result = move(generate_move())
        if result == -1:
            break
        clear_board()
        add_objects()
        time.sleep(0.05)  # 0.5 = SLOW, 0.3 = MEDIUM, 0.1 = FAST FPS


def generate_move():
    valid = get_valid_adjacent(snake[0])
    if valid == []:
        return -1
    return r.choice(valid)


# ============MAIN=METHOD==============#
def main():
    while True:
        os.system("cls")
        display(base_board)
        path = pathfind()
        if path == -1:
            break
        move(path[0])
        clear_board()
        add_objects()
        time.sleep(0.07)


if __name__ == "__main__":
    main()
