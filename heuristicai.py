import random
import game
import sys
import numpy as np

UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3


def find_best_move(board):
    return verify_best_move(board)


def find_best_move_random_agent():
    return random.choice([UP, DOWN, LEFT, RIGHT])


def verify_best_move(board):
    boards = [board for x in range(4)]
    directions = [x for x in range(4)]
    alternative_move = [0 for x in range(4)]

    maximum = 0
    best_move = 0
    for index in range(len(directions) - 1):
        boards[index] = execute_move(index, board)
        if board_equals(board, boards[index]):
            directions.remove(index)
            continue

        result = verify_score(boards[index])
        result = verify_edge(boards[index], result)
        result += verify_zeros(boards, index)
        result += verify_two_first_col(board)

        if result > maximum:
            maximum = result
            alternative_move[index] = result
            best_move = index

    if best_move == 1 or best_move == 3:
        best_move = find_alternative_move(alternative_move, best_move)
    best_move = find_random_move_if_necessary(best_move, board)

    return best_move


def verify_board(board):
    result = verify_score(board)
    result = verify_edge(board, result)
    result += verify_two_first_col(board)
    return result


def find_random_move_if_necessary(best_move, board):
    newboard = execute_move(best_move, board)
    if board_equals(board, newboard):
        best_move = find_best_move_random_agent()
    return best_move


def find_alternative_move(alternative_move, best_move):
    if alternative_move[best_move] == alternative_move[best_move - 1]:
        best_move = best_move - 1
    return best_move


def verify_score(board):
    result = 0
    result += check_row_result(board, result)
    result += check_row_result(board.T, result)
    return result


def verify_edge(board, result):
    maximum = np.amax(board)
    val_left_top = board[0][0]
    val_left_sec = board[1][0]
    val_left_third = board[2][0]
    val_left_fourth = board[3][0]
    val_top_sec = board[0][1]

    if check_corner(board, maximum):
        return result
    if check_first_column(board, maximum):
        return result + val_left_top + val_left_sec + val_left_third + val_left_fourth
    return result + val_left_top + val_left_sec/2 + val_left_third/4 + val_top_sec/2


def verify_zeros(boards, index):
    return len(boards[index][boards[index] == 0])


def verify_two_first_col(board):
    result = 0
    for row in board:
        row = list(filter(lambda a: a != 0, row))
        if len(row) >= 2 and row[0] == row[1]:
            result += 4*row[0]
    return result


def check_corner(board, maximum):
    val_left_top = board[0][0]
    val_left_sec = board[1][0]
    val_top_sec = board[0][1]
    return val_left_top == 0 or val_top_sec == 0 or val_left_sec == 0 or val_left_top * 2 <= maximum


def check_first_column(board, maximum):
    val_left_top = board[0][0]
    val_left_sec = board[1][0]
    val_left_third = board[2][0]
    return val_left_top == maximum and val_left_sec * 2 >= maximum and val_left_third * 4 >= maximum


def check_row_result(board, result):
    for row in board:
        row = list(filter(lambda a: a != 0, row))
        if len(row) < 2:
            return result
        for i in (1, len(row) - 1):
            if row[i] == row[i - 1]:
                result += row[i]
    return result


def execute_move(move, board):
    """
    move and return the grid without a new random tile
	It won't affect the state of the game in the browser.
    """
    if move == UP:
        return game.merge_up(board)
    elif move == DOWN:
        return game.merge_down(board)
    elif move == LEFT:
        return game.merge_left(board)
    elif move == RIGHT:
        return game.merge_right(board)
    else:
        sys.exit("No valid move")


def board_equals(board, newboard):
    """
    Check if two boards are equal
    """
    return (newboard == board).all()
