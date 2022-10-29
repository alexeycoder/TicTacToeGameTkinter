import tkinter as tk


def center_to_parent(window: tk.Toplevel, parent_window: tk.BaseWidget):
    MIN_SHIFT = 30
    # window.update_idletasks()
    pw_width, pw_height = parent_window.winfo_width(), parent_window.winfo_height()
    x, y = parent_window.winfo_rootx(), parent_window.winfo_rooty()
    dx, dy = MIN_SHIFT, MIN_SHIFT
    # window.geometry(f'+{x+dx}+{y+dy}')
    # window.update()
    w_width, w_height = window.winfo_reqwidth(), window.winfo_reqheight()
    dx, dy = max(MIN_SHIFT, (pw_width-w_width)//2), \
        max(MIN_SHIFT, (pw_height-w_height)//2)
    window.geometry(f'+{x+dx}+{y+dy}')


def center_to_screen(window: tk.Toplevel):
    MIN_SHIFT = 1
    window.update_idletasks()
    s_width, s_height = window.winfo_screenwidth(), window.winfo_screenheight()
    w_width, w_height = window.winfo_width(), window.winfo_height()
    dx, dy = max(MIN_SHIFT, (s_width-w_width)//2), \
        max(MIN_SHIFT, (s_height-w_height)//2)
    window.geometry(f'+{dx}+{dy}')
