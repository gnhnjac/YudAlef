from flask import Flask, render_template, request, redirect, url_for, jsonify, logging
import copy
import json
import logging
import os

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)

app.env = 'development'

app.secret_key = os.urandom(24)#Flask.secret_key
global board
board = []


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/tictactoe')
def tictactoe():
    global board
    board = [[0, 0, 0],
             [0, 0, 0],
             [0, 0, 0]]

    return render_template('tictactoe.html')


# Tic tac toe win


def checkWin_ttt(game_board):
    for i in range(len(game_board)):

        if game_board[i][0] == 0:
            continue

        if game_board[i][0] == game_board[i][1] and game_board[i][1] == game_board[i][2]:
            return {'winner': game_board[i][0], 'index1': [i, 0], 'index2': [i, 2]}

    for j in range(len(game_board[0])):

        if game_board[0][j] == 0:
            continue

        if game_board[0][j] == game_board[1][j] and game_board[1][j] == game_board[2][j]:
            return {'winner': game_board[0][j], 'index1': [0, j], 'index2': [2, j]}

    if game_board[0][0] == game_board[1][1] and game_board[1][1] == game_board[2][2] and game_board[0][0] != 0:
        return {'winner': game_board[0][0], 'index1': [0, 0], 'index2': [2, 2]}

    if game_board[0][2] == game_board[1][1] and game_board[1][1] == game_board[2][0] and game_board[0][2] != 0:
        return {'winner': game_board[0][2], 'index1': [0, 2], 'index2': [2, 0]}

    tie = 0
    for i in range(len(game_board)):

        for j in range(len(game_board[0])):

            if (game_board[i][j] != 0):
                tie += 1

    if (tie == 9):
        return {'winner': 0}

    return {'winner': -1}


# Tic tac toe minimax


def minimax_ttt(current_node, game_board):
    state = checkWin_ttt(game_board)['winner']

    # Player wins (Bad)
    if state == 1:
        return -1

    # Machine wins (Good)
    elif state == 2:
        return 1

    # Tie (Okay)
    elif state == 0:
        return 0

    cost_tree = {}

    for i in range(len(game_board)):

        for j in range(len(game_board[0])):

            if game_board[i][j] == 0:

                game_board[i][j] = 1 if current_node == False else 2

                cost = minimax_ttt(not current_node, game_board)

                game_board[i][j] = 0

                if isinstance(cost, tuple):
                    cost = cost[0]

                cost_tree[cost] = [i, j]

                if current_node == False and cost == -1:
                    break

                elif current_node == True and cost == 1:
                    break

    return max(cost_tree) if current_node == True else min(cost_tree), cost_tree[max(cost_tree)]


@app.route('/tictactoe/board/set/<int:row>,<int:column>')
def tictacset(row, column):
    if (board[row][column] != 0):
        return jsonify(success=False), 404

    board[row][column] = 1

    state = checkWin_ttt(board)

    # tie
    if (state['winner'] != -1):
        return jsonify(state=state['winner'], success=True)

    # Get next move with minimax algorithm
    node = minimax_ttt(True, copy.deepcopy(board))[1]

    # row and column
    max_i = node[0]
    max_j = node[1]

    board[max_i][max_j] = 2

    state = checkWin_ttt(board)

    # machine wins
    if state['winner'] != -1:
        return jsonify(state=state['winner'], row=max_i, col=max_j, row1=state['index1'][0], col1=state['index1'][1],
                       row2=state['index2'][0], col2=state['index2'][1], success=True)

    # Nobody wins yet
    return jsonify(row=max_i,
                   col=max_j,
                   success=True), 200


@app.route('/connectfour')
def connectfour():
    global board
    board = []

    for i in range(6):

        board.append([])
        for _ in range(7):
            board[i].append(0)

    return render_template('connectfour.html')


# Connect Four win


