import customtkinter as ctk
import json
import os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.tabview = ctk.CTkTabview(self, width=500, height=500)
        self.tabview.pack(padx=20, pady=20, fill="both", expand=True)
        self.tabview.add("Навыки")
        self.tabview.add("Магазин")
        self.label = ctk.CTkLabel(
            self.tabview.tab("Навыки"), text="Твои цели", font=("Arial", 24)
        )
        self.label.pack(pady=20)
        self.add_btn = ctk.CTkButton(
            self.tabview.tab("Навыки"),
            text="Добавить навык",
            command=self.add_skill_event,
        )
        self.add_btn.pack(pady=10)
        self.skills_list = ctk.CTkScrollableFrame(
            self.tabview.tab("Навыки"), width=450, height=300
        )
        self.skills_list.pack(pady=10, padx=10, fill="both", expand=True)
        # Магазин
        self.balance_label = ctk.CTkLabel(
            self.tabview.tab("Магазин"), text="Баланс:0", font=("Arial", 24)
        )
        self.balance_label.pack(pady=20)
        self.shop_msg = ctk.CTkLabel(
            self.tabview.tab("Магазин"), text="Здесь будут твои награды!"
        )
        self.shop_msg.pack(pady=10)

    def update_balance_display(self):
        self.balance_label.configure(text=f"Твой баланс:{self.balance}")

    def delete_skill(self, name_to_delete):
        print(f"---Пытаюсь удалить:{name_to_delete}---")
        try:
            with open("my_goals.json", "r", encoding="utf-8") as file:
                goals = json.load(file)
                if name_to_delete in goals:
                    del goals[name_to_delete]
            with open("my_goals.json", "w", encoding="utf-8") as file:
                json.dump(goals, file, ensure_ascii=False, indent=4)
            self.load_skills()
        except Exception as e:
            print(f"Ой не удалось удалить:{e}")

    def load_skills(self):
        for widget in self.skills_list.winfo_children():
            widget.destroy()
        try:
            with open("my_goals.json", "r", encoding="utf-8") as file:
                goals = json.load(file)
                self.balance = goals.get("balance", 0)
                self.update_balance_display()
                for skill_name, info in goals.items():
                    if skill_name == "balance":
                        if not isinstance(info, dict):
                            continue
                    print(f"Рисую навык:{skill_name}")
                    row = ctk.CTkFrame(self.skills_list, fg_color="transparent")
                    row.pack(fill="x", pady=2)
                    label_text = f"{skill_name} (Lvl {info["level"]})"
                    label = ctk.CTkLabel(row, text=label_text, width=150, anchor="w")
                    label.pack(side="left", padx=10)
                    progress = ctk.CTkProgressBar(
                        row, width=150
                    )  # Прогресс бар с системой опыта для навыков
                    progress.set(info["xp"] / 100)
                    progress.pack(side="left", padx=10)

                    # Начисление опыта по нажатию кнопки
                    study_btn = ctk.CTkButton(
                        row,
                        text="+XP",
                        width=40,
                        command=lambda s=skill_name: self.add_xp(s),
                    )
                    study_btn.pack(side="left", padx=10)
                    label.pack(side="left", padx=10)
                    delete_btn = ctk.CTkButton(
                        row,
                        text="X",
                        width=30,
                        fg_color="red",
                        command=lambda s=skill_name: self.delete_skill(s),
                    )
                    delete_btn.pack(side="right", padx=10)
        except Exception as e:
            print(f"Файл пока пуст{e}")

    # Денюшки и опыт
    def add_xp(self, name):
        try:
            with open("my_goals.json", "r", encoding="utf-8") as file:
                goals = json.load(file)
            goals[name]["xp"] += 10
            self.balance += 10
            goals["balance"] = self.balance
            if goals[name]["xp"] >= 100:
                goals[name]["xp"] = 0
                goals[name]["level"] += 1
                print(f"Уровень {name} повышен ")
            with open("my_goals.json", "w", encoding="utf-8") as file:
                json.dump(goals, file, ensure_ascii=False, indent=4)
            self.load_skills()
            self.update_balance_display()
        except Exception as e:
            print(f"Ошибка прокачки{e}")

    # Добавление навыков
    def add_skill_event(self):
        dialog = ctk.CTkInputDialog(text="Введите новый навык:", title="Доавление")
        new_skill = dialog.get_input()
        if new_skill:
            try:
                with open("my_goals.json", "r", encoding="utf-8") as file:
                    goals = json.load(file)
            except (FileNotFoundError, json.JSONDecodeError):
                goals = {"balance": 0}
            if new_skill not in goals:
                goals[new_skill] = {"xp": 0, "level": 1}
                with open("my_goals.json", "w", encoding="utf-8") as file:
                    json.dump(goals, file, ensure_ascii=False, indent=4)
                print(f"Навык '{new_skill}' добавлен")
            self.load_skills()

        else:
            print("Такой навык уже есть")

    # Покупка
    def buy_items(self, name, price):
        try:
            with open("my_goals.json", "r", encoding="utf-8") as file:
                goals = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            if self.balance >= price:
                self.balance -= price
                print(f"Успешно купленно{name}")
                goals["balance"] = self.balance
            with open("my_goals.json", "w", encoding="utf-8") as file:
                json.dump(goals, file, ensure_ascii=False, indent=4)
                self.update_balance_display()
        else:
            print("Недостаточно средст!")


if __name__ == "__main__":
    app = App()
    app.mainloop()
