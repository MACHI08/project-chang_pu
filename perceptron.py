class PerceptronAgent:
    def __init__(self, visit_penalty=2):
        # 입력 순서:
        # goal_up, goal_down, goal_left, goal_right,
        # obstacle_up, obstacle_down, obstacle_left, obstacle_right
        self.weights = [5, 5, 5, 5, -8, -8, -8, -8]
        self.bias = 0
        self.visit_penalty = visit_penalty
        self.last_scores = {}

    def get_inputs(self, player, goal, grid):
        rows = len(grid)
        cols = len(grid[0])
        r, c = player

        goal_up = int(goal[0] < r)
        goal_down = int(goal[0] > r)
        goal_left = int(goal[1] < c)
        goal_right = int(goal[1] > c)

        obstacle_up = int(r == 0 or grid[r - 1][c] == "#")
        obstacle_down = int(r == rows - 1 or grid[r + 1][c] == "#")
        obstacle_left = int(c == 0 or grid[r][c - 1] == "#")
        obstacle_right = int(c == cols - 1 or grid[r][c + 1] == "#")

        return [
            goal_up,
            goal_down,
            goal_left,
            goal_right,
            obstacle_up,
            obstacle_down,
            obstacle_left,
            obstacle_right,
        ]

    def activation(self, x):
        return 1 if x > 0 else 0

    def choose_move(
        self,
        player,
        goal,
        grid,
        visited_count,
        previous_position=None,
    ):
        directions = {
            "w": (-1, 0),
            "s": (1, 0),
            "a": (0, -1),
            "d": (0, 1),
        }

        rows = len(grid)
        cols = len(grid[0])
        movable = []

        for move, (dr, dc) in directions.items():
            nr = player[0] + dr
            nc = player[1] + dc

            if not (0 <= nr < rows and 0 <= nc < cols):
                continue
            if grid[nr][nc] == "#":
                continue

            movable.append((move, (nr, nc)))

        # 직전 위치가 아닌 칸이 있으면 즉시 되돌아가기를 막는다.
        # 막다른 길처럼 직전 위치만 이동 가능하면 되돌아가기를 허용한다.
        alternatives = [
            candidate
            for candidate in movable
            if candidate[1] != previous_position
        ]
        candidates = alternatives if alternatives else movable

        best_move = None
        best_score = float("-inf")
        self.last_scores = {}

        for move, position in candidates:
            inputs = self.get_inputs(position, goal, grid)
            score = self.bias + sum(
                x * weight for x, weight in zip(inputs, self.weights)
            )
            score -= visited_count.get(position, 0) * self.visit_penalty
            self.last_scores[move] = score

            if score > best_score:
                best_score = score
                best_move = move

        return best_move
