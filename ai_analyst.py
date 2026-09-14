import json
import requests


# 1. Читаем файл, который надо проанализировать
try:
    with open("input/legacy_code.vba", "r", encoding="utf-8") as file:
        code_content = file.read()
except FileNotFoundError:
    code_content = "Sub HelloWorld()\n    MsgBox 'Hello from T2'\nEnd Sub"

# 2. Формируем строгий системный промпт (задаем роль)
system_prompt = (
    "Ты — опытный Senior Software Engineer. Твоя задача — проанализировать "
    " legacy-код, который прислал пользователь, найти в нём потенциальные баги "
    "и кратко объяснить на русском языке, что этот код делает."
)

# 3. Настраиваем тело запроса к нашей локальной Ollama
payload = {
    "model": "qwen2.5:1.5b",  # имя модели, которую мы скачали
    "messages": [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Проанализируй этот код:\n\n{code_content}"},
    ],
    "stream": False,  # Просим выдать ответ целиком, а не потоком по одной букве
}

print("🤖 Отправляю код на анализ локальной нейросети через Ollama...")

# 4. Делаем обычный POST-запрос к локальному серверу Ollama
response = requests.post("http://localhost:11434/api/chat", json=payload)

if response.status_code == 200:
    result = response.json()
    ai_answer = result["message"]["content"]
    print("\n📝 ОТВЕТ НЕЙРОСЕТИ:")
    print(ai_answer)
else:
    print(f"Ошибка сервера Ollama: {response.status_code}")
