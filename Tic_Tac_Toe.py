from tkinter import Frame, Label, CENTER, RAISED, SUNKEN, FLAT

import Logics
import constants as c

class TicTacToe(Frame):
    def __init__(self, username):
        Frame.__init__(self)
        # visualizing Frame in grid form
        self.grid()
        self.score_man = 0
        self.score_mach = 0
        self.score_draw = 0
        self.master.title('{:10}Scores [ {} : {} ; Royik (bot) : {} ; Draw : {} ]'.format('XOXO', username,
        self.score_man, self.score_mach, self.score_draw))
        # binding the control, i.e., if any key is pressed go to key_pressed function
        self.master.bind("<Button-1>", self.button_pressed)
        self.master.bind("<Return>", self.key_pressed)
        self.master.bind("<Motion>", self.hover_in)
        self.master.bind("<Leave>", self.hover_out)
        self.grid_cells = []
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
                justify = CENTER, font = c.FONT, width = 4, height = 2)

                t.grid()
                grid_row.append(t)

            self.grid_cells.append(grid_row)
    
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
        
        state = Logics.game_state(self.matrix)
        if state in {1,-1}:
            win_pos = Logics.get_win_pos(self.matrix, state)
            if win_pos[0] == 'r':
                for j in range(3):
                    self.grid_cells[win_pos[1]][j].configure(fg = c.CELL_TXT_WIN_COLOR)
            elif win_pos[0] == 'c':
                for i in range(3):
                    self.grid_cells[i][win_pos[1]].configure(fg = c.CELL_TXT_WIN_COLOR)
            elif win_pos[0] == 'ld':
                for i in range(3):
                    self.grid_cells[i][i].configure(fg = c.CELL_TXT_WIN_COLOR)
            elif win_pos[0] == 'od':
                for i in range(3):
                    self.grid_cells[2-i][i].configure(fg = c.CELL_TXT_WIN_COLOR)

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
            self.master.title('{:10}Scores [ {} : {} ; Royik (bot) : {} ; Draw : {} ]{:>40}'.format('XOXO', username,
            self.score_man, self.score_mach, self.score_draw, "Game OVER! (Press Enter for new game)"))
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
            self.master.title('{:10}Scores [ {} : {} ; Royik (bot) : {} ; Draw : {} ]{:>40}'.format('XOXO', username,
            self.score_man, self.score_mach, self.score_draw, "Game OVER! (Press Enter for new game)"))

    def key_pressed(self, event):
        self.master.title('{:10}Scores [ {} : {} ; Royik (bot) : {} ; Draw : {} ]'.format('XOXO', username,
        self.score_man, self.score_mach, self.score_draw))
        self.matrix = Logics.start_game(self.turn)
        self.update_grid_cells()

print("Hello, I'm Royik, the bot. Let's play Tic-Tac-Toe.")
print("What's your name?")
username = input()
print("OK", username,", let's see if you can beat me.")
print("(Instructions: Click on one of the boxes to do your move; Press Enter for new game)")

game = TicTacToe(username)
