from collections import namedtuple
from tkinter import font
from consts import CELLS_COUNT, DIM, EMPTY_SIGN
import tkinter as tk
from tkinter import ttk
from gui import helpers

CellButtonState = namedtuple(
    'CellButtonState', ('text', 'is_enabled'), defaults=(EMPTY_SIGN, True))


def set_entry_text(entry: tk.Entry, text):
    entry.delete(0, tk.END)
    entry.insert(0, text)


class MainWindow:
    TITLE = 'Крестики-нолики'

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title(MainWindow.TITLE)

        self.cell_btn_pressed_handler = None
        self.new_game_btn_pressed_handler = None
        self.surrender_btn_pressed_handler = None

        self._compose()

    def _compose(self):
        root = self.root

        base_font = font.nametofont('TkDefaultFont')
        base_font_family = base_font.actual('family')
        base_font_size = int(base_font.actual('size'))
        xo_size = round(base_font_size*1.75)
        xo_font = font.Font(family=base_font_family,
                            size=xo_size, weight='bold')

        # create controls:

        self.lbl_placeholder = tk.Label(root, text='место для меню')
        self.lbl_recent_status = tk.Label(root, text='последний ход')

        original_fg_color = self.lbl_recent_status.cget('fg')

        self.btns_game_desk: tuple[tk.Button] = \
            tuple(tk.Button(root, text=str(i+1), font=xo_font, disabledforeground=original_fg_color,
                            command=lambda cell_idx=i: self.__on_cell_btn_pressed(cell_idx))
                  for i in range(CELLS_COUNT))

        self.btn_start = tk.Button(
            root, text='Начать игру', command=self.__on_new_game_btn_pressed)
        self.btn_surrender = tk.Button(
            root, text='Сдаться', command=self.__on_surrender_btn_pressed)

        # layout controls:

        self.lbl_placeholder.grid(row=0, column=0, columnspan=3, sticky='nw')
        self.lbl_recent_status.grid(row=1, column=0, columnspan=3, sticky='we')
        # rows 2 3 4
        btns_start_row = 2
        for row in range(btns_start_row, btns_start_row+DIM):
            for col in range(DIM):
                i = (row - btns_start_row) * DIM + col
                btn_cell: tk.Button = self.btns_game_desk[i]
                btn_cell.grid(row=row,
                              column=col,
                              sticky='nswe',
                              padx=2, pady=2)
                root.columnconfigure(index=col, weight=1, minsize=xo_size*4)
            root.rowconfigure(index=row, weight=1, minsize=xo_size*4)

        self.btn_start.grid(row=5, column=0, columnspan=3, sticky='we')
        self.btn_surrender.grid(row=6, column=0, columnspan=3, sticky='we')

        helpers.center_to_screen(root)

    def __on_cell_btn_pressed(self, button_index: int):
        if self.cell_btn_pressed_handler:
            self.cell_btn_pressed_handler(button_index)

    def __on_new_game_btn_pressed(self):
        if self.new_game_btn_pressed_handler:
            self.new_game_btn_pressed_handler()

    def __on_surrender_btn_pressed(self):
        if self.surrender_btn_pressed_handler:
            self.surrender_btn_pressed_handler()

    def run(self):
        self.root.mainloop()

    def update(self, cell_btn_states: list[CellButtonState], game_status_msg: str, win_cells: tuple[int]):
        self.lbl_recent_status['text'] = game_status_msg

        assert (count := len(self.btns_game_desk)) == len(cell_btn_states), \
            "Количество кнопок и соответствующих им представлений должно совпадать."

        # for i in range(count):
        #     btn_cell: tk.Button = self.btns_game_desk[i]
        #     cell_btn_state = cell_btn_states[i]
        #     btn_cell['text'] = cell_btn_state.text
        #     btn_cell['state'] = tk.NORMAL if cell_btn_state.is_enabled else tk.DISABLED

        for btn, btn_state in zip(self.btns_game_desk, cell_btn_states):
            btn['text'] = btn_state.text
            btn['state'] = tk.NORMAL if btn_state.is_enabled else tk.DISABLED

        self.root.update()
