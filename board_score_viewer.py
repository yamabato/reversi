#encoding: utf-8

from tkinter import *
import json

def show(file_name):
    global canvas_id

    with open(file_name,mode="r") as f:
        board_scores = json.load(f)
    
    for ci in canvas_id:
        canvas.delete(ci)
    
    board_flat = sum(board_scores,[])
    max_score = max(board_flat)
    min_score = min(board_flat)
    score_range = max_score - min_score

    for y in range(8):
        for x in range(8):
            clr = "#4d7f1b"

            score = board_scores[y][x]
            
            if score < 0:
                clr = "red"
            elif score > 0:
                clr = "blue"
            
            clr = "#" + hex(255 * int(score - min_score) // int(score_range))[2:].zfill(2) * 3


            canvas_id.append(
                canvas.create_rectangle(x*100+5,y*100+5,x*100+95,y*100+95,fill=clr)
            )
            
            canvas_id.append(
                canvas.create_text(x*100+50,y*100+50,text=str(score))
            )




tk = Tk()
tk.geometry("800x800")

canvas = Canvas(tk,width=800,height=800,bg="#4d7f1b")
canvas.pack()

canvas_id = []

for y in range(1,9):
    canvas.create_line(0, y*100, 800, y*100, width=5)
for x in range(1,9):
    canvas.create_line(x*100, 0, x*100, 800, width=5)

show("pappohi_score.json")

tk.mainloop()


