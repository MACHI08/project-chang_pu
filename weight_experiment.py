from copy import deepcopy
from datetime import datetime
from pathlib import Path
from statistics import mean

from map import GridMap
from pathfinding import bfs_steps
from perceptron import DIRECTIONS, PerceptronAgent


PROJECT_DIR = Path(__file__).resolve().parent
DEFAULT_LOGS_DIR = PROJECT_DIR / "logs"


def _run_weight_simulation(
    preference_weight=1.0,
    distance_weight=-1.0,
    max_steps=200,
):
    game_map = GridMap()
    start_position = game_map.player
    goal_position = game_map.goal
    original_grid = deepcopy(game_map.grid)

    agent = PerceptronAgent()
    agent.weights = [preference_weight, distance_weight]

    visited = {start_position}
    steps = 0

    while steps < max_steps and game_map.player != goal_position:
        decision = agent.choose_move(
            game_map.player,
            goal_position,
            game_map.grid,
            game_map.preferences,
            visited,
        )

        move = decision["move"]
        if move is None:
            break

        dr, dc = DIRECTIONS[move]
        row, col = game_map.player
        next_position = (row + dr, col + dc)

        game_map.grid[row][col] = "*"
        game_map.player = next_position
        visited.add(next_position)
        steps += 1

        next_row, next_col = next_position
        game_map.grid[next_row][next_col] = "S"

    success = game_map.player == goal_position
    bfs_result = bfs_steps(original_grid, start_position, goal_position)
    difference = steps - bfs_result if success and bfs_result is not None else None

    return {
        "success": success,
        "perceptron_steps": steps,
        "bfs_steps": bfs_result,
        "difference": difference,
    }


def _summarize_results(results):
    success_results = [result for result in results if result["success"]]
    success_count = len(success_results)
    differences = [
        result["difference"]
        for result in success_results
        if result["difference"] is not None
    ]

    return {
        "success_count": success_count,
        "failure_count": len(results) - success_count,
        "success_rate": success_count / len(results) * 100,
        "average_steps": (
            mean(result["perceptron_steps"] for result in success_results)
            if success_results
            else 0
        ),
        "average_difference": mean(differences) if differences else 0,
    }


def _run_weight_case(
    count,
    label,
    preference_weight=1.0,
    distance_weight=-1.0,
):
    results = [
        _run_weight_simulation(
            preference_weight=preference_weight,
            distance_weight=distance_weight,
        )
        for _ in range(count)
    ]
    summary = _summarize_results(results)
    summary.update(
        {
            "label": label,
            "preference_weight": preference_weight,
            "distance_weight": distance_weight,
        }
    )
    return summary


def _save_weight_visualization(
    summaries,
    group_title,
    filename_suffix,
    colors,
    logs_dir=DEFAULT_LOGS_DIR,
):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.rcParams["font.family"] = "Malgun Gothic"
    plt.rcParams["axes.unicode_minus"] = False

    logs_path = Path(logs_dir)
    logs_path.mkdir(parents=True, exist_ok=True)

    figure, axes = plt.subplots(1, 3, figsize=(16, 5))
    figure.suptitle(f"{group_title} 테스트 결과", fontsize=18, fontweight="bold")

    metrics = [
        ("success_rate", "성공률", "%"),
        ("average_steps", "성공 실험 평균 이동 횟수", "회"),
        ("average_difference", "BFS 대비 평균 추가 이동", "회"),
    ]
    labels = [summary["label"] for summary in summaries]

    for axis, (metric_key, metric_title, unit) in zip(axes, metrics):
        values = [summary[metric_key] for summary in summaries]
        bars = axis.bar(labels, values, color=colors)
        axis.set_title(metric_title)
        axis.set_ylabel(unit)
        axis.grid(axis="y", alpha=0.25)
        axis.tick_params(axis="x", rotation=20)

        for bar, value in zip(bars, values):
            axis.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height(),
                f"{value:.2f}",
                ha="center",
                va="bottom",
                fontsize=9,
            )

    figure.tight_layout(rect=(0, 0, 1, 0.9))

    filename = datetime.now().strftime(f"%Y%m%d_%H%M_{filename_suffix}.png")
    output_path = logs_path / filename
    figure.savefig(output_path, dpi=160, bbox_inches="tight")
    plt.close(figure)

    return output_path


def run_weight_experiments(count=500):
    if count <= 0:
        raise ValueError("count는 0보다 커야 합니다.")

    preference_summaries = [ # 선호도에 대한 가중치 값들
        _run_weight_case(count, "무시 0", preference_weight=0.0),
        _run_weight_case(count, "기본 1.0", preference_weight=1.0),
        _run_weight_case(count, "강함 10", preference_weight=10.0),
        _run_weight_case(count, "선호 우선 50", preference_weight=50.0),
    ]
    distance_summaries = [ # 거리 비교에 관한 가중치 값들
        _run_weight_case(count, "거리 무시 0", distance_weight=0.0),
        _run_weight_case(count, "약함 -0.1", distance_weight=-0.1),
        _run_weight_case(count, "기본 -1.0", distance_weight=-1.0),
        _run_weight_case(count, "거리 우선 -10", distance_weight=-10.0),
    ]

    preference_output_path = _save_weight_visualization(
        preference_summaries,
        "선호도 가중치",
        "preference_weight",
        ["#DCEAF7", "#8BB8DF", "#3F83BF", "#155A92"],
    )
    distance_output_path = _save_weight_visualization(
        distance_summaries,
        "거리 영향 가중치",
        "distance_weight",
        ["#FDE1D3", "#F5A878", "#E76F51", "#A63D2D"],
    )
    print(f"선호도 가중치 시각화 저장: {preference_output_path}")
    print(f"거리 영향 가중치 시각화 저장: {distance_output_path}")
    return preference_output_path, distance_output_path


if __name__ == "__main__":
    run_weight_experiments()
