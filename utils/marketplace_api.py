# Файл: utils/marketplace_api.py

# ==============
# БЛОК ИМПОРТОВ
# ==============
import requests
import datetime
from typing import Dict, Any, List

# =================
# БЛОК КОНСТАНТ
# =================
# Базовый URL для API статистики
WB_STATS_API_URL = "https://statistics-api.wildberries.ru/api/v1/supplier/"
# Базовый URL для API Контента
WB_CONTENT_API_URL = "https://suppliers-api.wildberries.ru/"


# ==================================
# ФУНКЦИЯ ПОЛУЧЕНИЯ ДАННЫХ О ПРОДАЖАХ
# ==================================
def get_wb_sales_report(api_key: str, period_days: int) -> Dict[str, Any]:
    """
    Получает РЕАЛЬНЫЕ данные о продажах с API Wildberries,
    используя правильный эндпоинт /sales.
    """
    print(f"    [API] Выполняю запрос к эндпоинту /sales...")
    if not api_key:
        return {"error": "API ключ для Wildberries не предоставлен."}

    date_from = datetime.datetime.now() - datetime.timedelta(days=period_days)
    headers = {'Authorization': api_key}
    params = {
        'dateFrom': date_from.strftime('%Y-%m-%d %H:%M:%S'),
        'flag': 1
    }
    
    response = None
    try:
        endpoint = "sales"
        response = requests.get(f"{WB_STATS_API_URL}{endpoint}", headers=headers, params=params)
        response.raise_for_status() 
        return {"data": response.json()}
    except requests.exceptions.HTTPError as http_err:
        details = response.text if response else "Нет ответа от сервера."
        print(f"    [API] HTTP ошибка: {http_err} - {details}")
        return {"error": f"HTTP ошибка: {http_err}", "details": details}
    except Exception as e:
        print(f"    [API] Произошла ошибка: {e}")
        return {"error": f"Произошла ошибка при запросе к API: {e}"}


# ============================================
# ФУНКЦИЯ ПОЛУЧЕНИЯ СПИСКА ВСЕХ ТОВАРОВ
# ============================================
def get_all_wb_products(api_key: str) -> Dict[str, Any]:
    """
    Получает список всех товаров продавца с их артикулами и названиями.
    """
    print(f"    [API] Запрашиваю список всех товаров...")
    if not api_key:
        return {"error": "API ключ для Wildberries не предоставлен."}
        
    endpoint = "/content/v2/get/cards/list"
    headers = {'Authorization': api_key}
    
    payload = {
        "settings": {
            "cursor": { "limit": 1000 },
            "filter": { "withPhoto": -1 }
        }
    }

    try:
        response = requests.post(WB_CONTENT_API_URL + endpoint, headers=headers, json=payload)
        response.raise_for_status()
        
        cards = response.json().get("cards", [])
        
        product_list = []
        for card in cards:
            product_list.append({
                "sku": card.get("vendorCode"),
                "name": card.get("title"),
                "product_id_wb": card.get("nmID")
            })

        return {"products": product_list}

    except Exception as e:
        print(f"    [API] Ошибка при получении списка товаров: {e}")
        return {"error": str(e)}