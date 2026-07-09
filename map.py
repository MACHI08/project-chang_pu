class GridMap:
    def __init__(self):
        self.grid = [
            ["S", ".", ".", ".", "."],
            [".", "#", "#", ".", "."],
            [".", ".", ".", ".", "."],
            [".", "#", ".", "#", "."],
            [".", ".", ".", ".", "F"]
        ]

    def display(self):
        for row in self.grid:
            print(" ".join(row))