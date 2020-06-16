# # Tic-Tac-Toe Game Logics

import random
def start_game(turn=-1):
    mat = [[0 for j in range(3)] for i in range(3)]
    if turn == 1:
        row = random.randint(0,2)
        col = random.randint(0,2)
        mat[row][col] = 1
    return mat

def game_state(ele):
    # checking rows
    for i in range(3):
        if ele[i][0] == ele[i][1] and ele[i][1] == ele[i][2]:
            if ele[i][0] == 1:
                return 1
            elif ele[i][0] == -1:
                return -1
    # checking columns
    for j in range(3):
        if ele[0][j] == ele[1][j] and ele[1][j] == ele[2][j]:
            if ele[0][j] == 1:
                return 1
            elif ele[0][j] == -1:
                return -1
    # checking leading diagonal
    if ele[0][0] == ele[1][1] and ele[1][1] == ele[2][2]:
        if ele[1][1] == 1:
            return 1
        elif ele[1][1] == -1:
            return -1
    # checking other diagonal
    if ele[0][2] == ele[1][1] and ele[1][1] == ele[2][0]:
        if ele[1][1] == 1:
            return 1
        elif ele[1][1] == -1:
            return -1
    # check if all filled
    for i in range(3):
        for j in range(3):
            if ele[i][j] == 0:
                return
    return 0

def get_win_pos(ele, state):
    if state == 0 or state is None:
        return
    for i in range(3):
        if ele[i][0] == ele[i][1] and ele[i][1] == ele[i][2]:
            if ele[i][0] == state:
                return ['r', i]
    for j in range(3):
        if ele[0][j] == ele[1][j] and ele[1][j] == ele[2][j]:
            if ele[0][j] == state:
                return ['c', j]
    if ele[0][0] == ele[1][1] and ele[1][1] == ele[2][2]:
        if ele[1][1] == state:
            return ['ld']
    if ele[0][2] == ele[1][1] and ele[1][1] == ele[2][0]:
        if ele[1][1] == state:
            return ['od']

def fill(mat, pos):
    x = pos[0]
    y = pos[1]
    if mat[x][y] == 0:
        mat[x][y] = -1

def best_move(mat):
    best_score = [-float('inf')]
    move = None
    for i in range(3):
        for j in range(3):
            if mat[i][j] == 0:
                mat[i][j] = 1
                score = minimax(mat)
                mat[i][j] = 0
                if score[0] > best_score[0]:
                    move = (i,j)
                    best_score = score
    if move is not None:
        mat[move[0]][move[1]] = 1

def minimax(mat, depth = 1):
    state = game_state(mat)
    if state is not None:
        return (state, depth)
    isMaximizing = False
    if depth%2 == 0:
        isMaximizing = True
    ans = []
    if isMaximizing:
        for i in range(3):
            for j in range(3):
                if mat[i][j] == 0:
                    mat[i][j] = 1
                    ans.append(minimax(mat, depth+1))
                    mat[i][j] = 0
        return (max(ans, key = lambda ele:ele[0]))
    else:
        for i in range(3):
            for j in range(3):
                if mat[i][j] == 0:
                    mat[i][j] = -1
                    ans.append(minimax(mat, depth+1))
                    mat[i][j] = 0
        return (min(ans, key = lambda ele:ele[0]))
