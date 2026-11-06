
import argparse

from cs2_analytics.api_client import download_player
from cs2_analytics.process_stats import main as process_stats
from cs2_analytics.ai_analysis import analyze_player


PLAYERS = ["NiKo", "m0NESY", "ZywOo", "donk"]


def main():
    parser = argparse.ArgumentParser(
        description="CS2 Analytics 資料更新工具"
    )

    parser.add_argument(
        "--ai",
        action="store_true",
        help="同時執行 Gemini AI 分析"
    )

    args = parser.parse_args()

    print("=== CS2 Analytics ===")

    print("\n[1/3] 下載選手資料")

    failed_players = []

    for player in PLAYERS:
        try:
            download_player(player)
            print(f"{player} 下載成功")
        except Exception as error:
            print(f"{player} 下載失敗：{error}")
            failed_players.append(player)

    if failed_players:
        raise RuntimeError(
            f"以下選手資料下載失敗：{', '.join(failed_players)}"
        )

    print("\n[2/3] 處理統計資料")
    process_stats()

    if args.ai:
        print("\n[3/3] Gemini AI 分析")

        failed_ai_players = []

        for player in PLAYERS:
            try:
                analyze_player(player)
                print(f"{player} AI 分析成功")
            except Exception as error:
                print(f"{player} AI 分析失敗：{error}")
                failed_ai_players.append(player)

        if failed_ai_players:
            raise RuntimeError(
                f"以下選手 AI 分析失敗：{', '.join(failed_ai_players)}"
            )
    else:
        print("\n[3/3] 已略過 AI 分析")

    print("\n=== 執行完成 ===")


if __name__ == "__main__":
    main()
