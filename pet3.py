import json
import os

if os.path.exists("my_goals.json"):
    with open("my_goals.json", "r", encoding="utf-8") as file:
        goals = json.load(file)
        print("Старые данные загруженны")
else:
    goals = {}
    print("Файл не найден, начинаем с чистого листа")
while True:
    skill = input(" Какой навык учим сегодня? ").lower()
    if skill == "стоп":
        break
    if skill not in goals:
        progress = input("Какой прогресс в %?")
        goals[skill] = progress
    else:
        print("Уже есть в целях")
    with open("my_goals.json", "w", encoding="utf-8") as file:
        json.dump(goals, file, ensure_ascii=False, indent=4)
    print("Данные успешно сохраненны!")
