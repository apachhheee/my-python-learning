import customtkinter as ctk
import json
import os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Мой трекер навыков")
        self.geometry("400x500")
        self.label = ctk.CTkLabel(self, text="Твои цели", font=("Arial", 20))
        self.label.pack(pady=20)
        self.button = ctk.CTkButton(
            self, text="Добавить навык", command=self.add_skill_event
        )
        self.button.pack(pady=10)
        self.skills_list = ctk.CTkFrame(self, fg_color="transparent")
        self.skills_list.pack(fill="both", expand=True)
        self.load_skills()

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
                data = json.load(file)
                for skill_name, info in data.items():
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
        except:
            print("Файл пока пуст")

    def add_xp(self, name):
        try:
            with open("my_goals.json", "r", encoding="utf-8") as file:
                goals = json.load(file)
            goals[name]["xp"] += 10
            if goals[name]["xp"] >= 100:
                goals[name]["xp"] = 0
                goals[name]["level"] += 1
                print(f"Уровень {name} повышен ")
            with open("my_goals.json", "w", encoding="utf-8") as file:
                json.dump(goals, file, ensure_ascii=False, indent=4)
            self.load_skills()
        except Exception as e:
            print(f"Ошибка прокачки{e}")

    def add_skill_event(self):
        dialog = ctk.CTkInputDialog(text="Введите новый навык:", title="Доавление")
        new_skill = dialog.get_input()
        if new_skill:
            try:
                with open("my_goals.json", "r", encoding="utf-8") as file:
                    goals = json.load(file)
            except (FileNotFoundError, json.JSONDecodeError):
                goals = {}
            if new_skill not in goals:
                goals[new_skill] = {"xp": 0, "level": 1}
                with open("my_goals.json", "w", encoding="utf-8") as file:
                    json.dump(goals, file, ensure_ascii=False, indent=4)
                print(f"Навык '{new_skill}' добавлен")
            self.load_skills()

        else:
            print("Такой навык уже есть")


if __name__ == "__main__":
    app = App()
    app.mainloop()
