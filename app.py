# app.py
from flask import Flask, jsonify
from flask_cors import CORS
import asyncio
import uuid
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any

app = Flask(__name__)
CORS(app)

# --------------------------------------------------
# 通用工具
# --------------------------------------------------
def _gid() -> str:
    """生成匿名 UUID，用作 id 占位"""
    return str(uuid.uuid4())

async def _mock_delay():
    """模拟网络延迟 1.5 s"""
    await asyncio.sleep(1.5)

# --------------------------------------------------
# 1. 合规 / 披露
# --------------------------------------------------
@dataclass
class Compliance:
    k10: str
    sriPolicy: str
    costsAndCharges: Dict[str, float]
    taxWrapper: Dict[str, Any]
    regulatoryFlags: List[str]

    def to_dict(self):
        return asdict(self)

# --------------------------------------------------
# 2. 费用
# --------------------------------------------------
@dataclass
class AnnualCharges:
    ocf: float
    transactionCosts: float
    incidentalCosts: float

    def to_dict(self):
        return asdict(self)

# --------------------------------------------------
# 3. ESG
# --------------------------------------------------
@dataclass
class ESG:
    msciESGRating: str
    carbonIntensity: float  # tCO2e/£M invested

    def to_dict(self):
        return asdict(self)

# --------------------------------------------------
# 4. Morningstar
# --------------------------------------------------
@dataclass
class Morningstar:
    starRating: int
    category: str
    legalStructure: str

    def to_dict(self):
        return asdict(self)

# --------------------------------------------------
# 5. 基金级别
# --------------------------------------------------
@dataclass
class Fund:
    fundId: str
    fundName: str
    sedol: str
    isin: str
    units: float
    nav: float
    marketValue: float
    costBasis: float
    gainLoss: float
    gainLossPct: float
    annualCharges: AnnualCharges
    esg: ESG
    morningstar: Morningstar

    def to_dict(self):
        return {
            "fundId": self.fundId,
            "fundName": self.fundName,
            "sedol": self.sedol,
            "isin": self.isin,
            "units": self.units,
            "nav": self.nav,
            "marketValue": self.marketValue,
            "costBasis": self.costBasis,
            "gainLoss": self.gainLoss,
            "gainLossPct": self.gainLossPct,
            "annualCharges": self.annualCharges.to_dict(),
            "esg": self.esg.to_dict(),
            "morningstar": self.morningstar.to_dict(),
        }

# --------------------------------------------------
# 6. 资产配置节点
# --------------------------------------------------
@dataclass
class AssetNode:
    bucket: str
    targetPct: float
    currentPct: float
    marketValue: float
    children: List[Any] = field(default_factory=list)  # 支持嵌套
    funds: List[Fund] = field(default_factory=list)

    def to_dict(self):
        return {
            "bucket": self.bucket,
            "targetPct": self.targetPct,
            "currentPct": self.currentPct,
            "marketValue": self.marketValue,
            "children": [c.to_dict() for c in self.children],
            "funds": [f.to_dict() for f in self.funds],
        }

# --------------------------------------------------
# 7. 现金
# --------------------------------------------------
@dataclass
class Cash:
    targetPct: float
    currentPct: float
    marketValue: float
    sweepVehicle: str

    def to_dict(self):
        return asdict(self)

# --------------------------------------------------
# 8. 偏离
# --------------------------------------------------
@dataclass
class Drift:
    bucket: str
    driftPct: float
    threshold: float
    action: str

    def to_dict(self):
        return asdict(self)

# --------------------------------------------------
# 9. 表现
# --------------------------------------------------
@dataclass
class Performance:
    periods: List[str]
    benchmark: str
    moneyWeighted: Dict[str, float]
    timeWeighted: Dict[str, float]
    benchmarkReturns: Dict[str, float]
    volatility: float
    sharpeRatio: float
    maxDrawdown: Dict[str, Any]
    performanceAttribution: Dict[str, float]

    def to_dict(self):
        return asdict(self)

# --------------------------------------------------
# 10. 前瞻
# --------------------------------------------------
@dataclass
class Projections:
    projectionModel: str
    projectionDate: str
    maturityDate: str
    targetAmount: float
    percentiles: Dict[str, float]
    stressScenarios: List[Dict[str, Any]]
    cashFlow: List[Dict[str, Any]]

    def to_dict(self):
        return asdict(self)

# --------------------------------------------------
# 11. What-If
# --------------------------------------------------
@dataclass
class WhatIfScenario:
    scenarioId: str
    description: str
    newAllocation: Dict[str, Any]
    projectedReturn: float
    projectedVolatility: float
    carbonReduction: float

    def to_dict(self):
        return asdict(self)

@dataclass
class WhatIf:
    scenarios: List[WhatIfScenario]

    def to_dict(self):
        return {"scenarios": [s.to_dict() for s in self.scenarios]}

