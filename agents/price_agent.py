import random
from typing import Dict, Any
from agents.base import BaseAgent

class PriceAgent(BaseAgent):
    def analyze(self, sku: str, period_days: int) -> Dict[str, Any]:
        print(f"-> Агент [Цены]    анализирует SKU {sku}...")
        return { "current_price_rub": random.randint(1000, 5000) }