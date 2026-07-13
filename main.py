from simulation import run_simulation
from experiment import run_experiments


def main():

    while True:

        print("\n===== 메뉴 =====")
        print("1. 시뮬레이션")
        print("2. 100회 실험")
        print("0. 종료")

        choice = input("선택 : ")

        if choice == "1":
            run_simulation(show=True)

        elif choice == "2":
            run_experiments(100)

        elif choice == "0":
            break

        else:
            print("잘못된 입력입니다.")


if __name__ == "__main__":
    main()