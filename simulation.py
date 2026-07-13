from copy import deepcopy

from map import GridMap
from pathfinding import bfs_steps
from perceptron import PerceptronAgent


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


def _print_step(game_map, step, scores, move):
    print("\n====================")
    print(f"STEP {step}")
    print(f"현재 위치: {game_map.player}")
    game_map.display()

    if scores:
        print("후보별 점수:")
        for candidate, score in scores.items():
            print(f"  {candidate} ({DIRECTION_NAMES[candidate]}): {score}")
    else:
        print("후보별 점수: 이동 가능한 후보 없음")

    if move is None:
        print("선택 방향: 없음")
    else:
        print(f"선택 방향: {move} ({DIRECTION_NAMES[move]})")


def run_simulation(show=True, max_steps=200, visit_penalty=2):
    if max_steps < 0:
        raise ValueError("max_steps는 0 이상이어야 합니다.")

    game_map = GridMap()
    start_position = game_map.player
    goal_position = game_map.goal

    # 퍼셉트론 이동 흔적('*', 'S')이 BFS 결과에 영향을 주지 않도록
    # 이동을 시작하기 전 원본 격자를 별도로 보관한다.
    original_grid = deepcopy(game_map.grid)

    agent = PerceptronAgent(visit_penalty=visit_penalty)
    visited_count = {start_position: 1}
    previous_position = None
    path = [start_position]
    steps = 0

    while steps < max_steps and game_map.player != goal_position:
        move = agent.choose_move(
            game_map.player,
            goal_position,
            game_map.grid,
            visited_count,
            previous_position,
        )

        if show:
            _print_step(game_map, steps, agent.last_scores, move)

        if move is None:
            break

        dr, dc = DIRECTIONS[move]
        r, c = game_map.player
        next_position = (r + dr, c + dc)

        if game_map.grid[r][c] != "F":
            game_map.grid[r][c] = "*"

        previous_position = game_map.player
        game_map.player = next_position
        path.append(next_position)
        steps += 1

        visited_count[next_position] = visited_count.get(next_position, 0) + 1
        nr, nc = next_position
        game_map.grid[nr][nc] = "S"

    success = game_map.player == goal_position
    bfs_result = bfs_steps(original_grid, start_position, goal_position)
    difference = steps - bfs_result if success and bfs_result is not None else None

    if show:
        print("\n====================")
        print("시뮬레이션 종료")
        print(f"현재 위치: {game_map.player}")
        game_map.display()
        print(f"성공 여부: {success}")
        print(f"퍼셉트론 이동 횟수: {steps}")
        print(f"BFS 이동 횟수: {bfs_result}")
        print(f"차이: {difference}")

    return {
        "success": success,
        "perceptron_steps": steps,
        "bfs_steps": bfs_result,
        "difference": difference,
        "visited": len(visited_count),
        "path": path,
    }
