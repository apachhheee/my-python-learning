goals = []
while True:
    new_skill = input(
        "Какой навык необходимо выучить сегодня? (Напиши стоп если хочешь закончить)"
    ).lower
    if new_skill == "стоп":
        break
    goals.append(new_skill)
    print("Сейчав в твоем списке:", goals)
print("Финальный список:", goals)
