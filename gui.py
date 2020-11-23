#encoding: utf-8
import tkinter.ttk as ttk
import tkMessageBox
from tkinter import *
import json
import time

from board import Board
from tools import *
from pappohi import *
from karasu import *

player_function = {
     "random": random_player,
     u"パッポヒ": pappohi,
     u"カラス": karasu,
 }

com_player_list = (
    "random",
    u"パッポヒ",
    u"カラス",

    "人間","human",
 )

with open("setting.json",mode="r") as f:
    setting_file = json.load(f)

SHOW_LEGAL = setting_file["SHOW_LEGAL"]
SHOW_SCORE = setting_file["SHOW_SCORE"]
FIRST_COLOR = setting_file["FIRST_COLOR"]
LAST_COLOR = setting_file["LAST_COLOR"]
BACKGROUND_COLOR = setting_file["BACKGROUND_COLOR"]
DRAW_OVAL = setting_file["DRAW_OVAL"]
DRAW_LEGAL_OVAL = setting_file["DRAW_LEGAL_OVAL"]
SQUARE_SIZE = setting_file["SQUARE_SIZE"]
GAP = setting_file["GAP"]
WINDOW_WIDTH = setting_file["WINDOW_WIDTH"]
WINDOW_HEIGHT = setting_file["WINDOW_HEIGHT"]
SLEEP = setting_file["SLEEP"]

def setting_player():
    global first_type,last_type,first_name,last_name

    first_type = isinstance(first,str) or isinstance(first,unicode)
    last_type = isinstance(last,str) or isinstance(last,unicode)
 
    first_name = first if first_type else first(None,"NAME")
    last_name = last if last_type else last(None,"NAME")

def show():
    global stone_id
    
    if board.turn % 2 ==0:
        turn_label.configure(text=u"先手番 {0}({1})".format(first_name,"HUM" if first_type else "COM"))
    else:
        turn_label.configure(text=u"後手番 {0}({1})".format(last_name,"HUM" if last_type else "COM"))
    
    board_flat = sum(board.board,[])
    stones_label.configure(text="{0} - {1}".format(board_flat.count(2),board_flat.count(1)))

    for si in stone_id:
        canvas.delete(si)

    figure_func = canvas.create_rectangle

    if DRAW_OVAL:
        figure_func = canvas.create_oval

    for y in range(8):
        for x in range(8):
            stone = board.board[y][x]

            if stone:
                clr = LAST_COLOR if stone == 1 else FIRST_COLOR
                stone_id.append(figure_func(x*SQUARE_SIZE+5,y*SQUARE_SIZE+5,x*SQUARE_SIZE+SQUARE_SIZE-5,y*SQUARE_SIZE+SQUARE_SIZE-5,fill=clr,width=0))
    
    with open("pappohi_score.json",mode="r") as f:
        board_scores = json.load(f)

    legal = board.legal_hands(board.turn%2)

    if not SHOW_LEGAL:
        legal = []
     
    clr = "blue" if board.turn%2==0 else "red"
    
    figure_func = canvas.create_rectangle
    if DRAW_LEGAL_OVAL:
        figure_func = canvas.create_oval

    for l in legal:
        x,y = l
        stone_id.append(figure_func(x*SQUARE_SIZE+GAP, y*SQUARE_SIZE+GAP, x*SQUARE_SIZE+SQUARE_SIZE-GAP, y*SQUARE_SIZE+SQUARE_SIZE-GAP,fill=clr,width=0))
        if SHOW_SCORE:
            stone_id.append(canvas.create_text(x*SQUARE_SIZE+SQUARE_SIZE/2,y*SQUARE_SIZE+10,text=str(board_scores[y][x])))

    board.show()
    tk.update()
        
