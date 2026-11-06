
import json
from pathlib import Path
from statistics import mean

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"


def load_json(filename):
    with (DATA_DIR / filename).open("r", encoding="utf-8") as file:
        return json.load(file)


def safe_divide(a, b):
    if a is None or b is None or b == 0:
        return None
    return round(a / b, 4)


def average_field(rows, field):
    values = [
        row[field]
        for row in rows
        if isinstance(row.get(field), (int, float))
        and not isinstance(row[field], bool)
    ]
    return round(mean(values), 4) if values else None


def process_player_stats(data):
    totals = data["totals"]
    scope = data.get("totalsScope", {})
    rows_scope = data.get("rowsScope", {})
    rows = data.get("rows", [])

    kills = totals["kills"]
    deaths = totals["deaths"]
    maps = data["maps"]

    recent_maps = []

    for row in rows:
        recent_maps.append({
            "matchId": row.get("matchId"),
            "mapName": row.get("mapName"),
            "date": row.get("startsAt"),
            "team": row.get("teamName"),
            "kills": row.get("kills"),
            "deaths": row.get("deaths"),
            "assists": row.get("assists"),
            "kdRatio": safe_divide(
                row.get("kills"),
                row.get("deaths")
            ),
            "adr": row.get("adr"),
            "kast": row.get("kast"),
            "rating": row.get("rating"),
            "ratingVersion": row.get("ratingVersion"),
            "headshotRate": row.get("headshotPercent"),
            "firstKills": row.get("firstKills"),
            "firstDeaths": row.get("firstDeaths"),
        })

    summary = {
        "playerId": data["playerId"],
        "playerName": rows[0].get("playerName") if rows else None,
        "source": "Cito API",
        "asOf": scope.get("asOf"),
        "career": {
            "matches": totals["matches"],
            "maps": maps,
            "kills": kills,
            "deaths": deaths,
            "assists": totals.get("assists"),
            "headshots": totals.get("headshots"),
            "kdRatio": safe_divide(kills, deaths),
            "killsPerMap": safe_divide(kills, maps),
            "headshotRate": totals.get("headshotPercent"),
            "headshotCoverage": totals.get("headshotsCoverage"),
        },
        "recent": {
            "sampleSize": len(rows),
            "totalAvailableMaps": rows_scope.get("total"),
            "hasMore": rows_scope.get("hasMore"),
            "averageADR": average_field(rows, "adr"),
            "averageKAST": average_field(rows, "kast"),
            "averageRating": average_field(rows, "rating"),
            "ratingVersion": (
                rows[0].get("ratingVersion") if rows else None
            ),
            "maps": recent_maps,
        },
        "ratingNote": (
            "Rating values come from Cito API, "
            "not HLTV Rating."
        ),
    }

    return summary



def main():
    stats_files = sorted(DATA_DIR.glob("*_stats.json"))

    if not stats_files:
        print("找不到任何選手統計資料")
        return

    website_data_dir = PROJECT_ROOT / "docs" / "data"
    website_data_dir.mkdir(parents=True, exist_ok=True)

    players = []

    for stats_file in stats_files:
        filename = stats_file.name.removesuffix("_stats.json")

        print(f"\n正在處理：{filename}")

        data = load_json(stats_file.name)
        summary = process_player_stats(data)

        summary_filename = f"{filename}_summary.json"
        summary_path = DATA_DIR / summary_filename

        with summary_path.open("w", encoding="utf-8") as file:
            json.dump(summary, file, ensure_ascii=False, indent=2)

        website_path = website_data_dir / summary_filename

        with website_path.open("w", encoding="utf-8") as file:
            json.dump(summary, file, ensure_ascii=False, indent=2)

        recent_maps = summary["recent"]["maps"]
        team = recent_maps[0].get("team") if recent_maps else None

        players.append({
            "id": summary["playerId"],
            "name": summary["playerName"] or filename,
            "team": team or "Unknown",
            "dataFile": summary_filename
        })

        print(f"已產生：{summary_filename}")

    players_path = website_data_dir / "players.json"

    with players_path.open("w", encoding="utf-8") as file:
        json.dump(
            {"players": players},
            file,
            ensure_ascii=False,
            indent=2
        )

    print("\n所有選手資料處理完成！")
    print(f"共處理 {len(players)} 位選手")
    print(f"網站資料位置：{website_data_dir}")


if __name__ == "__main__":
    main()

