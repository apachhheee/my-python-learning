import customtkinter as ctk
import json

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.balance = 0
        self.title("Трекер навыков и магазин")
        self.geometry("600x600")

        self.tabview = ctk.CTkTabview(self, width=500, height=500)
        self.tabview.pack(padx=20, pady=20, fill="both", expand=True)
        self.tabview.add("Навыки")
        self.tabview.add("Магазин")

        # Вкладка "Навыки"
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

        # Вкладка "Магазин"
        self.balance_label = ctk.CTkLabel(
            self.tabview.tab("Магазин"), text="Баланс: 0", font=("Arial", 24)
        )
        self.balance_label.pack(pady=20)

        self.shop_msg = ctk.CTkLabel(
            self.tabview.tab("Магазин"), text="Здесь будут твои награды!"
        )
        self.shop_msg.pack(pady=10)

        self.add_item_btn = ctk.CTkButton(
            self.tabview.tab("Магазин"),
            text="Добавить награду",
            command=self.add_item_event,
        )
        self.add_item_btn.pack(pady=10)

        self.shop_list = ctk.CTkScrollableFrame(
            self.tabview.tab("Магазин"), width=450, height=300
        )
        self.shop_list.pack(pady=10, padx=10, fill="both", expand=True)

        # Загрузка данных при старте
        self.load_skills()
        self.load_shop()

    # Работа с магазином
    def add_item_event(self):
        """Добавление новой награды в магазин"""
        dialog_name = ctk.CTkInputDialog(
            text="Что хочешь купить?", title="Новая награда"
        )
        name = dialog_name.get_input()
        if not name:
            return

        price_dialog = ctk.CTkInputDialog(
            text="Сколько это будет стоить?", title="Цена"
        )
        price_str = price_dialog.get_input()
        if price_str and price_str.isdigit():
            price = int(price_str)
            try:
                with open("my_goals.json", "r", encoding="utf-8") as f:
                    goals = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                goals = {"balance": 0}

            # Добавляем предмет в магазин (создаём ключ shop, если его нет)
            if "shop" not in goals:
                goals["shop"] = {}
            goals["shop"][name] = price

            with open("my_goals.json", "w", encoding="utf-8") as f:
                json.dump(goals, f, ensure_ascii=False, indent=4)

            self.load_shop()
        else:
            print("Некорректная цена")

    def load_shop(self):
        """Отобразить все товары из магазина"""
        for widget in self.shop_list.winfo_children():
            widget.destroy()

        try:
            with open("my_goals.json", "r", encoding="utf-8") as f:
                goals = json.load(f)
            shop_items = goals.get("shop", {})
            for item_name, price in shop_items.items():
                row = ctk.CTkFrame(self.shop_list)
                row.pack(fill="x", pady=5, padx=5)

                label = ctk.CTkLabel(row, text=f"{item_name} - {price}")
                label.pack(side="left", padx=5)

                buy_btn = ctk.CTkButton(
                    row,
                    text="Купить",
                    width=60,
                    command=lambda n=item_name, p=price: self.buy_item(n, p),
                )
                buy_btn.pack(side="right", padx=5)
        except Exception as e:
            print(f"Ошибка загрузки магазина: {e}")

    def buy_item(self, name, price):
        """Покупка предмета из магазина"""
        try:
            with open("my_goals.json", "r", encoding="utf-8") as f:
                goals = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            print("Файл с данными не найден или повреждён")
            return

        current_balance = goals.get("balance", 0)
        if current_balance >= price:
            goals["balance"] = current_balance - price
            self.balance = goals["balance"]

            # Здесь можно добавить предмет в инвентарь, если нужно
            # goals.setdefault("inventory", []).append(name)

            with open("my_goals.json", "w", encoding="utf-8") as f:
                json.dump(goals, f, ensure_ascii=False, indent=4)

            self.update_balance_display()
            print(f"Куплено: {name} за {price}")
        else:
            print("Недостаточно средств!")

    def update_balance_display(self):
        """Обновить отображение баланса в интерфейсе"""
        self.balance_label.configure(text=f"Баланс: {self.balance}")

    # Работа с навыками
    def add_skill_event(self):
        """Добавление нового навыка"""
        dialog = ctk.CTkInputDialog(text="Введите новый навык:", title="Добавление")
        new_skill = dialog.get_input()
        if not new_skill:
            return

        if new_skill in ("balance", "shop"):
            print("Нельзя создать навык с таким именем")
            return

        try:
            with open("my_goals.json", "r", encoding="utf-8") as f:
                goals = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            goals = {"balance": 0}

        if new_skill not in goals:
            goals[new_skill] = {"xp": 0, "level": 1}
            with open("my_goals.json", "w", encoding="utf-8") as f:
                json.dump(goals, f, ensure_ascii=False, indent=4)
            print(f"Навык '{new_skill}' добавлен")
            self.load_skills()
        else:
            print("Такой навык уже есть")

    def delete_skill(self, name_to_delete):
        """Удаление навыка"""
        if name_to_delete in ("balance", "shop"):
            print("Нельзя удалить служебный раздел")
            return

        print(f"Удаляем: {name_to_delete}")
        try:
            with open("my_goals.json", "r", encoding="utf-8") as f:
                goals = json.load(f)

            if name_to_delete in goals:
                del goals[name_to_delete]

                with open("my_goals.json", "w", encoding="utf-8") as f:
                    json.dump(goals, f, ensure_ascii=False, indent=4)

                self.load_skills()
        except Exception as e:
            print(f"Ошибка удаления: {e}")

    def add_xp(self, name):
        """Добавить опыт навыку и начислить монеты"""
        if name in ("balance", "shop"):
            print("Нельзя добавить XP служебному разделу")
            return

        try:
            with open("my_goals.json", "r", encoding="utf-8") as f:
                goals = json.load(f)

            if name not in goals:
                return

            goals[name]["xp"] += 10
            self.balance += 10
            goals["balance"] = self.balance

            if goals[name]["xp"] >= 100:
                goals[name]["xp"] = 0
                goals[name]["level"] += 1
                print(f"Уровень навыка '{name}' повышен до {goals[name]['level']}")

            with open("my_goals.json", "w", encoding="utf-8") as f:
                json.dump(goals, f, ensure_ascii=False, indent=4)

            self.load_skills()  # обновить отображение навыков
            self.update_balance_display()
        except Exception as e:
            print(f"Ошибка при добавлении XP: {e}")

    def load_skills(self):
        """Загрузить и отобразить все навыки из файла"""

        for widget in self.skills_list.winfo_children():
            widget.destroy()

        try:
            with open("my_goals.json", "r", encoding="utf-8") as f:
                goals = json.load(f)

            self.balance = goals.get("balance", 0)
            self.update_balance_display()

            for skill_name, info in goals.items():
                if skill_name in ("balance", "shop"):
                    continue

                if (
                    not isinstance(info, dict)
                    or "level" not in info
                    or "xp" not in info
                ):
                    continue

                row = ctk.CTkFrame(self.skills_list, fg_color="transparent")
                row.pack(fill="x", pady=2)

                label_text = f"{skill_name} (Lvl {info['level']})"
                label = ctk.CTkLabel(row, text=label_text, width=150, anchor="w")
                label.pack(side="left", padx=10)

                progress = ctk.CTkProgressBar(row, width=150)
                progress.set(info["xp"] / 100.0)  # прогресс от 0 до 1
                progress.pack(side="left", padx=10)

                study_btn = ctk.CTkButton(
                    row,
                    text="+XP",
                    width=40,
                    command=lambda s=skill_name: self.add_xp(s),
                )
                study_btn.pack(side="left", padx=5)

                delete_btn = ctk.CTkButton(
                    row,
                    text="X",
                    width=30,
                    fg_color="red",
                    command=lambda s=skill_name: self.delete_skill(s),
                )
                delete_btn.pack(side="right", padx=10)

        except FileNotFoundError:
            print("Файл my_goals.json не найден. Будет создан при добавлении навыка.")
        except Exception as e:
            print(f"Ошибка загрузки навыков: {e}")


if __name__ == "__main__":
    app = App()
    app.mainloop()
