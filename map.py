class GridMap:
    def __init__(self):
        self.grid = [
            ["S", ".", ".", ".", "."],
            [".", "#", "#", ".", "."],
            [".", ".", ".", ".", "."],
            [".", "#", ".", "#", "."],
            [".", ".", ".", ".", "F"]
        ]

        self.player = (0, 0)
        self.goal = (4, 4)

    def display(self):
        for row in self.grid:
            print(" ".join(row))