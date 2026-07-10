class PerceptronAgent:

    def __init__(self):

        # 입력 순서
        #
        # x0 = goal_up
        # x1 = goal_down
        # x2 = goal_left
        # x3 = goal_right
        # x4 = obstacle_up
        # x5 = obstacle_down
        # x6 = obstacle_left
        # x7 = obstacle_right

        self.weights = [
            5,
            5,
            5,
            5,
            -8,
            -8,
            -8,
            -8
        ]

        self.bias = 0


    def get_inputs(self, player, goal, grid):

        rows = len(grid)
        cols = len(grid[0])

        r, c = player

        goal_up = int(goal[0] < r)
        goal_down = int(goal[0] > r)
        goal_left = int(goal[1] < c)
        goal_right = int(goal[1] > c)

        obstacle_up = int(
            r == 0 or grid[r-1][c] == "#"
        )

        obstacle_down = int(
            r == rows-1 or grid[r+1][c] == "#"
        )

        obstacle_left = int(
            c == 0 or grid[r][c-1] == "#"
        )

        obstacle_right = int(
            c == cols-1 or grid[r][c+1] == "#"
        )

        return [
            goal_up,
            goal_down,
            goal_left,
            goal_right,
            obstacle_up,
            obstacle_down,
            obstacle_left,
            obstacle_right
        ]


    def activation(self, x):

        return 1 if x > 0 else 0


    def choose_move(self, player, goal, grid, visited_count):

        directions = {
            "w": (-1,0),
            "s": (1,0),
            "a": (0,-1),
            "d": (0,1)
        }

        best_move = None
        best_score = float("-inf")

        rows = len(grid)
        cols = len(grid[0])

        for move, (dr, dc) in directions.items():

            nr = player[0] + dr
            nc = player[1] + dc

            if not (0 <= nr < rows and 0 <= nc < cols):
                continue

            if grid[nr][nc] == "#":
                continue

            # 이동한 위치를 기준으로 입력 생성
            inputs = self.get_inputs(
                (nr, nc),
                goal,
                grid
            )

            score = self.bias

            for x, w in zip(inputs, self.weights):
                score += x * w

            # 방문 패널티
            score -= visited_count.get((nr, nc), 0) * 2

            if score > best_score:

                best_score = score
                best_move = move

        return best_move