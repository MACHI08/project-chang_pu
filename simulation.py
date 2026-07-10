import time

from map import GridMap
from perceptron import PerceptronAgent


def run_simulation(show=True):

    game_map = GridMap()
    agent = PerceptronAgent()

    visited_count = {}

    step = 0
    max_step = 200

    while step < max_step:

        if show:
            print("\n========================")
            print(f"Step : {step}")
            game_map.display()
            print()

        # 현재 위치 방문 기록
        visited_count[game_map.player] = visited_count.get(game_map.player, 0) + 1

        move = agent.choose_move(
            game_map.player,
            game_map.goal,
            game_map.grid,
            visited_count
        )

        if move is None:

            return {
                "success": False,
                "steps": step,
                "visited": len(visited_count)
            }

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

        # 이동 전 위치 표시
        if game_map.grid[r][c] != "F":
            game_map.grid[r][c] = "*"

        game_map.player = (nr, nc)

        # 목표 도착
        if game_map.player == game_map.goal:

            game_map.grid[nr][nc] = "S"

            if show:
                print("\n목표 도착!")
                game_map.display()
                print(f"\n이동 횟수 : {step+1}")

            return {
                "success": True,
                "steps": step + 1,
                "visited": len(visited_count)
            }

        game_map.grid[nr][nc] = "S"

        step += 1

        if show:
            time.sleep(0.15)

    return {
        "success": False,
        "steps": step,
        "visited": len(visited_count)
    }