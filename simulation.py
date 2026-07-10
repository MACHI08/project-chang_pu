import time

from map import GridMap
from perceptron import PerceptronAgent
from analysis import analyze


def run_simulation():

    game_map = GridMap()

    agent = PerceptronAgent()

    visited_count = {}

    step = 0
    max_step = 200

    while step < max_step:

        print("\n==========================")
        print("Step :", step)

        game_map.display()

        visited_count[game_map.player] = visited_count.get(
            game_map.player,
            0
        ) + 1

        move = agent.choose_move(
            game_map.player,
            game_map.goal,
            game_map.grid,
            visited_count
        )

        if move is None:
            print("더 이상 이동 불가")
            break

        direction = {
            "w": (-1, 0),
            "s": (1, 0),
            "a": (0, -1),
            "d": (0, 1)
        }

        dr, dc = direction[move]

        r, c = game_map.player

        nr = r + dr
        nc = c + dc

        if game_map.grid[r][c] != "F":
            game_map.grid[r][c] = "*"

        game_map.player = (nr, nc)

        if game_map.player == game_map.goal:

            game_map.grid[nr][nc] = "S"

            print("\n목표 도착!")

            game_map.display()

            analyze(
                game_map.grid,
                game_map.player,
                game_map.goal,
                step + 1
            )

            return

        game_map.grid[nr][nc] = "S"

        step += 1

        time.sleep(0.1)

    print("\n실패")

    analyze(
        game_map.grid,
        game_map.player,
        game_map.goal,
        step
    )