# Файл: cli_client.py
import requests
import json

# Используем внутренний, надежный адрес
BASE_URL = "http://127.0.0.1:8000"

def run_analysis():
    """Основная функция клиента: запрашивает анализ и предлагает задать вопросы."""
    
    print("--- Клиент для аналитической системы ---")
    skus_to_analyze = ["SKU-PRO", "SKU-LITE"]
    print(f"Запускаю анализ для товаров: {', '.join(skus_to_analyze)}...")

    try:
        response = requests.post(
            f"{BASE_URL}/analyze",
            json={
                "marketplace": "ozon",
                "period_days": 14,
                "sku_list": skus_to_analyze
            }
        )
        response.raise_for_status()
        data = response.json()

        print("\n✅ Отчет от LLM получен:\n")
        print("="*40)
        print(data.get("llm_summary", "Нет отчета от LLM."))
        print("="*40)

        request_id = data.get("request_id")
        if not request_id:
            print("\nНе удалось получить request_id. Уточняющие вопросы невозможны.")
            return

        # --- УЛУЧШЕНО: Показываем пользователю, о чем можно спросить ---
        analyzed_skus = list(data.get("raw_data", {}).keys())
        print(f"\nАнализ завершен. Вы можете задать уточняющие вопросы по SKU: {', '.join(analyzed_skus)}")

        while True:
            ask = input("Хотите уточнить детали? (да/нет): ").lower()
            if ask != 'да':
                print("Завершение работы.")
                break

            sku = input(f"Введите SKU товара из списка ({', '.join(analyzed_skus)}): ")
            aspect = input("Введите аспект (sales/price): ")

            question_response = requests.post(
                f"{BASE_URL}/question",
                json={
                    "request_id": request_id,
                    "sku": sku,
                    "aspect": aspect
                }
            )
            question_data = question_response.json()

            # --- УЛУЧШЕНО: Проверяем, есть ли ошибка в ответе ---
            if "error" in question_data:
                print(f"\n❌ Ошибка от сервера: {question_data['error']}")
            else:
                print("\n💡 Ответ от LLM:")
                print(f"   -> {question_data.get('answer', 'Нет ответа.')}")

    except requests.exceptions.RequestException as e:
        print(f"\n❌ Ошибка сети при обращении к API: {e}")
    except json.JSONDecodeError:
        print("\n❌ Не удалось обработать ответ от сервера. Это не JSON.")

if __name__ == "__main__":
    run_analysis()