goals = []
while True:
    new_skill = input("Какой навык необходимо выучить сегодня? ").lower()
    if new_skill == "стоп":
        break
    if new_skill not in goals:
        goals.append(new_skill)
        count = len(goals)
        print("Сейчас в твоем списке", count)
        print("Сейчав в твоем списке:", goals)
    else:
        print("Этот навык уже добавлен,попробуйте другое")

print("Финальный список:", goals)
print(f"Что бы уехать тебе обходимо выуычить {len(goals)} методов")
