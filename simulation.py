import time

from map import GridMap
from perceptron import PerceptronAgent
from pathfinding import bfs_steps


def run_simulation(show=True):

    game_map = GridMap()
    agent = PerceptronAgent()

    visited_count = {}

    step = 0
    max_step = 200

    while step < max_step:

        if show:

            print("\n====================")
            print(f"STEP {step}")

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

            break

        direction = {
            "w": (-1,0),
            "s": (1,0),
            "a": (0,-1),
            "d": (0,1)
        }

        dr,dc = direction[move]

        r,c = game_map.player

        nr=r+dr
        nc=c+dc

        if game_map.grid[r][c]!="F":
            game_map.grid[r][c]="*"

        game_map.player=(nr,nc)

        if game_map.player==game_map.goal:

            game_map.grid[nr][nc]="S"

            break

        game_map.grid[nr][nc]="S"

        step+=1

        if show:
            time.sleep(0.1)

    success = game_map.player == game_map.goal

    bfs_result = bfs_steps(
        game_map.grid,
        game_map.player if not success else game_map.goal,
        game_map.goal
    )

    return {

        "success": success,

        "perceptron_steps": step+1 if success else step,

        "bfs_steps": bfs_result,

        "difference":
            None if bfs_result is None
            else (step+1)-bfs_result,

        "visited": len(visited_count)
    }