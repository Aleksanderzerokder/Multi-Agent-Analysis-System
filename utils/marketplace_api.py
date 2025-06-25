# Файл: utils/marketplace_api.py (ОТЛАДОЧНАЯ ВЕРСИЯ)

import requests
import datetime
from typing import Dict, Any

# --- ИЗМЕНЕНИЕ: Используем IP-адрес напрямую ---
IP_ADDRESS = "104.18.9.93"
DOMAIN_NAME = "suppliers-api.wildberries.ru"

# Собираем URL с IP-адресом
WB_CONTENT_API_URL_BY_IP = f"https://{IP_ADDRESS}"

# Старый URL для статистики оставляем, так как он работает
WB_STATS_API_URL = "https://statistics-api.wildberries.ru/api/v1/supplier/"


# Функция получения списка товаров (модифицированная)
def get_all_wb_products(api_key: str) -> Dict[str, Any]:
    print(f"    [API-DEBUG] Запрашиваю список товаров НАПРЯМУЮ по IP: {IP_ADDRESS}...")
    if not api_key:
        return {"error": "API ключ не предоставлен."}
    
    endpoint = "/content/v2/get/cards/list"
    
    # --- ИЗМЕНЕНИЕ: Формируем заголовки со специальным полем 'Host' ---
    headers = {
        'Authorization': api_key,
        'Host': DOMAIN_NAME  # Говорим серверу, к какому домену мы на самом деле обращаемся
    }
    
    payload = {
        "settings": { "cursor": { "limit": 1000 }, "filter": { "withPhoto": -1 } }
    }

    try:
        # --- ИЗМЕНЕНИЕ: Обращаемся к URL по IP-адресу ---
        response = requests.post(WB_CONTENT_API_URL_BY_IP + endpoint, headers=headers, json=payload)
        response.raise_for_status()
        cards = response.json().get("cards", [])
        product_list = [
            {"sku": card.get("vendorCode"), "name": card.get("title"), "product_id_wb": card.get("nmID")}
            for card in cards if card.get("vendorCode")
        ]
        return {"products": product_list}
    except requests.exceptions.RequestException as e:
        # Мы ловим именно RequestException, чтобы увидеть любые сетевые проблемы
        print(f"    [API-DEBUG] Ошибка при получении списка товаров по IP: {e}")
        return {"error": str(e)}

# Функция получения данных о продажах (остается без изменений, так как она работает)
def get_wb_sales_report(api_key: str, period_days: int) -> Dict[str, Any]:
    # ... код без изменений ...
    return {} # Временно, чтобы не загромождать вывод