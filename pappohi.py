#encoding: utf-8
import sys
import random
import math
import json
import time

from tools import *
from board import Board

def pappohi_engine(board):
    with open("pappohi_score.json",mode="r") as f:
        board_score = json.load(f)

    legal = board.legal_hands(board.turn%2)

    choiced = [min(sum(board_score,[])),[]]
    
    for l in legal:
        x,y = l
        score = board_score[y][x]
        if choiced[0] < score:
            choiced = [score,[(x,y)]]
        elif choiced[0] == score:
            choiced[1].append((x,y))
    
    if not legal:
        return -1,-1
    return random.choice(choiced[1])

def pappohi(board,opt=""):
    if opt == "NAME":
        return u"パッポヒ"

    return pappohi_engine(board)


def pappohi_learn(N=1000,player=random_player):

    with open("pappohi_score.json",mode="r") as f:
        board_score = json.load(f)

    board = Board()
    start = time.time()
    loop_start = time.time()
    for i in range(N):
        percent = float(i+1) / float(N) * 100

        now = time.time()

        pass_time = round(now-start,2)
        time_left = round((now-loop_start) * N - pass_time,2)
        sys.stdout.write("\r" + "#"*int(percent/2) + "  " + str(percent)+"%  " + str(i+1) + "/" + str(N) + "   " + str(pass_time) + "s | " + str(time_left) + "s")
        sys.stdout.flush()
        loop_start = time.time()

        board.__init__()
        first_pos = []
        last_pos  = []
        winner = 2
        for j in range(64):
            turn = board.turn % 2

            x,y = player(board)
            board.turn_stones(x,y,turn)
            
            if x == -1:
                board.turn += 1 
                continue
            
            if turn == 0:
                first_pos.append((x,y))
            else:
                last_pos.append((x,y))

            result = board.judge()
            if result != -1:
                winner = result[0]
                break

        first_point = 0.5
        last_point = 0.5

        if winner == 0:
            first_point = 1
            last_point = -1
        elif winner == 1:
            first_point = -1
            last_point = 1

        for pos in first_pos:
            x,y = pos
            board_score[y][x] += first_point
        for pos in last_pos:
            x,y = pos
            board_score[y][x] += last_point
    
    print 
    with open("pappohi_score.json",mode="w") as f:
        json.dump(board_score,f)

def print_score():
    with open("pappohi_score.json",mode="r") as f:
        board_score = json.load(f)
    
    n = 1

    for s in sum(board_score,[]):
        if n < len(str(s)):
            n = len(str(s))

    for y in range(8):
        for x in range(8):
            print str(board_score[y][x]).rjust(n),
        print

def reset():
    with open("pappohi_score.json",mode="w") as f:
        json.dump([[0 for j in range(8)] for i in range(8)],f)

if __name__ == "__main__":
    reset()
    pappohi_learn(1000,pappohi_engine)
    print_score()
