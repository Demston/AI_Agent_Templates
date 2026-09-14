import os
from crewai import Agent, Crew, Process, Task, LLM

# 1. Подключаем локальную Ollama с моделью Qwen
local_llm = LLM(
    model="ollama/qwen2.5:1.5b",
    base_url="http://localhost:11434"
)

# 2. Читаем наш legacy-файл (VBA код из Access)
try:
    with open("input/legacy_code.vba", "r", encoding="utf-8") as f:
        vba_code_content = f.read()
except FileNotFoundError:
    vba_code_content = "Sub Error() \n MsgBox 'Файл не найден!' \n End Sub"

# 3. Указываем пути к нашим YAML-файлам конфигурации
agents_config_path = os.path.join(os.path.dirname(__file__), 'agents/agents.yaml')
tasks_config_path = os.path.join(os.path.dirname(__file__), 'tasks/tasks.yaml')

# 4. Инициализируем Агентов, загружая их параметры из YAML
# Мы вручную парсим файлы и берем нужный ключ конфигурации
import yaml

with open(agents_config_path, 'r', encoding='utf-8') as f:
    agents_yaml = yaml.safe_load(f)

with open(tasks_config_path, 'r', encoding='utf-8') as f:
    tasks_yaml = yaml.safe_load(f)

writer_agent = Agent(
    config=agents_yaml['technical_writer'],
    verbose=True,
    llm=local_llm
)

auditor_agent = Agent(
    config=agents_yaml['security_engineer'],
    verbose=True,
    llm=local_llm
)

# 5. Инициализируем Задачи, подставляя VBA-код в шаблон документации
# Важно: пробрасываем vba_code во входящие переменные задачи
task1 = Task(
    config=tasks_yaml['documentation_task'],
    agent=writer_agent
)
# Перезаписываем описание задачи, подставляя туда наш реальный код
task1.description = tasks_yaml['documentation_task']['description'].format(vba_code=vba_code_content)

task2 = Task(
    config=tasks_yaml['audit_task'],
    agent=auditor_agent
)

# 6. Собираем и запускаем последовательную Команду (Crew)
my_crew = Crew(
    agents=[writer_agent, auditor_agent],
    tasks=[task1, task2],
    process=Process.sequential,
    verbose=True
)

print("🚀 Запускаю промышленный YAML-конвейер CrewAI...")
final_report = my_crew.kickoff()

# 7. Сохраняем результат
with open("output/VBA_YAML_Audit_Report.md", "w", encoding="utf-8") as out_file:
    out_file.write(str(final_report))

print("\n🏆 Проверка завершена! Результат сохранен в файл VBA_YAML_Audit_Report.md")
