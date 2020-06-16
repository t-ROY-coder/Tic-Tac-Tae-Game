from tkinter import Frame, Label, CENTER, RAISED, SUNKEN, FLAT

import Logics
import constants as c

class TicTacToe(Frame):
    def __init__(self):
        Frame.__init__(self)
        # visualizing Frame in grid form
        self.grid()
        self.master.title('XOXO')
        # binding the control, i.e., if any key is pressed go to key_pressed function
        self.master.bind("<Button-1>", self.button_pressed)
        self.master.bind("<Return>", self.key_pressed)
        self.master.bind("<Motion>", self.hover_in)
        self.master.bind("<Leave>", self.hover_out)
        self.grid_cells = []
        self.score_man = 0
        self.score_mach = 0
        self.score_draw = 0
        self.init_grid()
        self.init_matrix()
        # update UI (set cell bg color and cell text color)
        self.update_grid_cells()
        # gameplay loop
        self.mainloop()

    def init_grid(self):
        # making the background
        background = Frame(self, bg = c.BG_COLOR_GAME, width = c.SIZE, height = c.SIZE)
        # visualizing background in grid form
        background.grid()
        self.bg = background
        for i in range(c.GRID_LEN):
            grid_row = []
            for j in range(c.GRID_LEN):
                # making cells inside background
                cell = Frame(background, bg = c.BG_COLOR_EMP_CELL, bd = 5,
                relief = RAISED, width = c.SIZE/c.GRID_LEN, height = c.SIZE/c.GRID_LEN)

                # placing cells in the correct position with padding
                cell.grid(row = i, column = j, padx = c.GRID_PAD, pady = c.GRID_PAD)

                # making the textbox(Label) inside cell which will contain the numbers
                t = Label(master = cell, text = "", bg = c.BG_COLOR_EMP_CELL,
                justify = CENTER, font = c.FONT, width = 5, height = 2)

                t.grid()
                grid_row.append(t)

            self.grid_cells.append(grid_row)

            #for i in range(3):
                #panel = Frame(self.bg, bg = c.BG_COLOR_EMP_CELL, height = 50, width = 250)
                #panel.grid(row = 4, column = i)
                #txt = Label(master = panel, text = "XO", fg = c.CELL_TXT_COLOR,
                #justify = CENTER, font = c.FONT)
    
    def init_matrix(self):
        self.turn = -1
        self.matrix = Logics.start_game(-1)
    
    def update_grid_cells(self):
        # UI update
        for i in range(c.GRID_LEN):
            for j in range(c.GRID_LEN):
                new_num = self.matrix[i][j]
                if new_num == 0:
                    self.grid_cells[i][j].configure(text = "", bg = c.BG_COLOR_EMP_CELL,
                    relief = FLAT)
                elif new_num == 1:
                    self.grid_cells[i][j].configure(text = "X",
                    bg = c.BG_COLOR_EMP_CELL, fg = c.CELL_TXT_COLOR, relief = SUNKEN)
                else:
                    self.grid_cells[i][j].configure(text = "O",
                    bg = c.BG_COLOR_EMP_CELL, fg = c.CELL_TXT_COLOR, relief = SUNKEN)
        # waits until all UI changes are done
        self.update_idletasks()

    def hover_in(self, event):
        if event.widget['bg'] != c.BG_COLOR_GAME:
            event.widget.configure(bg = c.BG_COLOR_HOVER_CELL)
    
    def hover_out(self, event):
        if event.widget['bg'] != c.BG_COLOR_GAME:
            event.widget.configure(bg = c.BG_COLOR_EMP_CELL)

    def button_pressed(self, event):
        state = Logics.game_state(self.matrix)
        if state is not None:
            return
        x = event.x_root - self.bg.winfo_rootx() 
        y = event.y_root - self.bg.winfo_rooty()
        z = self.bg.grid_location(x, y)
        if z[0] not in {0,1,2} or z[1] not in {0,1,2}:
            return
        pos = (z[1], z[0])
        if self.matrix[pos[0]][pos[1]] != 0:
            return
        Logics.fill(self.matrix, pos)
        self.update_grid_cells()
        state = Logics.game_state(self.matrix)
        if state is not None:
            if state == 1:
                self.score_mach += 1
            elif state == -1:
                self.score_man += 1
            else:
                self.score_draw += 1
            self.turn = -self.turn
            return
        Logics.best_move(self.matrix)
        self.update_grid_cells()
        state = Logics.game_state(self.matrix)
        if state is not None:
            if state == 1:
                self.score_mach += 1
            elif state == -1:
                self.score_man += 1
            else:
                self.score_draw += 1
            self.turn = -self.turn

    def key_pressed(self, event):
        self.matrix = Logics.start_game(self.turn)
        print('Game OVER')
        print('MAN:', self.score_man, 'MACHINE:', self.score_mach, 'DRAW:', self.score_draw)
        self.update_grid_cells()

#print('Enter your name:')
#s = input()
#print(s)

game = TicTacToe()
