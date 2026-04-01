"""
sudoku6.py - Questions 6a and 6b
Reads .txt input in the friendly format, outputs solution in the same format.
Usage: python sudoku6.py instances/txt/ex00.txt
"""

import sys
import clingo
from clingo.application import Application, clingo_main
from sudoku_board import Sudoku

SUDOKU_ENCODING = """
{ sudoku(R,C,V) : V = 1..9 } = 1 :- R = 1..9, C = 1..9.
sudoku(R,C,V) :- initial(R,C,V).
:- sudoku(R,C1,V), sudoku(R,C2,V), C1 != C2.
:- sudoku(R1,C,V), sudoku(R2,C,V), R1 != R2.
:- sudoku(R1,C1,V), sudoku(R2,C2,V),
   (R1-1)/3 == (R2-1)/3, (C1-1)/3 == (C2-1)/3,
   (R1,C1) != (R2,C2).
#show sudoku/3.
"""


class Context:

    def __init__(self, board: Sudoku):
        self._board = board

    def initial(self) -> list:
        result = []
        for (row, col), val in self._board.sudoku.items():
            symbol = clingo.Function(
                "",
                [
                    clingo.Number(row),
                    clingo.Number(col),
                    clingo.Number(val),
                ],
            )
            result.append(symbol)
        return result


class SudokuApp(Application):

    program_name = "sudoku"
    version = "1.0"

    def __init__(self):
        self._context = None

    def print_model(self, model, printer):
        sudoku = Sudoku.from_model(model)
        print(str(sudoku))

    def main(self, ctl, files):
        # Read the .txt puzzle file
        puzzle_text = ""
        for fname in files:
            with open(fname, "r") as fh:
                puzzle_text = fh.read()
            break

        board = Sudoku.from_str(puzzle_text)
        self._context = Context(board)

        # Add encoding and inject initial facts directly
        ctl.add("base", [], SUDOKU_ENCODING)
        for (row, col), val in board.sudoku.items():
            ctl.add("base", [], f"initial({row},{col},{val}).")

        ctl.ground([("base", [])], context=self._context)
        ctl.solve()


if __name__ == "__main__":
    clingo_main(SudokuApp(), sys.argv[1:])