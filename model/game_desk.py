import random
from consts import CELLS_COUNT
from entities.cell_state import CellState, get_opposite
from entities.game_state import GameState


class GameDesk:
    __SCANLINES = ((0, 1, 2), (3, 4, 5), (6, 7, 8),
                   (0, 3, 6), (1, 4, 7), (2, 5, 8),
                   (0, 4, 8), (2, 4, 6))

    def __init__(self):
        self.game_state = None
        self.desk_changed_handler = None

    def initialize(self, user_mark: CellState):
        self.user_mark = user_mark
        self.ai_mark = get_opposite(user_mark)
        self.desk = [CellState.EMPTY] * CELLS_COUNT
        self.user_turns = []
        self.ai_turns = []

        self.win_cells: tuple[int] = None
        self.game_state = GameState.INITIALIZED

    def start(self):
        assert self.game_state == GameState.INITIALIZED, "Need to initialize before start!"

        if self.ai_mark == CellState.X:
            self.game_state = GameState.AI_TURN
            self.__do_ai_turn()
        else:
            self.game_state = GameState.USER_TURN
            self.__on_desk_changed()

    def __on_desk_changed(self):
        if self.desk_changed_handler:
            self.desk_changed_handler(
                self.desk, self.game_state, self.win_cells)

    def user_turn(self, cell_index):
        assert self.game_state == GameState.USER_TURN, "Сейчас ход ИИ, а не игрока!"
        assert self.desk[cell_index] == CellState.EMPTY, "Ячейка уже занята!"

        self.__do_user_turn(cell_index)

    def __do_user_turn(self, cell_index):
        self.desk[cell_index] = self.user_mark
        self.user_turns.append(cell_index)

        self.game_state = GameState.AI_TURN
        self.__check_for_winner()

        self.__on_desk_changed()
        if self.game_state == GameState.AI_TURN:
            self.__do_ai_turn()

    def __do_ai_turn(self):
        empty_cells_indexes = [i for i, v in
                               enumerate(self.desk) if v == CellState.EMPTY]
        chosen_index = random.choice(empty_cells_indexes)

        self.desk[chosen_index] = self.ai_mark
        self.ai_turns.append(chosen_index)

        self.game_state = GameState.USER_TURN
        self.__check_for_winner()

        self.__on_desk_changed()

    def __check_for_winner(self):
        winner_tuple = GameDesk.__try_find_winner(self.desk)

        if winner_tuple is None:
            return

        (who_wins, win_cells) = winner_tuple
        if who_wins == CellState.EMPTY:
            self.game_state = GameState.GAMEOVER_NOONE_WINS
            return

        self.win_cells = win_cells
        if who_wins == self.ai_mark:
            self.game_state = GameState.GAMEOVER_AI_WINS
        else:
            self.game_state = GameState.GAMEOVER_USER_WINS

    @staticmethod
    def __try_find_winner(desk) -> tuple[CellState, tuple[int]]:
        """Вернёт кортеж вида ( CellState.ЗнакПобедителя, (индексы пересечения) ), если есть победитель
        либо кортеж вида (CellState.EMPTY, None) если -- ничья,
        в противном случае вернёт None
        """
        noone_can_win = True
        for scanline in GameDesk.__SCANLINES:
            states = {desk[i] for i in scanline}
            if len(states - {CellState.EMPTY}) != 2:
                noone_can_win = False
            if len(states) == 1 and states != {CellState.EMPTY}:
                winner = list(states)[0]
                return (winner, scanline)

        if noone_can_win or desk.count(CellState.EMPTY) == 0:
            return (CellState.EMPTY, None)
