
import os
import json
import re
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")

BASE_URL = "https://api.citoapi.com/api/v1/cs2"
API_KEY = os.getenv("CITO_API_KEY")


def get_data(endpoint, params=None):
    if not API_KEY:
        raise ValueError("找不到 CITO_API_KEY，請檢查 .env")

    response = requests.get(
        f"{BASE_URL}/{endpoint}",
        headers={"x-api-key": API_KEY},
        params=params,
        timeout=30
    )

    response.raise_for_status()
    result = response.json()

    if not result.get("success"):
        raise ValueError(f"API 回傳失敗：{result}")

    return result["data"]


def save_json(filename, data):
    output_dir = PROJECT_ROOT / "data"
    output_dir.mkdir(exist_ok=True)

    output_file = output_dir / filename

    output_file.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print(f"已儲存：{output_file}")


def download_player(player_name):
    print(f"\n正在搜尋選手：{player_name}")

    players = get_data(
        "players/search",
        {"q": player_name}
    )

    if not isinstance(players, list) or not players:
        print(f"找不到選手：{player_name}")
        return

    player = next(
        (
            p for p in players
            if p.get("nickname", "").casefold()
            == player_name.casefold()
        ),
        None
    )

    if player is None:
        print("沒有找到完全符合名稱的選手。")
        print("搜尋結果：")

        for p in players:
            print(p.get("nickname"), p.get("id"))

        return

    player_id = player["id"]
    nickname = player["nickname"]

    print(f"找到選手：{nickname}")
    print(f"選手 ID：{player_id}")
    print("正在下載統計資料...")

    stats = get_data(
        f"players/{player_id}/stats",
        {"limit": 10}
    )

    filename = re.sub(
        r"[^a-z0-9_-]",
        "_",
        nickname.lower()
    )

    save_json(f"{filename}_profile.json", player)
    save_json(f"{filename}_stats.json", stats)

    print(f"{nickname} 資料下載完成！")


def main():
    player_names = sys.argv[1:] or ["NiKo"]

    try:
        for name in player_names:
            download_player(name)

    except requests.HTTPError as e:
        print(f"HTTP 錯誤：{e.response.status_code}")
        print(e.response.text[:500])

    except requests.RequestException as e:
        print(f"網路連線錯誤：{e}")

    except (ValueError, KeyError) as e:
        print(f"資料處理錯誤：{e}")


if __name__ == "__main__":
    main()