def checkWin_c4(game_board):
    for i in range(len(game_board)):

        for j in range(len(game_board[0])):

            if (game_board[i][j] == 0):
                continue

            if (i <= len(game_board) - 4):
                match = 1
                for k in range(3):

                    if (game_board[i + k][j] == game_board[i + k + 1][j]):
                        match += 1
                if (match == 4):
                    return {'winner': game_board[i][j], 'index1': [i, j], 'index2': [i + 3, j]}

                if (j <= len(game_board[0]) - 4):
                    diag_match = 1
                    for k in range(3):

                        if (game_board[i + k][j + k] == game_board[i + k + 1][j + k + 1]):
                            diag_match += 1

                    if (diag_match == 4):
                        return {'winner': game_board[i][j], 'index1': [i, j], 'index2': [i + 3, j + 3]}

                if (j >= 3):

                    reverse_diag_match = 1
                    for k in range(3):

                        if (game_board[i + k][j - k] == game_board[i + k + 1][j - k - 1]):
                            reverse_diag_match += 1

                    if (reverse_diag_match == 4):
                        return {'winner': game_board[i][j], 'index1': [i, j], 'index2': [i + 3, j - 3]}

            if (j <= len(game_board[0]) - 4):
                match = 1
                for k in range(3):
                    if (game_board[i][j + k] == game_board[i][j + k + 1]):
                        match += 1

                if (match == 4):
                    return {'winner': game_board[i][j], 'index1': [i, j], 'index2': [i, j + 3]}

    tie = 0
    for i in range(len(game_board)):

        for j in range(len(game_board[0])):

            if (game_board[i][j] != 0):
                tie += 1

    if (tie == 7 * 6):
        return {'winner': 0}

    return {'winner': -1}


def getRow(col, game_board):
    gravity = 0

    while (game_board[gravity][col] == 0):

        gravity += 1

        if (gravity == len(game_board)):
            break

    return gravity - 1


def getPieces(player, game_board):
    pieces = 0

    for i in range(len(game_board)):

        for j in range(len(game_board[0])):

            if player == game_board[i][j]:
                pieces += 1

    return pieces


# Connect Four minimax


def minimax_c4(current_node, game_board, alpha, beta, d):
    state = checkWin_c4(game_board)['winner']

    # Player wins (Bad)
    if (state == 1):
        return -22 + getPieces(1, game_board)

    # Machine wins (Good)
    elif (state == 2):
        return 22 - getPieces(2, game_board)

    # Tie (Okay)
    elif (state == 0 or d == 9):
        return 0

    value = -23 if current_node == True else 23

    pos = [0, 0]

    middle_offset = 0

    offset_positive = True

    for _ in range(len(game_board[0])):

        col = int(len(game_board[0]) / 2) + \
              (middle_offset if offset_positive else -middle_offset)

        offset_positive = not offset_positive

        if not offset_positive:
            middle_offset += 1

        row = getRow(col, game_board)

        if (row == -1):
            continue

        game_board[row][col] = 1 if current_node == False else 2

        cost = minimax_c4(not current_node, game_board, alpha, beta, d + 1)

        game_board[row][col] = 0

        if (isinstance(cost, tuple)):
            cost = cost[0]
        if d == 0:
            print(cost, end='')
        if current_node == True and cost > value:
            value = cost
            pos = [row, col]
        elif current_node == False and cost < value:
            value = cost

        if value > alpha and current_node == True:
            alpha = value
        elif value < beta and current_node == False:
            beta = value

        if beta <= alpha:
            break

    return value, pos


@app.route('/connectfour/board/set/<int:column>')
def connectfourset(column):
    row = getRow(column, board)

    board[row][column] = 1

    print("Calculating...")

    node = minimax_c4(True, copy.deepcopy(board), -23, 23, 0)[1]
    print()
    max_i = node[0]
    max_j = node[1]

    board[max_i][max_j] = 2

    state = checkWin_c4(board)

    if (state['winner'] != -1):
        return jsonify(state=state['winner'], row=max_i, col=max_j, player_row=row, row1=state['index1'][0],
                       col1=state['index1'][1], row2=state['index2'][0], col2=state['index2'][1], success=True)

    return jsonify(row=max_i, col=max_j, player_row=row, success=True)


@app.route('/checkers')
def checkers():
    global board
    board = []

    for i in range(8):

        board.append([])

        for j in range(8):

            board[i].append(-1 if (j % 2 == 0 if i %
                                                 2 == 0 else j % 2 == 1) else 0)

            if (j % 2 == 1 if i % 2 == 0 else j % 2 == 0):
                if i < 3:
                    board[i][j] = 2
                elif i > 4:
                    board[i][j] = 1

    return render_template('checkers.html')


