# Файл: schemas/models.py
from pydantic import BaseModel
from typing import List, Literal
from enum import Enum

class Marketplace(str, Enum):
    WILDERRIES = "wildberries"
    OZON = "ozon"
    YANDEX_MARKET = "yandex_market"

class AnalysisRequest(BaseModel):
    marketplace: Marketplace
    period_days: int
    sku_list: List[str] | Literal["all"]
