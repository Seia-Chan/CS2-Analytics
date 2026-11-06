# CS2 Analytics

CS2 Analytics 是一個以 Counter-Strike 2 職業選手統計資料為基礎的數據分析網站，整合 Cito API、Python、Gemini AI 與 GitHub Actions，提供選手數據視覺化、選手比較及 AI 表現分析。

## 網站連結

https://seia-chan.github.io/CS2-Analytics/

## 主要功能

1. **選手統計資料**：展示 NiKo、m0NESY、ZywOo、donk 四位選手的統計數據。
2. **數據視覺化**：透過折線圖與長條圖呈現選手表現。
3. **選手比較**：比較不同選手的統計數據。
4. **Gemini AI 分析**：根據實際統計資料，自動產生繁體中文選手表現分析。
5. **自動資料更新**：使用 GitHub Actions 定期取得最新資料、產生 AI 分析並更新網站。

## 使用技術

| 技術 | 用途 |
|---|---|
| Python | API 資料取得與處理 |
| uv | Python 專案與套件管理 |
| Cito API | CS2 職業選手統計資料來源 |
| Gemini API | AI 選手表現分析 |
| Pydantic | AI 回傳資料格式驗證 |
| HTML / JavaScript | 網站介面與資料呈現 |
| GitHub Actions | 自動更新與 Commit |
| GitHub Pages | 靜態網站部署 |

## 自動更新流程

1. GitHub Actions 定期或手動啟動 Workflow。
2. Python 從 Cito API 下載選手統計資料。
3. 整理統計資料並輸出 JSON。
4. Gemini AI 根據統計資料產生繁體中文分析。
5. 將 JSON 儲存至 `docs/data/`。
6. GitHub Actions 偵測資料變更並自動 Commit、Push。
7. GitHub Pages 部署更新後的網站。

## API Key 安全管理

本專案使用環境變數管理 API Key。

- 本機透過 `.env` 讀取金鑰。
- `.gitignore` 排除 `.env`，避免金鑰被提交。
- GitHub Actions 使用 Repository Secrets。
- 不在程式碼、公開 JSON 或 README 中儲存真實 API Key。

## 資料說明

- 選手 Rating 使用 Cito Rating，並非 HLTV Rating。
- 生涯統計與近期統計分開處理。
- 近期統計以 API 提供的最近地圖資料為基礎。
- Gemini AI 僅根據取得的統計資料進行分析，不應將 AI 產生的文字視為已驗證的比賽事實。

## 本機執行

### 1. 安裝套件

安裝 uv 後，在專案根目錄執行：

```powershell
uv sync
```

### 2. 設定 API Key

在專案根目錄建立 `.env`，填入自己的 API Key：

```env
CITO_API_KEY=your_cito_api_key
GEMINI_API_KEY=your_gemini_api_key
```

請勿將 `.env` 提交至 GitHub。

### 3. 執行資料更新與 AI 分析

```powershell
uv run python -m cs2_analytics.main --ai
```

### 4. 啟動網站

```powershell
uv run python -m http.server 8000 --directory docs
```

在瀏覽器開啟：

http://localhost:8000

## AI 使用說明

### 使用的 AI 工具

- **Gemini API**：分析 CS2 職業選手統計資料。
- **ChatGPT**：協助程式設計、除錯、文件整理及 GitHub Actions 設定。

### 使用的 LLM 技術

本專案使用 Structured Output（結構化輸出）。

透過 Pydantic 定義 JSON Schema，讓 Gemini API
依照指定格式回傳選手分析結果。

分析內容包含：

1. 整體評價
2. 選手優勢
3. 選手弱點
4. 近期表現
5. 分析結論

### 自行修改與驗證

開發過程中，針對 API 資料處理、JSON 格式、
網站呈現及 GitHub Actions 工作流程進行調整。

使用本機執行結果、Pydantic 格式驗證、
GitHub Actions 執行紀錄及 GitHub Pages 網站測試，
確認程式可以正常運作。

AI 產生的分析僅供參考，
不代表已驗證的比賽事實。
