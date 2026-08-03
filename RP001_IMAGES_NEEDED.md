# RP-001 所需圖片清單

只列真正需要、且已存在或可由現有結果產生的圖片,不濫列。

## 已具備,直接可用(11 張,`rp001_data/phase2a/charts/`)

全部由真實結果產生,無示意資料。用途對照見 `RP001_FIGURE_INDEX.md`。

01_universe_coverage.png、02_missingness_distribution.png、03_institutional_category_history.png、04_rolling_ic.png、05_break_before_after.png、06_liquidity_groups.png、07_hypothesis_verdicts.png、08_exploratory_vs_confirmatory.png、09_interaction_residualization.png、10_data_quality_summary.png、11_research_lifecycle_timeline.png

## 不需要額外製作的項目

- **不需要**手繪示意流程圖——`11_research_lifecycle_timeline.png` 已用真實 commit 日期呈現生命週期,足以取代示意圖
- **不需要**額外的「架構圖」——若面試或書面資料需要系統架構說明,直接使用 `README.md` 中的目錄結構區塊(純文字,已足夠清楚),不必畫成圖片
- **不需要**個人照片或校徽等裝飾性素材——本作品集內容以研究本身為主,不需要視覺裝飾

## 若有餘力才考慮製作(非必要)

- **GitHub commit 歷史截圖**:如果要放進紙本或簡報版作品集(而非直接連結 GitHub),可截取 `git log --oneline --graph` 的一段輸出作為視覺佐證,證明每個階段獨立 commit——但這屬於「有更好」而非「必要」,線上作品集直接附連結即可,不必截圖
- **面試簡報用的單頁摘要圖卡**:若需要在口頭面試中出示紙本,可將 `07_hypothesis_verdicts.png` 與關鍵數字合併成一張 A4 摘要卡,但這是排版工作,不是新圖表,直接沿用 `RP001_PORTFOLIO_LAYOUT_GUIDE.md` 的版面建議即可產生

## 明確不要製作的項目(避免濫列)

- 不要製作示意性的「因子邏輯圖」(如畫箭頭表示「外資買超→股價上漲」)——這類圖具誤導性,暗示因果關係已被證實,與研究結論矛盾
- 不要製作投資報酬/績效類圖表(如「假設投入 100 萬元」的模擬曲線)——本研究從未進行回測,製作這類圖表會與研究誠信原則直接衝突
- 不要為每個 Deviation(D-01 至 D-08)個別製圖——`10_data_quality_summary.png` 的彙總呈現已足夠,逐項製圖只會稀釋重點
