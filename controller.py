import random
from consts import CELLS_COUNT
from entities.cell_state import CellState
from entities.game_state import GameState
from gui.main_window import CellButtonState, MainWindow
from model.game_desk import GameDesk


def cell_state_to_button_state(cell_state: CellState) -> CellButtonState:
    btn_txt = str(cell_state)
    is_enabled = cell_state == CellState.EMPTY
    return CellButtonState(text=btn_txt, is_enabled=is_enabled)


def game_state_to_text(game_state: GameState):
    match game_state:
        case GameState.INITIALIZED:
            return 'Игра ещё не начата.'
        case GameState.USER_TURN:
            return 'Ход игрока'
        case GameState.AI_TURN:
            return 'Ход ИИ'
        case GameState.GAMEOVER_NOONE_WINS:
            return 'Игра окончена: Ничья!'
        case GameState.GAMEOVER_USER_WINS:
            return 'Игра окончена: Вы победили!'
        case GameState.GAMEOVER_AI_WINS:
            return 'Игра окончена: Вы проиграли!'


def desk_to_view(desk: list[CellState]):
    return list(map(cell_state_to_button_state, desk))


class ModelViewBinder:

    def __init__(self) -> None:

        self.game_desk = GameDesk()
        self.game_desk.desk_changed_handler = self.desk_changed_handler

        self.window = MainWindow()
        self.window.update([(CellButtonState())] * CELLS_COUNT,
                           'В ожидании запуска...',
                           None)
        self.window.cell_btn_pressed_handler = self.cell_btn_pressed_handler
        self.window.surrender_btn_pressed_handler = self.surrender_btn_pressed_handler
        self.window.new_game_btn_pressed_handler = self.new_game_btn_pressed_handler

    def run_app(self):
        self.window.run()

    def desk_changed_handler(self, desk: list[CellState], game_state: GameState, win_cells: tuple[int]):
        cells_states = desk_to_view(desk)
        game_status_msg = game_state_to_text(game_state)
        self.window.update(cells_states, game_status_msg, win_cells)

    def new_game_btn_pressed_handler(self):
        # self.game_desk.initialize(random.choice((CellState.X, CellState.O)))
        self.game_desk.initialize(CellState.X)
        self.game_desk.start()

    def surrender_btn_pressed_handler(self):
        pass

    def cell_btn_pressed_handler(self, button_index: int):
        self.game_desk.user_turn(button_index)
