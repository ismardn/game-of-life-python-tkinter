import tkinter.ttk


class Game:

    def __init__(self):
        self.window = tkinter.Tk()
        self.window.title("Conway's Game of Life")

        self.WIDTH = 900
        self.HEIGHT = 950

        self.MIN_CELLS_NUMBER = 20
        self.MAX_CELLS_NUMBER = 70

        self.TASKBAR_HEIGHT_PERCENTAGE = 8

        self.window.geometry(f"{self.WIDTH}"
                             f"x{self.HEIGHT}"
                             f"+{self.window.winfo_screenwidth() // 2 - self.WIDTH // 2}"
                             f"+{self.window.winfo_screenheight() // 2 - self.HEIGHT // 2 - round((self.TASKBAR_HEIGHT_PERCENTAGE / 100) * self.window.winfo_screenheight() / 2)}")

        self.window.resizable(False, False)

        self.window.configure(bg="white")

        self.display_menu()

        self.window.mainloop()


    def delete_widgets(self):
        for widget in self.window.winfo_children():
            widget.destroy()


    def display_menu(self):
        self.delete_widgets()

        self.play = False

        self.cells_number = self.MIN_CELLS_NUMBER

        self.scale_value = tkinter.IntVar()

        self.frame = tkinter.Frame(self.window, bg="white", height=self.HEIGHT // 3, width=self.WIDTH)
        self.frame.pack_propagate(False)
        self.frame.pack(expand=tkinter.YES)

        tkinter.Label(self.frame, text="Choose the number of cells per row/column :", font=("Rockwell", 25), bg="white").pack(expand=tkinter.YES)

        self.frame_scale = tkinter.Frame(self.frame, bg="white")
        self.frame_scale.pack(expand=tkinter.YES)

        self.style_scale = tkinter.ttk.Style()
        self.style_scale.theme_use('clam')
        self.style_scale.configure("TScale", background="white")
        self.scale = tkinter.ttk.Scale(self.frame_scale, from_=self.MIN_CELLS_NUMBER, to=self.MAX_CELLS_NUMBER, length=self.WIDTH // 3, style="TScale", variable=self.scale_value, command=self.set_current_scale)
        self.scale.pack(side=tkinter.LEFT)

        self.subframe_scale = tkinter.Frame(self.frame_scale, bg="white")
        self.subframe_scale.pack(expand=tkinter.YES)

        tkinter.Label(self.subframe_scale, text=" " * (self.WIDTH // 200), font=("Rockwell", 25), bg="white").pack(side=tkinter.LEFT)

        self.scale_label = tkinter.Label(self.subframe_scale, text=f"{self.cells_number} cells", font=("Rockwell", 25), bg="white")
        self.scale_label.pack(side=tkinter.RIGHT)

        self.style_create_button = tkinter.ttk.Style()
        self.style_create_button.configure("TButton", font=("Rockwell", 25), focuscolor='none')

        self.create_button = tkinter.ttk.Button(self.frame, text="Create the grid", style="TButton", command=self.set_game)
        self.create_button.pack(expand=tkinter.YES)


    def set_current_scale(self, _):
        self.cells_number = self.scale_value.get()
        self.scale_label.config(text=f"{self.cells_number} cells")


    def set_rectangles(self):
        for row in range(self.cells_number):
            for column in range(self.cells_number):
                self.cell_rects[row][column] = self.grid.create_rectangle(round(column * self.cell_size),
                                                                          round(row * self.cell_size),
                                                                          round((column + 1) * self.cell_size),
                                                                          round((row + 1) * self.cell_size),
                                                                         
                                                                          fill="white", outline='gray')


    def set_game(self):
        self.delete_widgets()

        self.generation = 0

        self.grid_list = [[False for _cell in range(self.cells_number)] for _cells_list in range(self.cells_number)]
        self.cell_rects = [[None for _cell in range(self.cells_number)] for _cells_list in range(self.cells_number)]

        self.size_grid = self.WIDTH - self.WIDTH // 8

        self.cell_size = self.size_grid / self.cells_number

        self.frame = tkinter.Frame(self.window, width=self.size_grid, height=self.size_grid + self.WIDTH // 16, bg="white")
        self.frame.pack_propagate(False)
        self.frame.pack(expand=tkinter.YES)

        self.top_frame = tkinter.Frame(self.frame, width=self.size_grid, height=self.WIDTH // 16, bg="white")
        self.top_frame.pack_propagate(False)
        self.top_frame.pack(side=tkinter.TOP)

        self.style_start_button = tkinter.ttk.Style()
        self.style_start_button.theme_use("alt")
        self.style_start_button.configure("Top.TButton", font=("Rockwell", 12), focuscolor="none")

        self.bouton_retour = tkinter.ttk.Button(self.top_frame, text="Redefine number of cells", style="Top.TButton", command=self.display_menu)
        self.bouton_retour.pack(side=tkinter.LEFT)

        self.bouton_retour = tkinter.ttk.Button(self.top_frame, text="Clear grid", style="Top.TButton", command=self.clear_grid)
        self.bouton_retour.pack(side=tkinter.RIGHT)

        self.grid = tkinter.Canvas(self.frame, bg="white", width=self.size_grid, height=self.size_grid,  highlightthickness=1, highlightbackground="gray")
        self.grid.pack(side=tkinter.BOTTOM)

        for column in range(1, self.cells_number):
            self.grid.create_line(round(self.cell_size * column), 0, round(self.cell_size * column), self.size_grid + 2, fill="gray", width=1)

        for row in range(1, self.cells_number):
            self.grid.create_line(0, round(self.cell_size * row), self.size_grid + 2, round(self.cell_size * row), fill="gray", width=1)

        self.grid.create_line(0, self.size_grid, self.size_grid + 1, self.size_grid, fill="gray", width=1)
        self.grid.create_line(self.size_grid, 0, self.size_grid, self.size_grid + 1, fill="gray", width=1)

        self.grid.bind("<Button-1>", self.grid_click)

        self.set_rectangles()

        self.bottom_frame = tkinter.Frame(self.window, width=self.size_grid, height=self.HEIGHT - self.size_grid - self.WIDTH // 8, bg="white")
        self.bottom_frame.pack_propagate(False)
        self.bottom_frame.pack(expand=tkinter.YES)

        self.left_frame = tkinter.Frame(self.bottom_frame, width=self.size_grid // 4, height=self.HEIGHT - self.size_grid - self.WIDTH // 8, bg="white")
        self.left_frame.pack_propagate(False)
        self.left_frame.pack(side=tkinter.LEFT)

        self.style_start_button = tkinter.ttk.Style()
        self.style_start_button.theme_use("alt")
        self.style_start_button.configure("Play.TButton", font=("Rockwell", 17), focuscolor="none")
        self.start_button = tkinter.ttk.Button(self.left_frame, text="Start", style="Play.TButton", command=self.start_game)
        self.start_button.pack(side=tkinter.LEFT)

        self.subframe = tkinter.Frame(self.bottom_frame, width=self.size_grid - self.size_grid // 4, height=self.HEIGHT - self.size_grid - self.WIDTH // 8, bg="white")
        self.subframe.pack_propagate(False)
        self.subframe.pack(side=tkinter.RIGHT)

        self.middle_frame = tkinter.Frame(self.subframe, width=self.size_grid // 2, height=self.HEIGHT - self.size_grid - self.WIDTH // 8, bg="white")
        self.middle_frame.pack_propagate(False)
        self.middle_frame.pack(side=tkinter.LEFT)

        self.speed_frame_entry = tkinter.Frame(self.middle_frame, width=self.size_grid // 3, height=(self.HEIGHT - self.size_grid - self.WIDTH // 8) // 2, bg="white")
        self.speed_frame_entry.pack_propagate(False)
        self.speed_frame_entry.pack(side=tkinter.TOP)

        tkinter.Label(self.speed_frame_entry, text="Set speed (ms) : ", bg="white", font=("Rockwell", 15)).pack(side=tkinter.LEFT)

        self.speed_input = tkinter.IntVar()
        self.speed_input.set(1000)
        self.speed_input.trace_add('write', lambda *_args: self.set_current_speed())

        self.speed = int(self.speed_input.get())

        self.speed_entry = tkinter.Entry(self.speed_frame_entry, font=("Rockwell", 15), textvariable=self.speed_input, bg="white", width=self.size_grid // 3)
        self.speed_entry.pack(side=tkinter.RIGHT)

        self.speed_label = tkinter.Label(self.middle_frame, text=f"Current set speed : 1000 ms", font=("Rockwell", 10), bg="white")
        self.speed_label.pack(side=tkinter.BOTTOM)

        self.right_frame = tkinter.Frame(self.subframe, width=self.size_grid // 3, height=self.HEIGHT - self.size_grid - self.WIDTH // 8, bg="white")
        self.right_frame.pack_propagate(False)
        self.right_frame.pack(side=tkinter.RIGHT)

        self.generation_label = tkinter.Label(self.right_frame, text=f"Generation : 0", font=("Rockwell", 17), bg="white")
        self.generation_label.pack(side=tkinter.RIGHT)


    def set_current_speed(self):
        try:
            speed = self.speed_input.get()
            if 50 <= speed <= 5000:
                self.speed = speed
                self.speed_label.config(text=f"Current (max) speed : {speed} ms")
        except:
            pass


    def clear_grid(self):
        for row in range(self.cells_number):
            for column in range(self.cells_number):
                if self.grid_list[row][column]:
                    self.grid_list[row][column] = False
                    self.kill_cell(row, column)

        self.generation = 0
        self.generation_label.config(text=f"Generation : {self.generation}")

        self.stop_game()
        

    def grid_click(self, event):
        self.x_postion = event.x
        self.y_postion = event.y

        if not self.play:
            for row in range(self.cells_number):
                for column in range(self.cells_number):
                    if round(column * self.cell_size) < self.x_postion < round((column + 1) * self.cell_size) and round(row * self.cell_size) < self.y_postion < round((row + 1) * self.cell_size):
                        if self.grid_list[row][column]:
                            self.grid_list[row][column] = False
                            self.kill_cell(row, column)
                        else:
                            self.grid_list[row][column] = True
                            self.create_cell(row, column)


    def create_cell(self, row, column):
        self.grid.itemconfig(self.cell_rects[row][column], fill="black")


    def kill_cell(self, row, column):
        self.grid.itemconfig(self.cell_rects[row][column], fill="white")


    def start_game(self):
        self.play = True
        self.play_game()

        self.start_button.config(text="Stop", command=self.stop_game)


    def play_game(self):
        if self.play:

            new_grid_list = [[False for _cell in range(self.cells_number)] for _cells_list in range(self.cells_number)]

            for row in range(self.cells_number):
                for column in range(self.cells_number):
                    
                    neighbouring_cells = []


                    if row > 0:
                        if column > 0:
                            neighbouring_cells.append(self.grid_list[row - 1][column - 1])  # oXX

                        neighbouring_cells.append(self.grid_list[row - 1][column])          # XoX

                        if column < self.cells_number - 1:
                            neighbouring_cells.append(self.grid_list[row - 1][column + 1])  # XXo


                    if column > 0:
                        neighbouring_cells.append(self.grid_list[row][column - 1])          # o-X

                    if column < self.cells_number - 1:
                        neighbouring_cells.append(self.grid_list[row][column + 1])          # X-o


                    if row < self.cells_number - 1:
                        if column > 0:
                            neighbouring_cells.append(self.grid_list[row + 1][column - 1])  # oXX

                        neighbouring_cells.append(self.grid_list[row + 1][column])          # XoX

                        if column < self.cells_number - 1:
                            neighbouring_cells.append(self.grid_list[row + 1][column + 1])  # XXo

        
                    alive_cells_number = 0
                    for cell in neighbouring_cells:
                        if cell:
                            alive_cells_number += 1

                    if not self.grid_list[row][column] and alive_cells_number == 3:
                        new_grid_list[row][column] = True
                        
                    elif self.grid_list[row][column] and alive_cells_number not in (2, 3):
                        new_grid_list[row][column] = False

                    else:
                        new_grid_list[row][column] = self.grid_list[row][column]

                    if new_grid_list[row][column] != self.grid_list[row][column]:
                        if new_grid_list[row][column]:
                            self.create_cell(row, column)
                        else:
                            self.kill_cell(row, column)


            self.grid_list = new_grid_list

            self.generation += 1
            self.generation_label.config(text=f"Generation : {self.generation}")

            self.window.after(self.speed, self.play_game)


    def stop_game(self):
        self.play = False
        self.start_button.config(text="Start", command=self.start_game)


Game()
