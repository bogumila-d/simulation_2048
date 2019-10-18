import random
import game
import sys
import numpy as np


# Author:      chrn (original by nneonneo)
# Date:        11.11.2016
# Copyright:   Algorithm from https://github.com/nneonneo/2048-ai
# Description: The logic to beat the game. Based on expectimax algorithm.

import heuristicai as heuristic

def find_best_move(board):
    """
    find the best move for the next turn.
    """
    bestmove = -1
    UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3
    move_args = [UP, DOWN, LEFT, RIGHT]

    result = [score_toplevel_move(i, board) for i in range(len(move_args))]
    bestmove = result.index(max(result))
    newboard = execute_move(bestmove, board)

    if board_equals(board, newboard):
        bestmove = heuristic.find_best_move_random_agent()

    for m in move_args:
        print("move: %d score: %.4f" % (m, result[m]))

    return bestmove


def score_toplevel_move(move, board):
    """
    Entry Point to score the first move.
    """
    newboard = execute_move(move, board)
    result = 0
    print(newboard)
    zeros = count_zeros(newboard)

    result += verify_external_rows(board, zeros, result, 0)
    result += verify_external_rows(board, zeros, result, 3)
    result += verify_external_cols(board, zeros, result)


    if board_equals(board, newboard):
        return 0
    # TODO:
    # Implement the Expectimax Algorithm.
    # 1.) Start the recursion until it reach a certain depth

    deepth = 0
    while deepth > 3:
        result += heuristic.get_result(board)
        score_toplevel_move(find_best_move(board), newboard)
        deepth += 1
    # 2.) When you don't reach the last depth, get all possible board states and
    #	calculate their scores dependence of the probability this will occur. (recursively)
    # 3.) When you reach the leaf calculate the board score with your heuristic.
    return result


def verify_external_cols(board, zeros, result):
    if board[1][0] == 0:
        result += sum_result(board, result, 1, 0, zeros)
    if board[1][3] == 0:
        result += sum_result(board, result, 1, 3, zeros)
    if board[2][0] == 0:
        result += sum_result(board, result, 2, 0, zeros)
    if board[2][3] == 0:
        result += sum_result(board, result, 2, 3, zeros)
    return result


def verify_external_rows(board, zeros, result, row_n):
    for i in range(4):
        if board[row_n][i] == 0:
            sum_result(board, result, row_n, i, zeros)
    return result


def sum_result(board, result, tile_row, tile_col, zeros):
    prob_board = board
    prob_board[tile_row][tile_col] = 2
    result += (heuristic.verify_board(prob_board) * 0.9) / zeros
    prob_board = board
    prob_board[tile_row][tile_col] = 4
    result += (heuristic.verify_board(prob_board) * 0.1) / zeros
    prob_board[tile_row][tile_col] = 0
    return result


def count_zeros(board):
    zeros = 0
    zeros += 4 - np.count_nonzero(board[0])
    zeros += 4 - np.count_nonzero(board[3])
    if board[1][0] == 0:
        zeros += 1
    if board[1][3] == 0:
        zeros += 1
    if board[2][0] == 0:
        zeros += 1
    if board[2][3] == 0:
        zeros += 1
    return zeros


def execute_move(move, board):
    """
    move and return the grid without a new random tile 
    It won't affect the state of the game in the browser.
    """

    UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3

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
