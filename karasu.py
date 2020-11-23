#encoding: utf-8
import random
from copy import deepcopy

from tools import random_player

def karasu_point(board,turn):
    board_flat = sum(board.board,[])

    black = board_flat.count(2)
    white = board_flat.count(1)

    if turn == 0:
        return black - white
    else:
        return white - black

def karasu_engine(board,N=10):
    legal = board.legal_hands(board.turn%2)
    
    original_board = deepcopy(board)
    
    wins = {}
    turn = board.turn % 2

    scores = {}
    for l in legal:
        wins[l] = 0
        for n in range(N):
            board = deepcopy(original_board)
            board.turn_stones(l[0],l[1],board.turn%2)

            for i in range(64):
                x,y = random_player(board)
                board.turn_stones(x,y,board.turn%2)

                result = board.judge()

                if result != -1:
                    break
            winner = -1
            if result != -1:
                winner = result[0]

            if winner == turn:
                wins[l] += 1
    
    choiced = [0,[]]

    for l in wins:
        win = wins[l]

        if choiced[0] < win:
            choiced = [win,[l]]
        elif choiced[0] == win:
            choiced[1].append(l)

    board = deepcopy(original_board)
    

    if not choiced[1]:
        if legal:
            return random.choice(legal)
        return -1,-1
    return random.choice(choiced[1])

def karasu(board,opt=""):
    if opt == "NAME":
        return u"カラス"

    return karasu_engine(board)
