import random
from pathfinding import is_reachable


class GridMap:

    def __init__(self, size=10, obstacle_count=15): # 2번째 칼럼의 size를 수정하면 맵 사이즈도 같이 변경됨

        self.size = size

        while True:

            # 빈 맵 생성
            self.grid = [["." for _ in range(size)] for _ in range(size)]

            # 시작 위치 생성
            self.player = (
                random.randint(0, size - 1),
                random.randint(0, size - 1)
            )

            # 목표 위치 생성 (시작 위치와 겹치지 않게)
            while True:

                self.goal = (
                    random.randint(0, size - 1),
                    random.randint(0, size - 1)
                )

                if self.goal != self.player:
                    break

            # 장애물 생성
            count = 0

            while count < obstacle_count:

                r = random.randint(0, size - 1)
                c = random.randint(0, size - 1)

                if (r, c) != self.player and (r, c) != self.goal:

                    if self.grid[r][c] == ".":
                        self.grid[r][c] = "#"
                        count += 1

            # 시작 위치와 목표 위치 표시
            pr, pc = self.player
            gr, gc = self.goal

            self.grid[pr][pc] = "S"
            self.grid[gr][gc] = "F"

            # 도달 가능한 맵이면 종료
            if is_reachable(self.grid, self.player, self.goal):
                break

    def display(self):

        for row in self.grid:
            print(" ".join(row))