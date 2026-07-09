from map import GridMap

def run_simulation():
    game_map = GridMap()

    while True:
        print("\n===== 현재 맵 =====")
        game_map.display()

        print(f"\n현재 위치 : {game_map.player}")
        print(f"목표 위치 : {game_map.goal}")

        move = input("\n이동(W/A/S/D, 종료 Q) : ").lower()

        if move == "q":
            break

        row, col = game_map.player

        if move == "w":
            row -= 1
        elif move == "s":
            row += 1
        elif move == "a":
            col -= 1
        elif move == "d":
            col += 1
        else:
            continue

        # 맵 밖으로 못 나가게
        if not (0 <= row < 5 and 0 <= col < 5):
            print("맵 밖입니다.")
            continue

        # 장애물 확인
        if game_map.grid[row][col] == "#":
            print("장애물입니다.")
            continue

        # 기존 위치 지우기
        old_r, old_c = game_map.player
        game_map.grid[old_r][old_c] = "."

        # 이동
        game_map.player = (row, col)

        # 목표 도착
        if game_map.player == game_map.goal:
            game_map.grid[row][col] = "S"

            print("\n===== 현재 맵 =====")
            game_map.display()

            print("\n🎉 목표 도착!")
            break

        game_map.grid[row][col] = "S"