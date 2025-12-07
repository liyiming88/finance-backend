# app.py
from flask import Flask, jsonify
from flask_cors import CORS
import asyncio
from typing import Dict, List, Any

app = Flask(__name__)
CORS(app)  # 允许跨域请求

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