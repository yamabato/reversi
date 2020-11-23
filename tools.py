#encoding: utf-8

import random
import time

def random_player(board,opt=""):
    if opt == "NAME":
        return u"ランダム"

    legal = board.legal_hands(board.turn%2)
    if not legal:
        return -1,-1
    return random.choice(legal)
