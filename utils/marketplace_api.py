# Файл: utils/marketplace_api.py
import random

def get_sales_data_from_marketplace(api_key: str, sku: str, period_days: int) -> dict:
    """
    ЭМУЛЯТОР: Эта функция имитирует реальный запрос к API маркетплейса.
    Она "делает вид", что использует API-ключ для получения данных.
    """
    print(f"    [API] Имитация запроса к API маркетплейса для SKU {sku}...")

    # Проверяем "валидность" ключа для эмуляции
    if not api_key or "sk-" not in api_key:
        return {"error": "Invalid or missing API key"}

    # Возвращаем такие же данные, как генерировали раньше, но уже из "API"
    return {
        "total_sales_rub": random.randint(50000, 200000),
        "units_sold": random.randint(100, 500),
        "sales_trend": random.choice(["up", "down", "stable"]),
        "conversion_rate": round(random.uniform(0.05, 0.25), 2)
    }

# По аналогии можно добавить функции для цен, остатков и т.д.