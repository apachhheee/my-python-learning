import random

while True:
    choises = ["камень", "ножницы", "бумага"]
    player_score = 0
    pc_score = 0

    while player_score < 3 and pc_score < 3:

        pc = random.choice(choises)
        player = input("Твой выбор (Камень,ножницы,бумага): ").lower()

    if player not in choises:
        print("Неверный ввод! Такого варианта нет. Попробуй снова.")
    continue

    print(f"Пк выбрал: {pc}")
    if player == pc:
        print("Вы оба выиграли")
    elif (
        (player == "камень" and pc == "ножницы")
        or (player == "ножницы" and pc == "бумага")
        or (player == "бумага" and pc == "камень")
    ):
        print("Ты выиграл раунд! 🎯")
        player_score += 1
    else:
        print("Компьютер выиграл раунд! 💻")
        pc_score += 1
        print("\n" + "=" * 30)
    if player_score == 3:
        print("🎉 ТЫ ПОБЕДИЛ В ИГРЕ! 🎉")
    else:
        print("💻 КОМПЬЮТЕР ПОБЕДИЛ В ИГРЕ! 💻")

    again = input("Хочешь сыграть еще? (Да/Нет): ").lower()
    if again != "да" and again != "yes" and again != "y":
        print("Заканчиваем!")
        break
