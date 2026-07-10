from pathfinding import bfs


def compare_algorithms(grid, start, goal, perceptron_steps):

    bfs_path = bfs(grid, start, goal)

    if bfs_path is None:

        return {
            "perceptron_steps": perceptron_steps,
            "bfs_steps": None,
            "difference": None
        }

    bfs_steps = len(bfs_path) - 1

    return {
        "perceptron_steps": perceptron_steps,
        "bfs_steps": bfs_steps,
        "difference": perceptron_steps - bfs_steps
    }


def print_result(result):

    print("\n============================")
    print("실험 결과")
    print("============================")

    print(f"퍼셉트론 이동 횟수 : {result['perceptron_steps']}")

    if result["bfs_steps"] is None:
        print("BFS : 경로 없음")
        return

    print(f"BFS 이동 횟수 : {result['bfs_steps']}")
    print(f"차이 : {result['difference']}")