def eat(i1, j1, i2, j2, game_board, turn, playerToEat, isKing):
    if game_board[i2][j2] != 0:
        return -1

    if isKing and i1 < i2 or (turn == True and i1 < i2):
        if j1 > j2 and game_board[i1 + 1][j1 - 1] == playerToEat:
            return [i1 + 1, j1 - 1]
        elif j1 < j2 and game_board[i1 + 1][j1 + 1] == playerToEat:
            return [i1 + 1, j1 + 1]

    if i1 > i2 or (isKing and i1 < i2 and turn == True):
        if j1 > j2 and game_board[i1 - 1][j1 - 1] == playerToEat:
            return [i1 - 1, j1 - 1]
        elif j1 < j2 and game_board[i1 - 1][j1 + 1] == playerToEat:
            return [i1 - 1, j1 + 1]

    return -1


def isEatAvailable(game_board, current_node):
    for i in range(8):

        for j in range(8):

            if game_board[i][j] == 0 or game_board[i][j] == -1:
                continue

            if current_node == True and game_board[i][j] in [1, 11]:
                continue

            elif current_node == False and game_board[i][j] in [2, 22]:
                continue

            piece = game_board[i][j]

            eat_options = []

            if current_node == False:
                eat_options = [2, 22]
            else:
                eat_options = [1, 11]

            isKing = False

            if piece == 11 or piece == 22:
                isKing = True

            for k in [-2, 2]:
                if (i + 2 < len(game_board) and j + k >= 0 and j + k < len(game_board[0])):
                    if (game_board[i + 2][j + k] == 0):

                        for opponent in eat_options:

                            result = eat(i, j, i + 2, j + k, game_board,
                                         current_node, opponent, isKing)

                            if result != -1:
                                return True


def checkWin_checkers(game_board):
    player_pieces = 0
    bot_pieces = 0

    for i in range(len(game_board)):
        for j in range(len(game_board[0])):

            if game_board[i][j] in [1, 11]:
                player_pieces += 1
            elif game_board[i][j] in [2, 22]:
                bot_pieces += 1

    if player_pieces == 0 and bot_pieces > 0:
        return {'winner': 2}
    elif player_pieces > 0 and bot_pieces == 0:
        return {'winner': 1}
    else:
        return {'winner': 0}


