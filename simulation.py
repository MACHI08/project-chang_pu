from copy import deepcopy
import time

from map import GridMap
from pathfinding import bfs_steps
from perceptron import DIRECTIONS, DIRECTION_NAMES, PerceptronAgent


def _display_position(position):
    return position[0] + 1, position[1] + 1


def _print_step(game_map, step, decision):
    print("\n====================")
    print(f"STEP {step}")
    game_map.display()
    print(f"현재 위치: {_display_position(game_map.player)}")
    print(f"목표 위치: {_display_position(game_map.goal)}")
    print("인접 타일 입력과 선형 점수:")

    for move in DIRECTIONS:
        direction_name = DIRECTION_NAMES[move]
        raw_position = decision["positions"][move]
        tile_inputs = decision["inputs"][move]
        reason = decision["excluded_reasons"][move]

        if reason == "맵 밖":
            print(
                f"  {move} ({direction_name}): "
                f"후보 제외 - {reason}"
            )
            continue

        position = _display_position(raw_position)
        if reason is not None:
            print(
                f"  {move} ({direction_name}) {position}: "
                f"후보 제외 - {reason}"
            )
            continue

        preference, distance = tile_inputs
        score = decision["scores"][move]
        print(
            f"  {move} ({direction_name}) {position}: "
            f"[선호도={preference:.3f}, 거리={distance:.3f}] "
            f"점수={score:.3f}"
        )

    selected_move = decision["move"]
    if selected_move is None:
        print("최종 선택 방향: 없음 - 이동 가능한 미방문 칸 없음")
    else:
        print(
            f"최종 선택 방향: {selected_move} "
            f"({DIRECTION_NAMES[selected_move]})"
        )


def run_simulation(
    show=True,
    max_steps=200,
    step_delay=0.5,
    preference_min=0.48,
    preference_max=0.52,
):
    if max_steps < 0:
        raise ValueError("max_steps는 0 이상이어야 합니다.")
    if step_delay < 0:
        raise ValueError("step_delay는 0 이상이어야 합니다.")

    game_map = GridMap(
        preference_min=preference_min,
        preference_max=preference_max,
    )
    start_position = game_map.player
    goal_position = game_map.goal
    original_grid = deepcopy(game_map.grid)

    agent = PerceptronAgent()
    visited = {start_position}
    perceptron_path = [start_position]
    steps = 0

    while steps < max_steps and game_map.player != goal_position:
        decision = agent.choose_move(
            game_map.player,
            goal_position,
            game_map.grid,
            game_map.preferences,
            visited,
        )

        if show:
            _print_step(game_map, steps, decision)
            time.sleep(step_delay)

        move = decision["move"]
        if move is None:
            break

        dr, dc = DIRECTIONS[move]
        row, col = game_map.player
        next_position = (row + dr, col + dc)

        game_map.grid[row][col] = "*"
        game_map.player = next_position
        visited.add(next_position)
        perceptron_path.append(next_position)
        steps += 1

        next_row, next_col = next_position
        game_map.grid[next_row][next_col] = "S"

    success = game_map.player == goal_position
    bfs_result = bfs_steps(original_grid, start_position, goal_position)
    difference = steps - bfs_result if success and bfs_result is not None else None

    if show:
        print("\n====================")
        print("시뮬레이션 종료")
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
        "visited": len(visited),
        "perceptron_path": perceptron_path,
        "start": start_position,
        "goal": goal_position,
    }
