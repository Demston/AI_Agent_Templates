import os
from crewai import Agent, Crew, Process, Task, LLM


# 1. Подключаем нашу локальную Ollama с моделью Qwen, которую ты вчера скачал
local_llm = LLM(
    model="ollama/qwen2.5:1.5b", base_url="http://localhost:11434"
)

# 2. Читаем наш legacy-файл (VBA код из Access)
try:
    with open("input/legacy_code.vba", "r", encoding="utf-8") as f:
        vba_code = f.read()
except FileNotFoundError:
    vba_code = "Sub Error() \n MsgBox 'Файл не найден!' \n End Sub"

# 3. Создаем Первого Агента — Технический Писатель (Документатор)
writer_agent = Agent(
    role="Technical Writer",
    goal="Создать подробное техническое описание и алгоритм работы присланного кода.",
    backstory="Ты — опытный технический писатель в ИТ-департаменте телекома. Умеешь переводить сложный legacy-код "
              "на понятный русский язык.",
    verbose=True,
    llm=local_llm,
)

# 4. Создаем Второго Агента — Эксперт по безопасности (Аудитор)
auditor_agent = Agent(
    role="Senior Security Engineer",
    goal="Найти критические баги, уязвимости и потенциальные краши в присланном коде.",
    backstory="Ты — въедливый аудитор безопасности. Ищешь скрытые дефекты, отсутствие обработчиков ошибок "
              "и проблемы с памятью/БД.",
    verbose=True,
    llm=local_llm,
)

# 5. Нарезаем задачи для Агентов
task1 = Task(
    description=f"Проанализируй этот VBA-код и напиши техническую документацию на русском языке (что делает функция, "
                f"какие объекты использует):\n\n{vba_code}",
    expected_output="Структурированное техническое описание кода.",
    agent=writer_agent,
)

task2 = Task(
    description="Изучи техническое описание из предыдущей задачи и сам исходный код. Найди критические баги "
                "и напиши рекомендации по исправлению на русском языке.",
    expected_output="Список найденных багов, уязвимостей и код исправлений.",
    agent=auditor_agent,
)

# 6. Собираем Команду (Crew) в последовательный конвейер (Process.sequential)
my_crew = Crew(
    agents=[writer_agent, auditor_agent],
    tasks=[task1, task2],
    process=Process.sequential,  # Результат Task1 автоматически полетит на вход Task2!
    verbose=True,
)

print("🚀 Запускаю мультиагентный конвейер CrewAI...")
final_report = my_crew.kickoff()

# 7. Сохраняем готовый отчет для твоего сеньора в файл
with open("output/VBA_Audit_Report.md", "w", encoding="utf-8") as out_file:
    out_file.write(str(final_report))

print("\n🏆 Проверка завершена! Результат сохранен в файл VBA_Audit_Report.md")