def minimax_checkers(current_node, game_board, alpha, beta, d):
    state = checkWin_checkers(game_board)['winner']

    # Player wins (Bad)
    if (state == 1):
        return float('-inf')

    # Machine wins (Good)
    elif (state == 2):
        return float('inf')

    elif (d == 9):
        return getPieces(2, game_board) - getPieces(1, game_board)

    value = -13 if current_node == True else 13

    pos_old = []
    pos = []
    eat_pos = []

    isEatMoveAvailable = isEatAvailable(game_board, current_node)

    for i in range(len(game_board)):
        for j in range(len(game_board[0])):

            if game_board[i][j] == 0 or game_board[i][j] == -1:
                continue

            if current_node == True and game_board[i][j] in [1, 11]:
                continue
            elif current_node == False and game_board[i][j] in [2, 22]:
                continue

            piece = game_board[i][j]

            eat_options = []

            if current_node == False:
                eat_options = [2, 22]
            else:
                eat_options = [1, 11]

            isKing = False

            if i == len(game_board) - 1 and piece == 2:
                game_board[i][j] = 22
                piece = game_board[i][j]
            elif i == 0 and piece == 1:
                game_board[i][j] = 11
                piece = game_board[i][j]

            if piece == 22 or piece == 11:
                isKing = True

            for k in [-2, 2, -1, 1]:
                for o in [-2, 2]:

                    if not isKing and ((current_node == True and o == -2) or (current_node == False and o == 2)):
                        continue

                    if (k == 1 or k == -1) and isEatMoveAvailable:
                        continue

                    new_pos = []

                    ate = []

                    ate_piece = 0

                    another_turn = False

                    if k == 1 or k == -1:
                        if (i + 1 < len(game_board) and j + k >= 0 and j + k < len(game_board[0])):
                            if (game_board[i + 1][j + k] == 0):
                                game_board[i][j] = 0
                                new_pos = [i + 1, j + k]

                    else:

                        if i + o < len(game_board) and 0 <= j + k < len(game_board[0]):
                            if (game_board[i + o][j + k] == 0):

                                for opponent in eat_options:

                                    result = eat(
                                        i, j, i + o, j + k, game_board, current_node, opponent, isKing)

                                    if result != -1:
                                        game_board[i][j] = 0
                                        new_pos = [i + o, j + k]
                                        ate = result
                                        ate_piece = game_board[result[0]][result[1]]

                                        for r in [-2, 2]:
                                            if (i + 2 + o < len(game_board) and 0 <= j + k + r < len(
                                                    game_board[0])):
                                                if (game_board[i + 2 + o][j + k + r] == 0):

                                                    for opponent in eat_options:

                                                        result = eat(
                                                            i + o, j + k, i + 2 + o, j + k + r, game_board,
                                                            current_node, opponent, isKing)

                                                        if result != -1:
                                                            another_turn = True

                                        break

                    if new_pos == []:
                        continue

                    game_board[new_pos[0]][new_pos[1]] = piece

                    if ate_piece != 0:
                        game_board[ate[0]][ate[1]] = 0

                    cost = minimax_checkers(
                        not current_node if not another_turn else current_node, game_board, alpha, beta, d + 1)

                    game_board[new_pos[0]][new_pos[1]] = 0

                    if ate_piece != 0:
                        game_board[ate[0]][ate[1]] = ate_piece

                    game_board[i][j] = piece

                    if isinstance(cost, tuple):
                        cost = cost[0]

                    if d == 0:
                        print(cost, end=',')

                    if current_node == True and cost > value:
                        value = cost
                        pos = new_pos
                        pos_old = [i, j]
                        if ate_piece != 0:
                            eat_pos = ate
                        else:
                            eat_pos = []
                    elif current_node == False and cost < value:
                        value = cost

                    if value > alpha and current_node == True:
                        alpha = value
                    elif value < beta and current_node == False:
                        beta = value

                    if beta <= alpha:
                        return value, pos, pos_old, eat_pos

    return value, pos, pos_old, eat_pos


@app.route('/checkers/board/set/<int:row1>,<int:column1>,<int:row2>,<int:column2>')
def checkersset(row1, column1, row2, column2):
    if board[row2][column2] != 0 or (
            board[row1][column1] != 1 and board[row1][column1] != 11) or row1 - row2 > 2 or row1 == row2:
        return jsonify(success=False), 404

    # can't move backwards if not king
    if board[row1][column1] != 11 and row1 < row2:
        return jsonify(success=False), 404

    didEat = False

    isKing = False

    if board[row1][column1] == 11:
        isKing = True

    # if space is 2 check if opponent between them and eat if there is
    if row1 - row2 == 2 or row1 - row2 == -2:

        for opponent in [2, 22]:
            result = eat(row1, column1, row2, column2, board, False, opponent, isKing)

            if result == -1:
                return jsonify(success=False), 404

            board[result[0]][result[1]] = 0

            didEat = True
            break

    if row2 == 0 or isKing:
        board[row2][column2] = 11
        isKing = True
    else:
        board[row2][column2] = 1

    board[row1][column1] = 0

    another_turn = False

    if didEat:

        for k in [-2, 2]:
            for opponent in [2, 22]:

                if row2 - 2 >= 0 and column2 + k >= 0 and column2 + k < 8:
                    if eat(row2, column2, row2 - 2, column2 + k, board, False, opponent, isKing) != -1:
                        another_turn = True

                if row2 + 2 < 8 and column2 + k >= 0 and column2 + k < 8 and isKing:
                    if eat(row2, column2, row2 + 2, column2 + k, board, False, opponent, isKing) != -1:
                        another_turn = True

    if not another_turn:
        node = minimax_checkers(True, copy.deepcopy(board), -13, 13, 0)

        print(node)

        board[node[1][0]][node[1][1]] = 22 if node[1][0] == len(board) - 1 or board[node[2][0]][node[2][1]] == 22 else 2
        board[node[2][0]][node[2][1]] = 0

        if node[3] != []:
            board[node[3][0]][node[3][1]] = 0

    return jsonify(board=board, success=True)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404


if (__name__ == '__main__'):
    app.run(debug=True)
