
import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai.errors import APIError


def main():
    project_root = Path(__file__).resolve().parents[2]
    load_dotenv(project_root / ".env")

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        print("錯誤：找不到 GEMINI_API_KEY")
        return

    client = genai.Client(api_key=api_key)

    try:
        print("正在查詢 Gemini 模型...\n")

        for model in client.models.list():
            if "flash" in model.name.lower():
                print(model.name)

    except APIError as e:
        print(f"查詢失敗：{e.code}")
        print(e.message)

    finally:
        client.close()


if __name__ == "__main__":
    main()
