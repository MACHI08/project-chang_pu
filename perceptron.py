DIRECTIONS = {
    "w": (-1, 0),
    "s": (1, 0),
    "a": (0, -1),
    "d": (0, 1),
}

DIRECTION_NAMES = {
    "w": "up",
    "s": "down",
    "a": "left",
    "d": "right",
}


class PerceptronAgent:
    def __init__(self):
        # 모든 인접 타일에 같은 선형 모델을 적용한다.
        # 입력 순서: tile_preference, normalized_goal_distance
        self.weights = [1.0, -1.0]
        self.bias = 0.0

    def _normalized_goal_distance(self, position, goal, grid):
        rows = len(grid)
        cols = len(grid[0])
        max_distance = max(rows + cols - 2, 1)

        distance = (
            abs(goal[0] - position[0])
            + abs(goal[1] - position[1])
        )
        return distance / max_distance

    def choose_move(self, player, goal, grid, preferences, visited):
        row, col = player
        rows = len(grid)
        cols = len(grid[0])

        inputs = {}
        scores = {}
        positions = {}
        excluded_reasons = {}

        for move, (dr, dc) in DIRECTIONS.items():
            next_position = (row + dr, col + dc)
            next_row, next_col = next_position
            positions[move] = next_position

            if not (0 <= next_row < rows and 0 <= next_col < cols):
                inputs[move] = None
                scores[move] = float("-inf")
                excluded_reasons[move] = "맵 밖"
                continue

            if grid[next_row][next_col] == "#":
                inputs[move] = None
                scores[move] = float("-inf")
                excluded_reasons[move] = "장애물"
                continue

            if next_position in visited:
                inputs[move] = None
                scores[move] = float("-inf")
                excluded_reasons[move] = "방문한 칸"
                continue

            tile_inputs = [
                preferences[next_row][next_col],
                self._normalized_goal_distance(next_position, goal, grid),
            ]
            score = sum(
                input_value * weight
                for input_value, weight in zip(tile_inputs, self.weights)
            )
            score += self.bias

            inputs[move] = tile_inputs
            scores[move] = score
            excluded_reasons[move] = None

        candidates = [
            move for move in DIRECTIONS
            if scores[move] != float("-inf")
        ]
        selected_move = (
            max(candidates, key=lambda move: scores[move])
            if candidates
            else None
        )

        return {
            "move": selected_move,
            "scores": scores,
            "inputs": inputs,
            "positions": positions,
            "excluded_reasons": excluded_reasons,
        }
