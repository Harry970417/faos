# RP-001 Evidence Map

All sources below were located via real WebSearch this session, not recalled from memory — consistent with ECC v1.0's verification standard. Where I could confirm volume/issue/pages/DOI, they're recorded; where I couldn't, marked Locator Pending, not guessed.

## Institutional trading behavior (Taiwan-specific)

| Citation | Tier | Verified detail | Relevance |
|---|---|---|---|
| Lin, C.M., Lee, Y.H., Chiu, C.L. (2009). Structural changes in foreign investors' trading behavior and the corresponding impact on Taiwan's stock market. *Research in International Business and Finance*, 23(1), 78-89. | Primary | Author names, journal, vol/issue/pages fully confirmed via RePEc | Direct Taiwan-market precedent for foreign investor trading impact |
| Lien, D., Hung, P.H., Lin, Z.W. (2020). Whose trades move stock prices? Evidence from the Taiwan Stock Exchange. *International Review of Economics & Finance*, 66, 25-50. DOI: 10.1016/j.iref.2019.10.011 | Primary | Fully confirmed including DOI | Establishes baseline: individual traders, not institutions, dominate Taiwan price-weighted contribution — important context-setting finding for H2/H3 |
| Lien, D., Hung, P.H. (2023). Whose trades contribute more to price discovery? Evidence from the Taiwan stock exchange. *Review of Quantitative Finance and Accounting*, 61, 213-263. | Primary | Author names, journal, pages confirmed | Reports mutual funds have highest per-order price contribution despite smallest volume share — directly relevant to H2 (institutional heterogeneity) |
| "Capital flows from foreign institutional investors have significant predictive power with regard to next-day TAIEX spot index returns, whereas flows from other types of investors appear to have no significant predictive power" | Secondary (search-summary level, source paper not yet individually confirmed) | **Locator Pending** — this specific finding needs its own source paper identified and verified before being cited directly, currently only known via search-engine synthesis | Directly bears on H2; must not be cited without isolating and verifying its actual source paper first |

## Order imbalance / price-pressure mechanism (general, not Taiwan-specific)

| Citation | Tier | Verified detail | Relevance |
|---|---|---|---|
| Chordia, T., Subrahmanyam, A. (2004). Order Imbalance and Individual Stock Returns: Theory and Evidence. *Journal of Financial Economics*, 72, 485-518. | Primary | Author names, journal, volume, pages confirmed | Foundational for H1b — establishes the price-pressure-then-reversal mechanism that H1a (informed-trading continuation) directly competes against |

## Cross-sectional testing methodology (already Frozen KB objects, newly evidenced)

| Citation | Tier | Verified detail | Grounds |
|---|---|---|---|
| Fama, E.F., MacBeth, J.D. (1973). Risk, Return, and Equilibrium: Empirical Tests. *The Journal of Political Economy*, 81(3), 607-636. | Primary | Fully confirmed | **M16, F12** (already-existing KB objects) — newly attached this session as EV35, closing an ECC gap that existed before this research began |
| Newey, W.K., West, K.D. (1987). A Simple, Positive Semi-Definite, Heteroskedasticity and Autocorrelation Consistent Covariance Matrix. *Econometrica*, 55(3), 703-708. | Primary | Fully confirmed | **No KB object exists to ground this on** — see Research Production Finding #2 in RP001_FAOS_TRACE.md |

## Official data source

| Source | Type | Verified detail |
|---|---|---|
| FinMind, `TaiwanStockInstitutionalInvestorsBuySell` dataset | Dataset | Confirmed real, open-source, GitHub-hosted (github.com/FinMind/FinMind), documented API endpoint, covers both TWSE and TPEx. **Confirmed limitation: reports shares, not NT$ value** (verified independently against taiwan-attention-signal's own code-level documentation of the same limitation — two independent confirmations of the same constraint) |

## Evidence not yet attached to any Knowledge Object

The four Taiwan-institutional-trading and order-imbalance papers above cannot be formally `grounded-by`-linked yet — **no Institutional Flow Factor or Order Imbalance Concept exists anywhere in the Knowledge Base.** This is the single most important finding in this Evidence Map, not a footnote — see RP001_FAOS_TRACE.md, Research Production Finding #1. These citations are pre-positioned, ready to attach the moment such an object is created during execution, not before.

## ECC status summary

- **M16, F12** (Fama-MacBeth): now ECC-eligible for re-check — Primary source is peer-reviewed (satisfies the v1.0 Theory/Model peer-review clause), independent of prior KB sources. Not formally re-run against full ECC criteria here — that's execution-phase work, flagged for the Execution Plan.
- **Newey-West correction, Institutional Flow factors:** cannot be ECC-checked — there is nothing to check, since no object exists. This is an architecture/content gap, not an ECC failure.
