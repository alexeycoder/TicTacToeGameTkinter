from enum import Enum, auto
from consts import X_SIGN, O_SIGN, EMPTY_SIGN


class CellState(Enum):
    EMPTY = EMPTY_SIGN
    O = O_SIGN
    X = X_SIGN

    def __str__(self) -> str:
        return str(self.value)


def get_opposite(cell_state: CellState):
    assert cell_state is not None and cell_state != CellState.EMPTY, "Некорректное значение аргумента в " + get_opposite.__name__

    if cell_state == CellState.X:
        return CellState.O
    return CellState.X
