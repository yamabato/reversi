#encoding: utf-8

import re

"""
0 -
1 O 後手 白 n:1
2 X 先手 黒 n:0
"""

class Board:
    def __init__(self):
        self.board = [[0 for j in range(8)] for i in range(8)]

        self.board[3][3] = 1
        self.board[4][4] = 1
        self.board[4][3] = 2
        self.board[3][4] = 2

        self.turn = 0

    def legal_hands(self,turn):
        stone = "1" if turn else "2"
        opponent_stone = "2" if turn else "1"
        
        line_list = []
        legal = []

        for y in range(8):
            for x in range(8):
                if self.board[y][x] == 0:
                    line_list.append([(x,y)]+self.lines(x,y))
        
        pattern = re.compile(str(opponent_stone)+"+"+str(stone))
        for l in line_list:
            for line in l[1:]:
                if not line: continue
                line_str = "".join(map(str,line))

                if line_str[0] == opponent_stone and re.match(pattern,line_str):
                    legal.append(l[0])

        return legal
    
    def turn_stones(self,x,y,turn):
        line = self.lines(x,y)
        stone = "1" if turn else "2"
        opponent_stone = "2" if turn else "1"
        pattern = re.compile(str(opponent_stone)+"+"+str(stone))
        
        if self.board[y][x] != 0:
            return False
        if (x,y) not in self.legal_hands(turn):
            return False

        t = False
        for n,l in enumerate(line):
            line_str = "".join(map(str,l))
            
            match = re.match(pattern,line_str)
            if line_str and line_str[0] == opponent_stone and match:
                t = True
                end = match.end()
                
                if n == 0:
                    for i in range(y,y-end,-1):
                        self.board[i][x] = int(stone)
                elif n == 1:
                    if x == 0:
                        break
                    for i in range(x,x-end,-1):
                        self.board[y][i] = int(stone)
                elif n == 2:
                    for i in range(x,x+end):
                        self.board[y][i] = int(stone)
                elif n == 3:
                    for i in range(y,y+end):
                        self.board[i][x] = int(stone)
                elif n == 4:
                    for i,j in zip(range(x,x-end,-1),range(y,y-end,-1)):
                        self.board[j][i] = int(stone)
                elif n == 5:
                    for i,j in zip(range(x,x+end),range(y,y-end,-1)):
                        self.board[j][i] = int(stone)
                elif n == 6:
                    for i,j in zip(range(x,x-end,-1),range(y,y+end)):
                        self.board[j][i] = int(stone)
                elif n == 7:
                    for i,j in zip(range(x,x+end),range(y,y+end)):
                        self.board[j][i] = int(stone)
        if t:
            self.turn += 1
        return t


    def lines(self,x,y):
        line = []
        
        if y>0:
            line.append([self.board[i][x] for i in range(y-1,-1,-1)])
        else:
            line.append([])

        if x > 0:
            line.append(self.board[y][x-1::-1])
        else:
            line.append([])

        if x < 7:
            line.append(self.board[y][x+1:8])
        else:
            line.append([])

        if y < 7:
            line.append([self.board[i][x] for i in range(y+1,8)])
        else:
            line.append([])

        if x > 0 and y > 0:
            line.append([self.board[j][i] for i,j in zip(range(x-1,-1,-1), range(y-1,-1,-1))])
        else:
            line.append([])

        if x < 7 and y > 0:
            line.append([self.board[j][i] for i,j in zip(range(x+1,8), range(y-1,-1,-1))])
        else:
            line.append([])

        if x > 0 and y < 7:
            line.append( [self.board[j][i] for i,j in zip(range(x-1,-1,-1), range(y+1,8))])
        else:
            line.append([])

        if x < 7 and y < 7:
            line.append( [self.board[j][i] for i,j in zip(range(x+1,8), range(y+1,8))])
        else:
            line.append([])

        return line

    def show(self):
        stone_mark  = {
            0:"-",
            1:"O",
            2:"X",
            
            0:"ー",
            1:"⚪️",
            2:"⚫️",
        }
        for i in range(8):
            print "".join(map(lambda x:stone_mark[x], self.board[i]))
        print

    def judge(self):
        winner = -1
        if not all(map(all,self.board)):
            board_flat = sum(self.board,[])
            if board_flat.count(1) == 0:
                winner = 0
            elif board_flat.count(2) == 0:
                winner = 1
            else:
                if (not self.legal_hands(0)) and (not self.legal_hands(1)):
                    winner = -1
                else:
                    return -1

        black = 0
        white = 0

        for y in range(8):
            black += self.board[y].count(2)
            white += self.board[y].count(1)
        
        if winner == -1:
            winner = 2
            if black > white:
                winner = 0
            elif black < white:
                winner = 1
        return (winner,(black,white))


