import sys
import clingo
from clingo.application import Application, clingo_main


class SudokuApp(Application):
    program_name = "sudoku"
    version = "1.0"

    def main(self, control, files):
        control.load("sudoku.lp")

        for file in files:
            control.load(file)

        control.ground([("base", [])])
        control.solve()


app = SudokuApp()

if __name__ == "__main__":
    clingo_main(app, sys.argv[1:])