from enum import Enum

restricted_cells = {'A', 'CP&A'}


class BotType(Enum):
    BOT1 = 1
    BOT2 = 2
    BOT3 = 3
    BOT4 = 4 #RiskFactor:2n, Radius: 3
    BOT5 = 5
    BOT4RiskSigmoidRiskFactor4nRadius3 = 6
    BOT4RiskSigmoidRiskFactor2nRadius4 = 7
    BOT4RiskSigmoidRiskFactor2nRadius2 = 8
    BOT4RiskSigmoidRiskFactor1nRadius3 = 9
    BOT4RiskSigmoidRiskFactor2nRadius3 = 10
    BOT4RiskTanHRiskFactor2nRadius3 = 11
