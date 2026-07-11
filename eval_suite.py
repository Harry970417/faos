import re
from collections import defaultdict

path = r"C:\Users\user\Desktop\faos\knowledge_base_remediated_v0.1.psv"
lines = [l.rstrip("\n") for l in open(path, encoding="utf-8") if l.strip()]
rows = [l.split("|") for l in lines[1:]]
nodes = {r[0]: {"name": r[1], "type": r[2], "root": r[3]} for r in rows}
EDGE_COLS = {"DependsOn":6,"References":7,"Implements":8,"DerivedFrom":9}
def parse(cell):
    out=[]
    for tok in cell.split(";"):
        tok=tok.strip()
        if not tok: continue
        m=re.match(r"([A-Za-z0-9]+)", tok)
        out.append(m.group(0))
    return out
und = defaultdict(set)
for r in rows:
    s=r[0]
    for et,idx in EDGE_COLS.items():
        for t in parse(r[idx] if idx<len(r) else ""):
            if t in nodes:
                und[s].add(t); und[t].add(s)

def bfs(anchors, depth=2):
    visited=set(anchors)
    frontier=set(anchors)
    path=[list(anchors)]
    for _ in range(depth):
        nxt=set()
        for u in frontier:
            for v in und[u]:
                if v not in visited:
                    nxt.add(v); visited.add(v)
        if not nxt: break
        path.append(sorted(nxt))
        frontier=nxt
    return visited, path

