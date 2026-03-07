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

    def add_skill_event(self):
        dialog = ctk.CTkInputDialog(text="Введите новый навык:", title="Доавление")
        new_skill = dialog.get_input()
        if new_skill:
            try:
                with open("my_goals.json", "r", encoding="utf-8") as file:
                    goals = json.load(file)
            except:
                FileNotFoundError
            goals = {}
            if new_skill not in goals:
                goals[new_skill] = 0
                with open("my_goals.json", "w", encoding="utf-8") as file:
                    json.dump(goals, file, ensure_ascii=False, indent=4)
                print(f"Навык '{new_skill}' добавлен")

        else:
            print("Такой навык уже есть")


if __name__ == "__main__":
    app = App()
    app.mainloop()
