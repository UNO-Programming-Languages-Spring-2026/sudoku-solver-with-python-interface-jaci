"""
sudoku1.py - Questions 1a and 1b
Usage: python sudoku1.py instances/lp/ex00.lp [clingo options]
"""

import sys
from clingo.application import Application, clingo_main

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
    """Question 1a & 1b: Sudoku solver with sorted output."""

    program_name = "sudoku"
    version = "1.0"

    def print_model(self, model, printer):
        """Question 1b: Print atoms in alphabetically sorted order."""
        atoms = sorted(str(atom) for atom in model.symbols(shown=True))
        print(" ".join(atoms))

    def main(self, ctl, files):
        ctl.add("base", [], SUDOKU_ENCODING)
        for f in files:
            ctl.load(f)
        ctl.ground([("base", [])])
        ctl.solve()


if __name__ == "__main__":
    clingo_main(SudokuApp(), sys.argv[1:])