QUESTIONS = [
("Q001","What is the Sharpe Ratio and how is it calculated?","Quantitative Methods",["ME01"]),
("Q002","How is the Information Coefficient used to evaluate a factor's predictive power?","Quantitative Methods",["ME07"]),
("Q003","What is the momentum factor and how is it typically constructed?","Quantitative Methods",["FA03","PR03"]),
("Q004","Does momentum work in the Taiwan small-cap market?","Quantitative Methods",["FA04","PA01"]),
("Q005","What is the January effect and is it still considered a robust anomaly?","Quantitative Methods",["PA02"]),
("Q006","How does GARCH model volatility clustering?","Quantitative Methods",["M17","C47"]),
("Q007","What is look-ahead bias and how does it affect backtesting?","Quantitative Methods",["C50","PR10"]),
("Q008","What is survivorship bias in factor research?","Quantitative Methods",["C51"]),
("Q009","What is the Fama-MacBeth two-pass regression procedure?","Quantitative Methods",["M16"]),
("Q010","How do you avoid overfitting in a quantitative strategy?","Quantitative Methods",["C49"]),
("Q011","What is autocorrelation and why does it matter for time series models?","Quantitative Methods",["C46"]),
("Q012","Is the Efficient Market Hypothesis still valid given behavioral anomalies?","Quantitative Methods",["T02","T10"]),
("Q013","What is the Random Walk Theory and how does it relate to EMH?","Quantitative Methods",["T24","T02"]),
("Q014","What is stationarity and why is it important in econometric modeling?","Quantitative Methods",["C48"]),
("Q015","How is the value factor constructed and evaluated?","Quantitative Methods",["FA01","ME07"]),
("Q016","What determines a bond's Macaulay Duration?","Fixed Income",["ME08","F15"]),
("Q017","How does Modified Duration differ from Macaulay Duration?","Fixed Income",["ME09","F16"]),
("Q018","What is bond convexity and why does it matter for large rate changes?","Fixed Income",["ME10","F17"]),
("Q019","What does Pure Expectations Theory say about the yield curve shape?","Fixed Income",["T06"]),
("Q020","How does Liquidity Preference Theory explain the term premium?","Fixed Income",["T07","C56"]),
("Q021","What is Market Segmentation Theory and how does it differ from Pure Expectations?","Fixed Income",["T08"]),
("Q022","How does the Vasicek model simulate interest rates?","Fixed Income",["M05","F06"]),
("Q023","Why was the Cox-Ingersoll-Ross model developed instead of just using Vasicek?","Fixed Income",["M06","M05"]),
("Q024","What is the Merton structural credit model and how does it estimate default probability?","Fixed Income",["M09","C12"]),
("Q025","How do you bootstrap a yield curve from market data?","Fixed Income",["PR07","F19"]),
("Q026","What is duration-matching immunization?","Fixed Income",["PR08","PR21"]),
("Q027","How does the Nelson-Siegel model fit the yield curve?","Fixed Income",["M07","F07"]),
("Q028","What determines credit spread widening during recessions?","Fixed Income",["PA05","C31"]),
("Q029","What is sovereign risk and how does it differ from corporate credit risk?","Fixed Income",["C58","C12"]),
("Q030","What does CAPM say about the relationship between risk and expected return?","Portfolio Management",["T01","F01"]),
("Q031","What are the key assumptions underlying CAPM?","Portfolio Management",["T01","A01","A02"]),
("Q032","How does Modern Portfolio Theory justify diversification?","Portfolio Management",["T03","C05"]),
("Q033","What is the Fama-French three-factor model and how does it extend CAPM?","Portfolio Management",["M01","T01"]),
("Q034","How does the Fama-French five-factor model extend the three-factor model?","Portfolio Management",["M04","M01"]),
("Q035","How does the Carhart four-factor model add momentum to Fama-French?","Portfolio Management",["M10"]),
("Q036","What is the Treynor Ratio and how does it differ from Sharpe Ratio?","Portfolio Management",["ME02","ME01"]),
("Q037","What is Value at Risk and how is it calculated?","Portfolio Management",["ME17","F14"]),
("Q038","What is Conditional VaR and why is it considered superior to VaR for tail risk?","Portfolio Management",["ME18","C65"]),
("Q039","What is the Black-Litterman model used for in portfolio optimization?","Portfolio Management",["F29","PR32"]),
("Q040","How does the Kelly Criterion determine optimal position sizing?","Portfolio Management",["F30","PR33"]),
("Q041","What is Risk Parity and how does it differ from traditional allocation?","Portfolio Management",["FR13"]),
("Q042","What is Jensen's Alpha and how is it interpreted?","Portfolio Management",["ME20"]),
("Q043","How does the Black-Scholes model price a European option?","Derivatives",["M02","F03"]),
("Q044","What assumptions does Black-Scholes rely on?","Derivatives",["M02","A01","A03","A05","A06"]),
("Q045","How does the Binomial Option Pricing Model differ from Black-Scholes?","Derivatives",["M08","M02"]),
("Q046","What is Put-Call Parity and why must it hold in an efficient market?","Derivatives",["T09"]),
("Q047","What does Delta measure and how is it used in hedging?","Derivatives",["ME13","PR09"]),
("Q048","What is Gamma and why does it matter for dynamic hedging?","Derivatives",["ME14"]),
("Q049","What is implied volatility and how does it differ from historical volatility?","Derivatives",["ME16","C04"]),
("Q050","How is a Credit Default Swap priced?","Derivatives",["PR20","M09"]),
("Q051","What is counterparty risk in OTC derivatives and how is it mitigated?","Derivatives",["C26","S11"]),
("Q052","What is the difference between contango and backwardation in futures markets?","Derivatives",["C59","C60"]),
("Q053","What is basis risk in a hedging strategy?","Derivatives",["C27"]),
("Q054","How is Return on Equity decomposed in DuPont analysis?","Financial Statement Analysis",["FR01","ME04"]),
("Q055","What is the difference between ROE and ROA?","Financial Statement Analysis",["ME04","ME05"]),
("Q056","What is the Altman Z-Score and what does it predict?","Financial Statement Analysis",["FR08","ME28"]),
("Q057","What is the Debt-to-Equity Ratio and what does it indicate about leverage?","Financial Statement Analysis",["ME28","C07"]),
("Q058","How do IFRS and US GAAP differ in revenue recognition?","Financial Statement Analysis",["S01","S02"]),
("Q059","What is the going concern assumption in financial statement auditing?","Financial Statement Analysis",["C53"]),
("Q060","What is materiality in financial reporting?","Financial Statement Analysis",["C54"]),
("Q061","What is an off-balance-sheet item and why is it a red flag?","Financial Statement Analysis",["C55"]),
("Q062","What internal controls does Sarbanes-Oxley require for financial reporting?","Financial Statement Analysis",["S12"]),
("Q063","What does the Phillips Curve say about the inflation-unemployment tradeoff?","Economics",["T21"]),
("Q064","What is the Fisher Effect and how does it relate real and nominal interest rates?","Economics",["T22","F27"]),
("Q065","What does the Taylor Rule prescribe for setting the policy interest rate?","Economics",["M21","F26"]),
("Q066","How does the IS-LM model explain the interaction between goods and money markets?","Economics",["M22"]),
("Q067","What is Purchasing Power Parity and does it hold in practice?","Economics",["T23"]),
("Q068","What is Uncovered Interest Rate Parity?","Economics",["T25"]),
("Q069","What does Rational Expectations Theory assume about how agents form expectations?","Economics",["T11"]),
("Q070","What is the Quantity Theory of Money?","Economics",["T12"]),
("Q071","How is intrinsic value estimated using the Dividend Discount Model?","Equity Investments",["M12","C08"]),
("Q072","What is the Gordon Growth Model and when is it appropriate to use?","Equity Investments",["M03"]),
("Q073","How does the Residual Income Model value equity differently from DDM?","Equity Investments",["M13"]),
("Q074","How is Free Cash Flow to Equity used in valuation?","Equity Investments",["M14","C40"]),
("Q075","What is EV/EBITDA and why is it used in comparable company analysis?","Equity Investments",["ME35","PR05"]),
("Q076","What is the PEG ratio and how does it adjust P/E for growth?","Equity Investments",["ME38"]),
("Q077","What is Post-Earnings Announcement Drift and why does it persist?","Equity Investments",["PA06"]),
("Q078","What is an economic moat and why does it matter for long-term valuation?","Equity Investments",["C42"]),
("Q079","How does a private equity waterfall distribute returns between GP and LP?","Alternative Investments",["PR17","C21"]),
("Q080","What is vintage year and why does it matter for PE fund comparison?","Alternative Investments",["C20"]),
("Q081","What is the difference between IRR and MOIC in evaluating PE performance?","Alternative Investments",["ME22","ME23"]),
("Q082","How is real estate valued using the income approach?","Alternative Investments",["PR18","ME25"]),
("Q083","What is the Endowment Model of asset allocation?","Alternative Investments",["FR11"]),
("Q084","How is ESG integrated into investment screening?","Alternative Investments",["PR30","ME47"]),
("Q085","What is the illiquidity premium and how is it captured?","Alternative Investments",["C19"]),
("Q086","What does Modigliani-Miller say about capital structure irrelevance?","Corporate Issuers",["T05","C07"]),
("Q087","What is the Trade-Off Theory of capital structure?","Corporate Issuers",["T14","C38"]),
("Q088","What is Pecking Order Theory and how does it differ from Trade-Off Theory?","Corporate Issuers",["T13"]),
("Q089","What is Agency Theory and how does it explain the agency problem?","Corporate Issuers",["T15","C41"]),
("Q090","What is Signaling Theory in the context of dividend policy?","Corporate Issuers",["T16","C43"]),
("Q091","How is a leveraged buyout modeled?","Corporate Issuers",["PR23","F05"]),
("Q092","What is Working Capital Management and why does it matter for liquidity?","Corporate Issuers",["PR34","C37"]),
("Q093","What is fiduciary duty and how does it apply to investment managers?","Ethical and Professional Standards",["C34"]),
("Q094","What constitutes a conflict of interest under the CFA Code of Ethics?","Ethical and Professional Standards",["PR29","C35"]),
("Q095","How should an analyst handle material nonpublic information?","Ethical and Professional Standards",["PR28","C36"]),
("Q096","What is GIPS and why do asset managers voluntarily comply?","Ethical and Professional Standards",["S06","PR15"]),
("Q097","What does MiFID II require for best execution?","Ethical and Professional Standards",["S08","PR16"]),
("Q098","What does FATCA require and how does AML screening relate?","Ethical and Professional Standards",["S16","PR35"]),
("Q099","What are the Three Lines of Defense in risk governance?","Ethical and Professional Standards",["FR14"]),
("Q100","What must an investment manager disclose to comply with SEC Regulation FD?","Ethical and Professional Standards",["S07"]),
]

