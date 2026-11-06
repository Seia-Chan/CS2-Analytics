
import json
import os
import sys
import time
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from pydantic import ValidationError

from cs2_analytics.models import PlayerAnalysis


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
WEB_DATA_DIR = PROJECT_ROOT / "docs" / "data"

load_dotenv(PROJECT_ROOT / ".env")


def analyze_player(player_name):
    filename = player_name.lower()

    summary_path = DATA_DIR / f"{filename}_summary.json"

    if not summary_path.exists():
        raise FileNotFoundError(f"找不到選手資料：{summary_path}")

    with summary_path.open("r", encoding="utf-8") as file:
        stats = json.load(file)

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError("找不到 GEMINI_API_KEY，請檢查環境變數")

    client = genai.Client(api_key=api_key)

    prompt = f"""
你是一位專業 Counter-Strike 2 電競數據分析師。

請根據以下真實統計資料，使用繁體中文分析選手表現。

選手資料：
{json.dumps(stats, ensure_ascii=False, indent=2)}

分析規則：
1. 僅根據提供的數據分析，不得捏造比賽結果。
2. 區分生涯統計與近期統計。
3. 近期數據只包含最近 {stats['recent']['sampleSize']} 張地圖。
4. Rating 是 Cito Rating，不是 HLTV Rating。
5. 分析 K/D、ADR、KAST、Rating、爆頭率。
6. 說明選手的優勢、弱點與近期表現。
7. 若缺少資料，明確說明，不要自行推測。
8. 不要把統計相關性當成因果關係。
"""

    print(f"正在使用 Gemini 分析 {stats['playerName']}...")

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=prompt,
                config={
                    "response_mime_type": "application/json",
                    "response_json_schema":
                        PlayerAnalysis.model_json_schema()
                }
            )

            if not response.text:
                raise ValueError("Gemini 沒有回傳分析內容")

            analysis = PlayerAnalysis.model_validate_json(
                response.text
            )

            output = analysis.model_dump()

            DATA_DIR.mkdir(parents=True, exist_ok=True)
            WEB_DATA_DIR.mkdir(parents=True, exist_ok=True)

            for directory in [DATA_DIR, WEB_DATA_DIR]:
                output_path = directory / f"{filename}_analysis.json"

                output_path.write_text(
                    json.dumps(
                        output,
                        ensure_ascii=False,
                        indent=2
                    ),
                    encoding="utf-8"
                )

                print(f"已儲存：{output_path}")

            print("AI 分析完成！")
            print(analysis.overall_assessment)
            return

        except (ValidationError, ValueError) as error:
            raise RuntimeError(
                f"{player_name} AI 回傳格式錯誤：{error}"
            ) from error

        except Exception as error:
            print(f"第 {attempt + 1} 次呼叫失敗：{error}")

            if attempt < 2:
                wait_seconds = 5 * (2 ** attempt)
                print(f"等待 {wait_seconds} 秒後重試...")
                time.sleep(wait_seconds)

        raise RuntimeError(
            f"{player_name} Gemini 分析失敗，已重試 3 次"
)


def main():
    player_name = sys.argv[1] if len(sys.argv) > 1 else "niko"
    analyze_player(player_name)


if __name__ == "__main__":
    main()
