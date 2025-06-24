# Файл: decision_agent/manager.py
from typing import List, Dict, Any
from agents.sales_agent import SalesAgent
from agents.price_agent import PriceAgent

class DecisionManager:
    def __init__(self, marketplace_api_key: str):
        self.agents = [
            SalesAgent(api_key=marketplace_api_key),
            PriceAgent(),
        ]
        print("Управляющий агент создан и готов к работе.")

    # --- ВОТ ИСПРАВЛЕНИЕ: Добавлено тело функции ---
    def run_analysis(self, sku_list: List[str], period_days: int) -> Dict[str, Any]:
        print(f"\n--- Начинаю полный анализ для {len(sku_list)} SKU... ---")
        full_report = {}
        for sku in sku_list:
            print(f"\nАнализ товара SKU: {sku}")
            sku_report = {}
            for agent in self.agents:
                agent_name = agent.__class__.__name__.replace("Agent", "").lower()
                sku_report[agent_name] = agent.analyze(sku=sku, period_days=period_days)
            full_report[sku] = sku_report

        print("\n--- Полный анализ завершен. ---")
        return full_report