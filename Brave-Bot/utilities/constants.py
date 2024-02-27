from enum import Enum

restricted_cells = {'A', 'CP&A'}


class BotType(Enum):
    BOT1 = 1
    BOT2 = 2
    BOT3 = 3
    BOT4 = 4 #RiskFactor:2n, Radius: 3
    BOT5 = 5
    BOT4RiskFactor4nRadius3 = 6
    BOT4RiskFactor2nRadius4 = 7
    BOT4RiskFactor2nRadius2 = 8
    BOT4RiskFactor1nRadius3 = 9
    BOT4RiskLogRiskFactor2nRadius3 = 10
    BOT4RiskTanHRiskFactor2nRadius3 = 11