# --------------------------------------------------
# 12. UI Hints
# --------------------------------------------------
@dataclass
class UIHints:
    colorPalette: Dict[str, str]
    drillDown: Dict[str, int]
    chartOrder: List[str]
    featureFlags: Dict[str, bool]

    def to_dict(self):
        return asdict(self)

# --------------------------------------------------
# 13. 根对象
# --------------------------------------------------
@dataclass
class PlanViewerV2:
    planId: str
    planName: str
    clientId: str
    currency: str
    asOfDate: str
    locale: str
    disclaimerVersion: str
    planSnapshot: Dict[str, Any]
    performance: Performance
    projections: Projections
    whatIf: WhatIf
    compliance: Compliance
    uiHints: UIHints

    def to_dict(self):
        return {
            "planId": self.planId,
            "planName": self.planName,
            "clientId": self.clientId,
            "currency": self.currency,
            "asOfDate": self.asOfDate,
            "locale": self.locale,
            "disclaimerVersion": self.disclaimerVersion,
            "planSnapshot": self.planSnapshot,
            "performance": self.performance.to_dict(),
            "projections": self.projections.to_dict(),
            "whatIf": self.whatIf.to_dict(),
            "compliance": self.compliance.to_dict(),
            "uiHints": self.uiHints.to_dict(),
        }

# --------------------------------------------------
# 构造假数据工厂
# --------------------------------------------------
async def build_plan_viewer_v2() -> PlanViewerV2:
    await _mock_delay()

    # 1. 基金层
    f1 = Fund(
        fundId="FID-NA-EQ-001",
        fundName="Fidelity American Fund A-Acc",
        sedol="B827XX6",
        isin="GB00B827XX66",
        units=1234.56,
        nav=15.75,
        marketValue=19443.00,
        costBasis=18000.00,
        gainLoss=1443.00,
        gainLossPct=8.02,
        annualCharges=AnnualCharges(ocf=0.85, transactionCosts=0.06, incidentalCosts=0.01),
        esg=ESG(msciESGRating="A", carbonIntensity=98.2),
        morningstar=Morningstar(starRating=4, category="US Large-Cap Blend", legalStructure="OEIC"),
    )

    # 2. 资产节点
    equity_children = AssetNode(
        bucket="North America",
        targetPct=35.0,
        currentPct=33.1,
        marketValue=82750.0,
        funds=[f1],
    )

    equity = AssetNode(
        bucket="Equity",
        targetPct=60.0,
        currentPct=58.3,
        marketValue=145750.0,
        children=[equity_children],
    )

    bond = AssetNode(
        bucket="Bond",
        targetPct=35.0,
        currentPct=37.5,
        marketValue=93750.0,
        children=[],
        funds=[],
    )

    cash = Cash(targetPct=5.0, currentPct=4.2, marketValue=10500.0, sweepVehicle="Fidelity Cash Fund")

    drift = [Drift(bucket="Equity", driftPct=-1.7, threshold=2.0, action="Rebalance recommended")]

    plan_snapshot = {
        "totalMarketValue": 250000.00,
        "totalCostBasis": 230000.00,
        "totalGainLoss": 20000.00,
        "totalGainLossPct": 8.70,
        "targetRiskScore": 6,
        "currentRiskScore": 5.8,
        "assetAllocation": [equity.to_dict(), bond.to_dict()],
        "cash": cash.to_dict(),
        "drift": [d.to_dict() for d in drift],
    }

    # 3. 表现
    performance = Performance(
        periods=["1M", "3M", "YTD", "1Y", "3Y", "5Y", "SinceInception"],
        benchmark="FTSE WMA Balanced",
        moneyWeighted={"1Y": 7.2, "3Y": 5.4, "5Y": 6.1},
        timeWeighted={"1Y": 7.0, "3Y": 5.3, "5Y": 6.0},
        benchmarkReturns={"1Y": 6.5, "3Y": 5.0, "5Y": 5.8},
        volatility=9.8,
        sharpeRatio=0.62,
        maxDrawdown={"value": -11.3, "period": "2020-02-20 to 2020-03-23"},
        performanceAttribution={"assetAllocationEffect": 0.4, "selectionEffect": 0.8, "interactionEffect": -0.1},
    )

    # 4. 前瞻
    projections = Projections(
        projectionModel="Stochastic Monte-Carlo 2.1",
        projectionDate="2025-12-07",
        maturityDate="2030-12-31",
        targetAmount=300000,
        percentiles={"P10": 260000, "P50": 310000, "P90": 370000},
        stressScenarios=[{"name": "2008 Replay", "valueAtEnd": 215000}],
        cashFlow=[
            {
                "date": "2026-12-07",
                "contribution": 10000,
                "withdrawal": 0,
                "projectedValue": 271000,
            }
        ],
    )

    # 5. What-If
    what_if = WhatIf(
        scenarios=[
            WhatIfScenario(
                scenarioId="ESG-Tilt-10",
                description="Shift 10% equity to ESG leaders",
                newAllocation={"Equity": 50, "Bond": 40, "Cash": 10},
                projectedReturn=6.3,
                projectedVolatility=9.9,
                carbonReduction=15.2,
            )
        ]
    )

    # 6. 合规
    compliance = Compliance(
        k10="https://fidelity.co.uk/kid/832746",
        sriPolicy="https://fidelity.co.uk/sri",
        costsAndCharges={"oneOffCosts": 0, "ongoingCosts": 0.65, "incidentalCosts": 0.02, "totalCostRatio": 0.67},
        taxWrapper={"type": "ISA", "allowanceUsed": 20000, "allowanceRemaining": 0},
        regulatoryFlags=["PRIIPs", "MiFID II", "UK SMCR"],
    )

    # 7. UI Hints
    ui_hints = UIHints(
        colorPalette={"Equity": "#0051CC", "Bond": "#6BC4FF", "Cash": "#FF9E3D"},
        drillDown={"maxDepth": 4, "defaultDepth": 2},
        chartOrder=["pie", "treeMap", "driftBar"],
        featureFlags={"enableComparison": True, "enableESGFilter": True, "enableWhatIf": True},
    )

    return PlanViewerV2(
        planId=_gid(),
        planName="Moderate Growth 2030",
        clientId=_gid(),
        currency="GBP",
        asOfDate="2025-12-07",
        locale="en-GB",
        disclaimerVersion="v2025.1",
        planSnapshot=plan_snapshot,
        performance=performance,
        projections=projections,
        whatIf=what_if,
        compliance=compliance,
        uiHints=ui_hints,
    )

