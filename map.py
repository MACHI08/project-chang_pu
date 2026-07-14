import random

from pathfinding import is_reachable


class GridMap:
    def __init__(
        self,
        size=10,
        obstacle_count=15,
        preference_min=0.48,
        preference_max=0.52,
    ):
        if size <= 0:
            raise ValueError("size는 0보다 커야 합니다.")
        if obstacle_count < 0:
            raise ValueError("obstacle_count는 0 이상이어야 합니다.")
        if not 0.0 <= preference_min <= preference_max <= 1.0:
            raise ValueError(
                "선호도 범위는 0.0 <= preference_min <= "
                "preference_max <= 1.0이어야 합니다."
            )

        self.size = size
        self.preference_min = preference_min
        self.preference_max = preference_max

        for _ in range(1000):
            self.grid = [["." for _ in range(size)] for _ in range(size)]
            self.preferences = [
                [
                    random.uniform(preference_min, preference_max)
                    for _ in range(size)
                ]
                for _ in range(size)
            ]

            self.player = (
                random.randint(0, size - 1),
                random.randint(0, size - 1),
            )

            self.goal = self.player
            while self.goal == self.player:
                self.goal = (
                    random.randint(0, size - 1),
                    random.randint(0, size - 1),
                )

            obstacle_positions = self._create_spaced_obstacles(obstacle_count)
            if obstacle_positions is None:
                continue

            for row, col in obstacle_positions:
                self.grid[row][col] = "#"

            player_row, player_col = self.player
            goal_row, goal_col = self.goal
            self.grid[player_row][player_col] = "S"
            self.grid[goal_row][goal_col] = "F"

            if is_reachable(self.grid, self.player, self.goal):
                return

        raise RuntimeError(
            "조건을 만족하는 맵을 생성하지 못했습니다. "
            "맵 크기 또는 장애물 수를 조정하세요."
        )

    def _create_spaced_obstacles(self, obstacle_count):
        candidates = [
            (row, col)
            for row in range(self.size)
            for col in range(self.size)
            if (row, col) not in {self.player, self.goal}
        ]
        random.shuffle(candidates)

        obstacles = []
        for position in candidates:
            if all(
                max(
                    abs(position[0] - other[0]),
                    abs(position[1] - other[1]),
                )
                > 1
                for other in obstacles
            ):
                obstacles.append(position)

                if len(obstacles) == obstacle_count:
                    return obstacles

        return None

    def display(self):
        for row in self.grid:
            print(" ".join(row))
