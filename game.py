#encoding: utf-8

from board import Board

b = Board()
turn = 0
b.show()
while True:
    while True:
        x,y = map(int,raw_input("xy:"))
        if b.turn_stones(x,y,turn):break

    print "０１２３４５６７"
    b.show()

    result = b.judge()

    if result != -1:
        if result[0] == 2:
            print "引き分け",
        elif result[0] == 0:
            print "先手の勝利",
        else:
            print "後手の勝利",

        print result[1][0], "-", result[1][1] 
        break
    turn = abs(turn-1)
