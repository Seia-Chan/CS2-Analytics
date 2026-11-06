
from cs2_analytics.models import PlayerStats, PlayerAnalysis


def main():
    stats = PlayerStats(
        player="NiKo",
        team="Falcons",
        rating=1.25,
        adr=85.4,
        kast=73.2,
        kd=1.18,
        headshot=52.6
    )

    analysis = PlayerAnalysis(
        player=stats.player,
        overview="這名選手具有良好的傷害輸出能力。",
        strengths=[
            "ADR 達到 85.4",
            "K/D 達到 1.18"
        ],
        weaknesses=[
            "缺少逐場資料，無法確認近期穩定性"
        ],
        conclusion="需要更多比賽資料才能完成全面評估。"
    )

    print("=== 選手數據 ===")
    print(stats.model_dump_json(indent=2))

    print("\n=== 分析結果 ===")
    print(analysis.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