# --------------------------------------------------
# 路由：V2 全景数据
# --------------------------------------------------
@app.route("/api/plan/v2", methods=["GET"])
def get_plan_v2():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    plan = loop.run_until_complete(build_plan_viewer_v2())
    return jsonify(plan.to_dict())

# --------------------------------------------------
# 保留旧路由，向下兼容
# --------------------------------------------------
from typing import Dict, List, Any   # 已包含在上部

class AccountData:
    def __init__(self, totalBalance: float, vestedBalance: float, ytdChange: float,
                 rateOfReturn: float, lastContributionAmount: float,
                 nextContributionDate: str, contributionRate: int):
        self.totalBalance = totalBalance
        self.vestedBalance = vestedBalance
        self.ytdChange = ytdChange
        self.rateOfReturn = rateOfReturn
        self.lastContributionAmount = lastContributionAmount
        self.nextContributionDate = nextContributionDate
        self.contributionRate = contributionRate

    def to_dict(self) -> Dict[str, Any]:
        return {
            "totalBalance": self.totalBalance,
            "vestedBalance": self.vestedBalance,
            "ytdChange": self.ytdChange,
            "rateOfReturn": self.rateOfReturn,
            "lastContributionAmount": self.lastContributionAmount,
            "nextContributionDate": self.nextContributionDate,
            "contributionRate": self.contributionRate
        }

class Transaction:
    def __init__(self, id: str, date: str, description: str, amount: float, type: str):
        self.id = id
        self.date = date
        self.description = description
        self.amount = amount
        self.type = type

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "date": self.date,
            "description": self.description,
            "amount": self.amount,
            "type": self.type
        }

class Investment:
    def __init__(self, name: str, ticker: str, balance: float, allocationPercentage: int):
        self.name = name
        self.ticker = ticker
        self.balance = balance
        self.allocationPercentage = allocationPercentage

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "ticker": self.ticker,
            "balance": self.balance,
            "allocationPercentage": self.allocationPercentage
        }

async def fetch_plan_data() -> Dict[str, Any]:
    # 模拟服务器延迟（1.5秒）
    await asyncio.sleep(1.5)

    account_data = AccountData(
        totalBalance=142567.89,
        vestedBalance=139850.45,
        ytdChange=12450.50,
        rateOfReturn=12.4,
        lastContributionAmount=850.00,
        nextContributionDate="2024-06-15",
        contributionRate=8
    )

    transactions = [
        Transaction("1", "2024-06-01", "Contribution - Pay Period 11", 850.00, "Contribution"),
        Transaction("2", "2024-06-01", "Employer Match", 425.00, "Contribution"),
        Transaction("3", "2024-05-15", "Contribution - Pay Period 10", 850.00, "Contribution"),
        Transaction("4", "2024-03-31", "Dividend Reinvestment - FDKLX", 345.20, "Dividend"),
        Transaction("5", "2024-03-31", "Plan Admin Fee", -25.00, "Fee")
    ]

    investments = [
        Investment("Target Date 2060 Fund", "FDKLX", 64155.55, 45),
        Investment("500 Index Fund", "FXAIX", 49898.76, 35),
        Investment("Bond Index Fund", "FXNAX", 28513.58, 20)
    ]

    return {
        "accountData": account_data.to_dict(),
        "transactions": [t.to_dict() for t in transactions],
        "investments": [i.to_dict() for i in investments]
    }

@app.route('/api/plan', methods=['GET'])
def get_plan_data():
    # 运行异步函数获取数据
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    data = loop.run_until_complete(fetch_plan_data())
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)