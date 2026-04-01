from typing import Tuple
import clingo


class Sudoku:
    def __init__(self, sudoku: dict[Tuple[int, int], int]):
        self.sudoku = sudoku

    def __str__(self) -> str:
        s = ""
        for row in range(1, 10):
            # Add blank line between block rows (before rows 4 and 7)
            if row in (4, 7):
                s += "\n"
            row_str = ""
            for col in range(1, 10):
                # Double space between block columns (before cols 4 and 7)
                if col in (4, 7):
                    row_str += "  "
                elif col > 1:
                    row_str += " "
                val = self.sudoku.get((row, col), "-")
                row_str += str(val)
            s += row_str + "\n"
        return s.rstrip("\n")

    @classmethod
    def from_str(cls, s: str) -> "Sudoku":
        sudoku = {}
        # Filter out blank lines, strip whitespace from each line
        lines = [line.strip() for line in s.strip().splitlines() if line.strip()]
        row = 0
        for line in lines:
            row += 1
            tokens = line.split()
            col = 0
            for token in tokens:
                col += 1
                if token != "-":
                    sudoku[(row, col)] = int(token)
        return cls(sudoku)

    @classmethod
    def from_model(cls, model: clingo.solving.Model) -> "Sudoku":
        sudoku = {}
        for symbol in model.symbols(shown=True):
            if symbol.name == "sudoku" and len(symbol.arguments) == 3:
                row = symbol.arguments[0].number
                col = symbol.arguments[1].number
                val = symbol.arguments[2].number
                sudoku[(row, col)] = val
        return cls(sudoku)