def click(x,y):
    x //= SQUARE_SIZE
    y //= SQUARE_SIZE

    if x>=8 or y>=8:
        return

    turn = board.turn % 2

    if turn == 0:
        if not first_type:
            x,y = first(board)

        board.turn_stones(x,y,turn)
    elif turn == 1:
        if not last_type:
            x,y = last(board)

        board.turn_stones(x,y,turn)
    
    show()
    result = board.judge()
    
    if result != -1:
        end(result)
        return
    if not board.legal_hands(board.turn%2):
        board.turn += 1
        show()

        if board.turn % 2 == 0 and not first_type:
            click(-1,-1)
            return
        elif board.turn % 2 == 1 and not last_type:
            click(-1,-1)
            return
        
    if board.turn % 2 == 0 and not first_type:
        click(-1,-1)
    elif board.turn % 2 == 1 and not last_type:
        click(-1,-1)

def start():
    global first,last

    p1 = player1_combo.get()
    p2 = player2_combo.get()
    
    player1_combo.configure(state="disable")
    player2_combo.configure(state="disable")
    
    first = p1
    if p1 in player_function:
        first = player_function[p1]
    
    last = p2
    if p2 in player_function:
        last = player_function[p2]

    setting_player()
    
    tk.title(u"オセロ {0} vs {1}".format(first_name,last_name))
    board.__init__()
    show()

    
    if not first_type:
        click(-1,-1)

def end(result):
    winner = result[0]
    
    show()

    msg = u"引き分け!"

    if winner == 0:
        msg = u"先手({0})の勝利!".format(first_name)
    elif winner == 1:
        msg = u"後手({0})の勝利!".format(last_name)
    elif winner == -1:
        tkMessageBox.showinfo("オセロ","対局中断")
        player1_combo.configure(state="normal")
        player2_combo.configure(state="normal")

        board.__init__()
        show()
        return

    tkMessageBox.showinfo("オセロ",unicode(result[1][0])+u" - "+unicode(result[1][1])+u"で"+msg)
    
    player1_combo.configure(state="normal")
    player2_combo.configure(state="normal")
    
    board.__init__()
    show()

first = ""
last = ""

setting_player()
   

board = Board()

stone_id = []

tk = Tk()
tk.geometry("{0}x{1}".format(WINDOW_WIDTH,WINDOW_HEIGHT))
tk.title("オセロ")
tk.resizable(0,0)

turn_label = Label(tk,text="",font = ("",30))
turn_label.place(x=SQUARE_SIZE*8,y=0)

stones_label = Label(tk,text="",font=("",30))
stones_label.place(x=SQUARE_SIZE*8+100,y=50)

canvas = Canvas(tk,width=SQUARE_SIZE*8,height=SQUARE_SIZE*8,bg=BACKGROUND_COLOR)
canvas.place(x=0,y=0)

for y in range(9):
    canvas.create_line(0,y*SQUARE_SIZE,SQUARE_SIZE*8,y*SQUARE_SIZE,width=5)

for x in range(9):
    canvas.create_line(x*SQUARE_SIZE,0,x*SQUARE_SIZE,SQUARE_SIZE*8,width=5)


player1_combo = ttk.Combobox(tk, state="normal", width=20)
player1_combo["values"] = com_player_list
player1_combo.place(x=50, y=SQUARE_SIZE*8+10)

player2_combo = ttk.Combobox(tk, state="normal", width=20)
player2_combo["values"] = com_player_list
player2_combo.place(x=50, y=SQUARE_SIZE*8+30)

player1_combo.set("人間")
player2_combo.set(u"パッポヒ")

start_btn = Button(tk,text="対局開始",bg="blue",highlightbackground="blue",font=("",20),command=start)
start_btn.place(x=300,y=SQUARE_SIZE*8+10)

end_btn = Button(tk,text="対局中断",bg="cyan",highlightbackground="cyan",font=("",20),command=lambda:end([-1]))
end_btn.place(x=300,y=SQUARE_SIZE*8+40)

exit_btn = Button(tk,text="終了",bg="red",highlightbackground="red",font=("",30),command=exit)
exit_btn.place(x=500,y=SQUARE_SIZE*8+10)

canvas.bind("<ButtonPress>",lambda e:click(e.x,e.y))

show()

tk.mainloop()
