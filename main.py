# Файл: main.py
from fastapi import FastAPI
from schemas.models import AnalysisRequest

# Создаем экземпляр нашего приложения FastAPI
app = FastAPI(
    title="Мультиагентная аналитическая система",
    description="API для анализа товаров на маркетплейсах и генерации рекомендаций.",
    version="1.0.0"
)

# Определяем эндпоинт, который будет слушать POST-запросы по адресу /analyze
@app.post("/analyze")
async def analyze_products(request: AnalysisRequest):
    """
    Этот эндпоинт принимает запрос на анализ.
    FastAPI автоматически проверит, что входящие данные соответствуют
    нашей модели AnalysisRequest из schemas/models.py.

    Пока что он просто возвращает полученные данные для проверки.
    """
    return {
        "status": "received",
        "params": request.dict()
    }
