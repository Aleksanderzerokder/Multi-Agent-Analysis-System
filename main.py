# Файл: main.py
# ... все импорты из предыдущей версии остаются ...
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
import uuid
from fastapi import FastAPI, HTTPException # <-- Важно импортировать HTTPException
from schemas.models import AnalysisRequest, QuestionRequest
from decision_agent.manager import DecisionManager
from llm.generator import generate_recommendations, answer_question
from config import MARKETPLACE_API_KEY, OPENAI_API_KEY

app = FastAPI(title="Мультиагентная аналитическая система", version="1.0.0")
analysis_cache = {}

@app.post("/analyze")
async def analyze_products(request: AnalysisRequest):
    # --- ВОТ ИСПРАВЛЕНИЕ: Проверяем наличие ключей перед началом работы ---
    if not MARKETPLACE_API_KEY or not OPENAI_API_KEY:
        raise HTTPException(status_code=500, detail="Один или несколько API ключей не настроены на сервере в .env файле.")

    if request.sku_list == "all":
        request.sku_list = ["SKU-123", "SKU-ABC"]

    print("Шаг 1: Сбор данных от агентов...")
    # Теперь мы уверены, что ключ не None, и анализатор спокоен
    manager = DecisionManager(marketplace_api_key=MARKETPLACE_API_KEY)
    raw_results = manager.run_analysis(
        sku_list=request.sku_list,
        period_days=request.period_days
    )
    print("Сбор данных завершен.")

    print("\nШаг 2: Генерация отчета с помощью LLM...")
    llm_recommendation = generate_recommendations(raw_results)
    print("Генерация отчета завершена.")

    request_id = str(uuid.uuid4())
    analysis_cache[request_id] = raw_results
    print(f"\nРезультаты анализа сохранены в кэш под ID: {request_id}")

    return {
        "request_id": request_id,
        "llm_summary": llm_recommendation,
        "raw_data": raw_results
    }

# Эндпоинт /question остается без изменений
@app.post("/question")
async def ask_question(request: QuestionRequest):
    print(f"\nПолучен уточняющий вопрос по request_id: {request.request_id}")
    full_report = analysis_cache.get(request.request_id)
    if not full_report:
        raise HTTPException(status_code=404, detail="Анализ с таким ID не найден.")
    sku_data = full_report.get(request.sku)
    if not sku_data:
        raise HTTPException(status_code=404, detail=f"Товар с SKU {request.sku} не найден.")
    aspect_data = sku_data.get(request.aspect)
    if not aspect_data:
        raise HTTPException(status_code=404, detail=f"Аспект '{request.aspect}' не найден.")
    llm_answer = answer_question(
        raw_data_for_aspect=aspect_data,
        aspect_name=request.aspect,
        sku=request.sku
    )
    return {"answer": llm_answer}