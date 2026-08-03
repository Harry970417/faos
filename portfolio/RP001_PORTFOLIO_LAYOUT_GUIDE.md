# RP-001 Portfolio Layout Guide

版面規劃建議,不是最終排版檔案。文字內容來源:`portfolio/RP001_PORTFOLIO_ONE_PAGE.md`、`research/RP001_RESEARCH_SUMMARY_3TO5P.md`。

## 一頁版本版面

**建議單欄配置,由上到下:**

1. 標題 + 一句話研究問題(不超過 20 字)
2. 「為什麼重要」——2-3 句話,不用條列
3. 研究流程——橫向兩階段流程圖(探索性 → 確認性),每階段 3-4 個關鍵字即可,不寫完整句子
4. 資料規模——一組對照數字(50 檔/2 年 vs. 2,255 檔/14 年),用大字體數字 + 小字說明,不用表格
5. **一張代表性圖表**(建議 `figures/Figure04_RollingIC.png`)——占版面約 1/3,是全頁視覺重心
6. 主要發現 + 未複現結果——各 2-3 句
7. 我的貢獻 + 技術能力——併成一小段,不要分成兩個獨立區塊佔用過多版面
8. 頁尾:GitHub 連結 + 一句 reproducibility 說明

**每頁主標題:** 「RP-001:外資買賣超能預測台股報酬嗎?」

**每頁只保留哪些數字:** 2,255 檔股票、14 年、H-C1~H-C5 判定(5 個標籤即可,不放完整統計量)、1 個最具代表性的百分比(如「效果縮小 47 倍」)。

**哪些資訊可放註腳:** 完整 t 值、p 值、q 值;coverage gate 的確切門檻與通過率;資料來源細節。

**哪些資訊不能省略:** 「未複現」三個字必須清楚可見,不能只暗示;研究誠信聲明(哪怕只有一句話)。

## 3-5 頁研究版面

**建議每頁配置:**

- **第 1 頁:** 研究問題、動機、兩階段設計說明(含流程圖 `figures/Figure11_ResearchLifecycleTimeline.png` 或簡化版)
- **第 2 頁:** 資料規模與資料工程(含 `figures/Figure10_DataQualitySummary.png`)、統計方法
- **第 3 頁:** H-C1~H-C5 結果表格(含 `figures/Figure07_HypothesisVerdicts.png`)、探索與確認對比(含 `figures/Figure08_ExploratoryVsConfirmatory.png`)
- **第 4 頁:** 意外發現(含 `figures/Figure09_InteractionResidualization.png`)、研究限制、研究誠信
- **第 5 頁(選用):** 結論、未來研究、reproducibility

## 建議圖片順序

1. `figures/Figure04_RollingIC.png`——開場最具說服力的單一視覺證據
2. `figures/Figure07_HypothesisVerdicts.png`——結果總覽,適合放在摘要附近
3. `figures/Figure08_ExploratoryVsConfirmatory.png` 或 `figures/Figure05_BreakBeforeAfter.png`——量級對比
4. `figures/Figure06_LiquidityGroups.png`——若篇幅足夠,補充 H-C3 細節
5. `figures/Figure09_InteractionResidualization.png`——若要呈現意外發現才需要
6. `figures/Figure10_DataQualitySummary.png`——技術導向版本(台科/北科)優先使用
7. `figures/Figure01_UniverseCoverage.png`、`figures/Figure02_MissingnessDistribution.png`、`figures/Figure03_InstitutionalCategoryHistory.png`——僅在完整版報告或資料工程重點版本使用,一頁版與 3-5 頁版通常不需要

## 教授閱讀動線

假設教授只花 90 秒:標題 → 一張圖(`figures/Figure04_RollingIC.png`)→ H-C1~H-C5 判定 → 「未複現」與「研究誠信」關鍵句。**版面設計必須確保這四個元素在 90 秒掃視內都能看到,不能被埋在文字段落中間。**

## 避免文字過密的方法

- 每個區塊標題後,第一行必須是最重要的一句話,不要用「首先」「其次」這類鋪陳開場
- 統計數字用大字體單獨呈現,不要塞進完整句子裡(例如寫「**t = 0.735**」獨立一行,而非「Newey-West t 統計量為 0.735」寫在段落中)
- 每頁文字區塊與圖表區塊面積比例建議接近 1:1,避免整頁純文字
- 善用色塊區分「未複現」(紅)/「部分複現」(橘)/「複現」(綠)——`figures/Figure07_HypothesisVerdicts.png` 的配色可直接沿用到版面其他文字標籤上,建立視覺一致性
