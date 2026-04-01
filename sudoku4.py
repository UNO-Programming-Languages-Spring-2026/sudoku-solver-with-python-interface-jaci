import sys
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


class SudokuApp(Application):
    program_name = "sudoku"
    version = "1.0"

    def print_model(self, model, printer):
        sudoku = Sudoku.from_model(model)
        print(str(sudoku))

    def main(self, ctl, files):
        ctl.add("base", [], SUDOKU_ENCODING)
        for f in files:
            ctl.load(f)
        ctl.ground([("base", [])])
        ctl.solve()


if __name__ == "__main__":
    # Strip the leading '0' argument the assignment passes before the file
    args = [a for a in sys.argv[1:] if a != "0"]
    clingo_main(SudokuApp(), args)