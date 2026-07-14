from datetime import datetime
from pathlib import Path
from statistics import mean

from simulation import run_simulation


PROJECT_DIR = Path(__file__).resolve().parent
DEFAULT_LOGS_DIR = PROJECT_DIR / "logs"


def _save_visualization(results, logs_dir=DEFAULT_LOGS_DIR):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.rcParams["font.family"] = "Malgun Gothic"
    plt.rcParams["axes.unicode_minus"] = False

    logs_path = Path(logs_dir)
    logs_path.mkdir(parents=True, exist_ok=True)

    success_results = [result for result in results if result["success"]]
    success_count = len(success_results)
    failure_count = len(results) - success_count
    success_rate = success_count / len(results) * 100

    perceptron_average = (
        mean(result["perceptron_steps"] for result in success_results)
        if success_results
        else 0
    )
    bfs_average = mean(result["bfs_steps"] for result in results)
    differences = [
        result["difference"]
        for result in success_results
        if result["difference"] is not None
    ]

    experiment_ids = [result["experiment_id"] for result in results]
    perceptron_steps = [result["perceptron_steps"] for result in results]
    bfs_steps = [result["bfs_steps"] for result in results]
    failed_ids = [
        result["experiment_id"]
        for result in results
        if not result["success"]
    ]
    failed_steps = [
        result["perceptron_steps"]
        for result in results
        if not result["success"]
    ]

    figure, axes = plt.subplots(2, 2, figsize=(15, 10))
    figure.suptitle(
        f"퍼셉트론과 BFS 비교 - {len(results)}회 실험",
        fontsize=18,
        fontweight="bold",
    )

    axes[0, 0].bar(
        ["성공", "실패"],
        [success_count, failure_count],
        color=["#2E8B57", "#D9534F"],
    )
    axes[0, 0].set_title(f"성공률: {success_rate:.1f}%")
    axes[0, 0].set_ylabel("실험 횟수")
    axes[0, 0].grid(axis="y", alpha=0.25)

    averages = [perceptron_average, bfs_average]
    bars = axes[0, 1].bar(
        ["퍼셉트론\n(성공 실험)", "BFS\n(전체 맵)"],
        averages,
        color=["#4472C4", "#ED7D31"],
    )
    axes[0, 1].set_title("평균 이동 횟수")
    axes[0, 1].set_ylabel("이동 횟수")
    axes[0, 1].grid(axis="y", alpha=0.25)
    for bar, value in zip(bars, averages):
        axes[0, 1].text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            f"{value:.2f}",
            ha="center",
            va="bottom",
        )

    axes[1, 0].plot(
        experiment_ids,
        perceptron_steps,
        color="#4472C4",
        linewidth=1.2,
        label="퍼셉트론",
    )
    axes[1, 0].plot(
        experiment_ids,
        bfs_steps,
        color="#ED7D31",
        linewidth=1.2,
        label="BFS",
    )
    if failed_ids:
        axes[1, 0].scatter(
            failed_ids,
            failed_steps,
            color="#D9534F",
            marker="x",
            s=35,
            label="실패",
            zorder=3,
        )
    axes[1, 0].set_title("실험별 이동 횟수")
    axes[1, 0].set_xlabel("실험 번호")
    axes[1, 0].set_ylabel("이동 횟수")
    axes[1, 0].legend()
    axes[1, 0].grid(alpha=0.25)

    if differences:
        bin_count = min(15, max(5, len(set(differences))))
        axes[1, 1].hist(
            differences,
            bins=bin_count,
            color="#70AD47",
            edgecolor="white",
        )
        average_difference = mean(differences)
        axes[1, 1].axvline(
            average_difference,
            color="#C00000",
            linestyle="--",
            linewidth=1.5,
            label=f"평균: {average_difference:.2f}",
        )
        axes[1, 1].legend()
        axes[1, 1].set_title("퍼셉트론과 BFS의 이동 횟수 차이")
        axes[1, 1].set_xlabel("BFS 대비 추가 이동 횟수")
        axes[1, 1].set_ylabel("빈도")
        axes[1, 1].grid(axis="y", alpha=0.25)
    else:
        axes[1, 1].text(
            0.5,
            0.5,
            "성공한 퍼셉트론 실험 없음",
            ha="center",
            va="center",
            fontsize=13,
        )
        axes[1, 1].set_axis_off()

    figure.text(
        0.5,
        0.01,
        (
            f"전체: {len(results)}   |   성공: {success_count}   |   "
            f"실패: {failure_count}   |   성공률: {success_rate:.1f}%"
        ),
        ha="center",
        fontsize=11,
    )
    figure.tight_layout(rect=(0, 0.04, 1, 0.95))

    filename = datetime.now().strftime("%Y%m%d_%H%M.png")
    output_path = logs_path / filename
    figure.savefig(output_path, dpi=160, bbox_inches="tight")
    plt.close(figure)

    return output_path


def run_experiments(count=100, save_visualization=True):
    if count <= 0:
        raise ValueError("count는 0보다 커야 합니다.")

    results = []

    for experiment_id in range(1, count + 1):
        result = run_simulation(show=False)
        result["experiment_id"] = experiment_id
        results.append(result)

        status = "성공" if result["success"] else "실패"
        print(
            f"실험 {experiment_id:03d}/{count:03d}: {status} "
            f"(퍼셉트론 {result['perceptron_steps']}회, "
            f"BFS {result['bfs_steps']}회)"
        )

    success_results = [result for result in results if result["success"]]
    success_count = len(success_results)
    failure_count = count - success_count

    print("\n======================")
    print("실험 종료")
    print("======================")
    print(f"총 실험: {len(results)}")
    print(f"성공: {success_count}")
    print(f"실패: {failure_count}")
    print(f"성공률: {success_count / count * 100:.2f}%")

    if success_results:
        average_steps = mean(
            result["perceptron_steps"]
            for result in success_results
        )
        print(f"성공 실험 평균 이동 횟수: {average_steps:.2f}")

    if save_visualization:
        output_path = _save_visualization(results)
        print(f"시각화 저장: {output_path}")

    return results
