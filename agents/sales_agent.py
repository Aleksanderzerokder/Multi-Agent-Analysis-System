# Файл: agents/sales_agent.py
from typing import Dict, Any
from agents.base import BaseAgent
# --- НОВОЕ: Импортируем наш эмулятор API ---
from utils.marketplace_api import get_sales_data_from_marketplace

class SalesAgent(BaseAgent):

    # --- НОВОЕ: Теперь агент требует API-ключ для своей работы ---
    def __init__(self, api_key: str):
        self.api_key = api_key
        if not self.api_key:
            print("    ПРЕДУПРЕЖДЕНИЕ от SalesAgent: API ключ не предоставлен.")

    def analyze(self, sku: str, period_days: int) -> Dict[str, Any]:
        """
        Теперь этот метод не генерирует случайные данные,
        а обращается к модулю API для их получения.
        """
        print(f"-> Агент [Продажи] запрашивает данные через API для SKU {sku}...")

        # Если ключа нет, возвращаем ошибку
        if not self.api_key:
            return {"error": "API key is missing for SalesAgent"}

        # Вызываем нашу новую функцию
        sales_data = get_sales_data_from_marketplace(
            api_key=self.api_key,
            sku=sku,
            period_days=period_days
        )
        return sales_data