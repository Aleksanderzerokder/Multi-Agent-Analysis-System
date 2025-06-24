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


class QuestionRequest(BaseModel):
    request_id: str
    sku: str
    # Разрешаем спрашивать только про те аспекты, которые у нас есть
    aspect: Literal["sales", "price"]
    # Сам текст вопроса мы пока не используем, но закладываем на будущее
    question_text: str = "Расскажи подробнее об этом аспекте."