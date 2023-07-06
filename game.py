from tkinter import *
from tkinter import messagebox as msgbox
from random import randint as rnd
import datetime as dt

vertical = 20
side = 10
size = 10
mino_size = 4
form = 0
mode = 0
y = -1
x = 4
speed = 500

colours = ["cyan",
           "blue",
           "orange",
           "yellow",
           "green",
           "purple",
           "red",
           "dimgrey"]

y_data = [0,0,0,0]
x_data = [0,0,0,0]
foundation_data = [7,7,7,7]
foundation = [[7 for i in range(side + 2)] for j in range(vertical+2)]
for i in range(vertical+2):
    foundation[i][0],foundation[i][side+1] = 8, 8
foundation[vertical+1]=[8 for i in range(side+2)]

def draw_foundation():
    for v in range(vertical):
        v1 = v * size
        v2 = v1 + size
        for s in range(side):
            s1 = s * size
            s2 = s1 + size
            for c in range(len(colours)):
                if foundation[v+1][s+1] == c:
                    colour = colours[c]
                    cv.create_rectangle(s1,v1,s2,v2,fill=colour)

mino_data = [[[[2,0],[2,1],[2,2],[2,3]],
              [[0,1],[1,1],[2,1],[3,1]],
              [[1,0],[1,1],[1,2],[1,3]],
              [[0,2],[1,2],[2,2],[3,2]]],
             [[[1,0],[2,0],[2,1],[2,2]],
              [[1,1],[1,2],[2,1],[3,1]],
              [[2,0],[2,1],[2,2],[3,2]],
              [[1,1],[2,1],[3,0],[3,1]]], 
             [[[1,2],[2,0],[2,1],[2,2]],
              [[1,1],[2,1],[3,1],[3,2]],
              [[2,0],[2,1],[2,2],[3,0]],
              [[1,0],[1,1],[2,1],[3,1]]], 
             [[[1,1],[1,2],[2,1],[2,2]],
              [[1,1],[1,2],[2,1],[2,2]],
              [[1,1],[1,2],[2,1],[2,2]],
              [[1,1],[1,2],[2,1],[2,2]]],  
             [[[1,1],[1,2],[2,0],[2,1]],
              [[1,1],[2,1],[2,2],[3,2]],
              [[2,1],[2,2],[3,0],[3,1]],
              [[1,0],[2,0],[2,1],[3,1]]],
             [[[1,1],[2,0],[2,1],[2,2]],
              [[1,1],[2,1],[2,2],[3,1]],
              [[2,0],[2,1],[2,2],[3,1]],
              [[1,1],[2,0],[2,1],[3,1]]],
             [[[1,0],[1,1],[2,1],[2,2]],
              [[1,2],[2,1],[2,2],[3,1]],
              [[2,0],[2,1],[3,1],[3,2]],
              [[1,1],[2,0],[2,1],[3,0]]]]
mino = [[7 for i in range(mino_size)] for j in range(mino_size)]

def create_mino():
    global form, mino
    form = rnd(0,6)
    for i in range(len(mino_data[form][mode % 4])):
        y = mino_data[form][mode % 4][i][0]
        x = mino_data[form][mode % 4][i][1]
        mino[y][x] = form

def draw_mino():
    for v in range(mino_size):
        v1 = (v + y - 1)* size
        v2 = v1 + size
        for s in range(mino_size):
            s1 = (s + x - 1) * size
            s2 = s1 + size
            if mino[v][s] == form:
                cv.create_rectangle(s1, v1, s2, v2, fill = colours[form])
class Move_mino:
    def __init__(self,next_y,next_x,next_mode):
        self.next_y = next_y
        self.next_x = next_x
        self.next_mode = next_mode

    def reference(self):
        global x_data,y_data, foundation_data
        for i in range(len(mino_data[form][mode % 4])):
            y_data[i] = mino_data[form][(mode + self.next_mode) % 4][i][0] + y
            x_data[i] = mino_data[form][(mode + self.next_mode) % 4][i][1] + x
            foundation_data[i] = foundation[y_data[i] + self.next_y][x_data[i] + self.next_x]

    def move_mino(self,e):
        self.reference()
        global x,y
        global foundation, mino, mode
        if foundation_data == [7,7,7,7]:
            y += 1* self.next_y
            x += 1* self.next_x

        if self.next_y == 1 and foundation_data != [7,7,7,7]:
            for i in range(len(y_data)):
                foundation[y_data[i]][x_data[i]] = form
            delete()
            game_over()
            mode = 0
            y = -1
            x = 4
            mino = [[7 for i in range(mino_size)] for j in range(mino_size)]
            create_mino()
        cv.delete("all")
        draw_foundation()
        draw_mino()

    def drop_mino(self):
        global speed
        self.move_mino(Event)
        if speed > 200:
            speed -= 1
            win.after(speed, self.drop_mino)

    def spin_mino(self, e):
        self.reference()
        global mode, mino
        if foundation_data == [7,7,7,7]:
            mode += 1 * self.next_mode
            mino = [[7 for i in range(mino_size)] for j in range(mino_size)]
            for i in range(len(mino_data[form][mode % 4])):
                y = mino_data[form][mode % 4][i][0]
                x = mino_data[form][mode % 4][i][1]
                mino[y][x] = form
                cv.delete("all")
                draw_foundation()
                draw_mino()

def delete():
    for v in range(len(foundation)):
        if (7 in foundation[v]) == False and foundation[v] != [8 for i in range(side + 2)]:
            del foundation[v]
            add_foundation = [7 for i in range(side + 2)]
            add_foundation[0], add_foundation[side + 1] = 8,8
            foundation.insert(0, add_foundation)

def game_over():
    top_foundation = [7 for i in range(side + 2)]
    top_foundation[0],top_foundation[side+1] = 8,8
    if foundation[1] != top_foundation:
        sp = dt.datetime.now()
        msgbox.showinfo(message = "GAME OVER\nYou lasted " + str((sp-st).seconds)+ " seconds")
        quit()

def main():
    global win, cv
    win = Tk()
    cv = Canvas(win, width=side * size, height=vertical * size)
    left = Move_mino(0,-1,0)
    right = Move_mino(0,1,0)
    under = Move_mino(1,0,0)
    left_spin = Move_mino(0,0,-1)
    right_spin = Move_mino(0,0,1)
    win.bind("<Left>",left.move_mino)
    win.bind("<Right>",right.move_mino)
    win.bind("<Return>",under.move_mino)
    win.bind("<Up>",right_spin.spin_mino)
    win.bind("<Down>",left_spin.spin_mino)
    under.drop_mino()
    create_mino()
    cv.pack()
    win.mainloop()

if __name__ == "__main__":
    st = dt.datetime.now()
    main()