# Файл: utils/marketplace_api.py
import requests
import datetime
from typing import Dict, Any

WB_STATS_API_URL = "https://statistics-api.wildberries.ru/api/v1/supplier/"

def get_wb_sales_report(api_key: str, period_days: int) -> Dict[str, Any]:
    """
    Получает РЕАЛЬНЫЕ данные о продажах с API Wildberries,
    используя правильный эндпоинт /sales.
    """
    print(f"    [API] Выполняю запрос к эндпоинту /sales...")
    if not api_key:
        return {"error": "API ключ для Wildberries не предоставлен."}

    # Для /sales требуется полный формат даты и времени
    date_from = datetime.datetime.now() - datetime.timedelta(days=period_days)

    headers = {'Authorization': api_key}
    
    # --- ВОТ ГЛАВНОЕ ИСПРАВЛЕНИЕ: Параметры для эндпоинта /sales ---
    params = {
        # Формат YYYY-MM-DD HH:MM:SS
        'dateFrom': date_from.strftime('%Y-%m-%d %H:%M:%S'),
        'flag': 1 # 1 = сортировка по дате обновления, 0 = по дате продажи. 1 обычно эффективнее.
    }

    print(f"    [DEBUG] Отправляю запрос с ключом, который заканчивается на: ...{api_key[-6:]}")
    response = None
    try:
        # --- ИСПОЛЬЗУЕМ ПРАВИЛЬНЫЙ ЭНДПОИНТ ---
        endpoint = "sales"
        response = requests.get(f"{WB_STATS_API_URL}{endpoint}", headers=headers, params=params)
        
        # Если ключ неверный, WB вернет 401
        response.raise_for_status() 
        
        # Если все хорошо, вернется список продаж
        return {"data": response.json()}
        
    except requests.exceptions.HTTPError as http_err:
        details = response.text if response else "Нет ответа от сервера."
        print(f"    [API] HTTP ошибка: {http_err} - {details}")
        return {"error": f"HTTP ошибка: {http_err}", "details": details}
    except Exception as e:
        print(f"    [API] Произошла ошибка: {e}")
        return {"error": f"Произошла ошибка при запросе к API: {e}"}