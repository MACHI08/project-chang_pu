from simulation import run_simulation


def run_experiments(count=100):

    success = 0

    total_steps = 0

    results = []

    for i in range(count):

        print(f"\n===== 실험 {i+1} =====")

        result = run_simulation(show=False)

        results.append(result)

        if result["success"]:

            success += 1

            total_steps += result["perceptron_steps"]

    print("\n======================")

    print("실험 종료")

    print("======================")

    print(f"총 실험 : {count}")

    print(f"성공 : {success}")

    print(f"실패 : {count-success}")

    if success > 0:

        print(f"평균 이동횟수 : {total_steps/success:.2f}")

    return results