assert len(QUESTIONS) == 100
for qid,qtext,root,anchors in QUESTIONS:
    for a in anchors:
        assert a in nodes, f"{qid}: bad anchor {a}"

results = []
for qid,qtext,root,anchors in QUESTIONS:
    visited, path = bfs(anchors, depth=2)
    types_touched = set(nodes[n]["type"] for n in visited)
    anchor_degrees = [len(und[a]) for a in anchors]
    results.append({
        "qid": qid, "question": qtext, "root": root, "anchors": anchors,
        "touched": sorted(visited), "n_touched": len(visited),
        "types_touched": sorted(types_touched), "n_types": len(types_touched),
        "min_anchor_degree": min(anchor_degrees), "path_depth": len(path)
    })

for r in results:
    cs = "Y" if (r["n_touched"]>=3 and r["n_types"]>=2 and r["min_anchor_degree"]>=1) else "N"
    print(f"{r['qid']}|{r['root']}|{','.join(r['anchors'])}|{r['n_touched']}|{r['n_types']}|{r['min_anchor_degree']}|{cs}|{','.join(r['types_touched'])}")

from collections import Counter
cs_counts = Counter()
root_cs = defaultdict(lambda: [0,0])
for r in results:
    cs = "Y" if (r["n_touched"]>=3 and r["n_types"]>=2 and r["min_anchor_degree"]>=1) else "N"
    cs_counts[cs]+=1
    root_cs[r["root"]][0]+=1
    if cs=="Y": root_cs[r["root"]][1]+=1

print("\n=== SUMMARY ===")
print("Conceptually Sufficient:", dict(cs_counts))
print("\nBy root (sufficient/total):")
for root,(tot,suf) in sorted(root_cs.items()):
    print(f"  {root:40s} {suf}/{tot}")

isolated_anchor_qs = [r["qid"] for r in results if r["min_anchor_degree"]==0]
print("\nQuestions with a fully isolated anchor:", isolated_anchor_qs)
