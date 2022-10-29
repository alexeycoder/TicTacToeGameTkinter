from enum import Enum, auto


class GameState(Enum):
    INITIALIZED = auto()
    USER_TURN = auto()
    AI_TURN = auto()
    GAMEOVER_USER_WINS = auto()
    GAMEOVER_AI_WINS = auto()
    GAMEOVER_NOONE_WINS = auto()


# def next_turn(whose_turn: GameState):
#     assert whose_turn is not None and whose_turn in (GameState.AI_TURN, GameState.USER_TURN), \
#         "Некорректное значение аргумента в " + next_turn.__name__

#     if whose_turn == GameState.AI_TURN:
#         return GameState.USER_TURN
#     return GameState.AI_TURN
