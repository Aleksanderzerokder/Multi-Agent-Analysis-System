# Файл: config.py
import os
from dotenv import load_dotenv

# Эта команда загружает переменные из файла .env в окружение нашего приложения
load_dotenv()

# Читаем ключ из переменных окружения
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MARKETPLACE_API_KEY = os.getenv("MARKETPLACE_API_KEY")

# Проверка, что ключ успешно загружен
if not OPENAI_API_KEY:
    print("ПРЕДУПРЕЖДЕНИЕ: Ключ OPENAI_API_KEY не найден. Убедитесь, что у вас есть файл .env и в нем прописан ключ.")
