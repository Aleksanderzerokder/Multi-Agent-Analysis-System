# Файл: agents/sales_agent.py
from typing import Dict, Any
from agents.base import BaseAgent
from utils.marketplace_api import get_wb_sales_report

class SalesAgent(BaseAgent):
    def __init__(self, api_key: str):
        self.api_key = api_key

    def analyze(self, sku: str, period_days: int) -> Dict[str, Any]:
        print(f"-> Агент [Продажи] запрашивает РЕАЛЬНЫЕ данные для SKU {sku}...")
        if not self.api_key:
            return {"error": "API key is missing for SalesAgent"}
        
        response_data = get_wb_sales_report(
            api_key=self.api_key,
            period_days=period_days
        )
        
        if "error" in response_data:
            return response_data
        
        # --- НАЧАЛО БЛОКА ОТЛАДКИ ---
        all_sales_records = response_data.get('data', [])
        print(f"    [DEBUG] От API получено всего записей о продажах: {len(all_sales_records)}")

        if all_sales_records:
            first_item = all_sales_records[0]
            print(f"    [DEBUG] Пример первой записи от API: {first_item}")
            print(f"    [DEBUG] 'supplierArticle' из ответа: '{first_item.get('supplierArticle')}'")
            print(f"    [DEBUG] SKU, который мы ищем: '{sku}'")
        # --- КОНЕЦ БЛОКА ОТЛАДКИ ---

        total_sales = 0
        items_sold = 0
        for item in all_sales_records:
            # Наша строка-фильтр. Здесь может быть ошибка.
            if item.get('supplierArticle') == sku and item.get('saleID', '').startswith('S'):
                total_sales += item.get('forPay', 0)
                items_sold += 1
        
        print(f"    [SalesAgent] По SKU '{sku}' найдено {items_sold} продаж на сумму {total_sales:.2f} руб.")
        return {
            "total_sales_rub": round(total_sales, 2),
            "units_sold": items_sold,
            "data_source": "real_wb_api"
        }