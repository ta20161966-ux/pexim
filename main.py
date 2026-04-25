import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os

# --- 1. Список предопределённых задач ---
tasks = [
    {"name": "Прочитать статью", "type": "учёба"},
    {"name": "Сделать зарядку", "type": "спорт"},
    {"name": "Написать отчёт", "type": "работа"},
    {"name": "Посмотреть лекцию", "type": "учёба"},
    {"name": "Сходить на пробежку", "type": "спорт"},
    {"name": "Провести созвон", "type": "работа"},
]

# --- 2. Работа с историей (JSON) ---
HISTORY_FILE = 'history.json'

def load_history():
    """Загружает историю из файла JSON, если он существует."""
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_history(history):
    """Сохраняет историю в файл JSON."""
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=4)

# --- 3. Основная логика приложения ---
class TaskGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Task Generator")
        self.root.geometry("500x500")

        self.history = load_history()
        self.filter_type = tk.StringVar(value="все")  # По умолчанию — все задачи

        # --- Виджеты ---
        # Текущая задача
        self.current_task_label = tk.Label(root, text="Ваша задача появится здесь", font=('Arial', 12), wraplength=400)
        self.current_task_label.pack(pady=10)

        # Кнопка генерации
        self.generate_btn = tk.Button(root, text="Сгенерировать задачу", command=self.generate_task)
        self.generate_btn.pack(pady=5)

        # Фильтр по типу
        filter_frame = tk.Frame(root)
        filter_frame.pack(pady=5)
        
        tk.Label(filter_frame, text="Фильтр по типу:").pack(side=tk.LEFT)
        type_options = ["все"] + list(set(task['type'] for task in tasks))
        self.filter_combo = ttk.Combobox(filter_frame, textvariable=self.filter_type, values=type_options, state="readonly", width=15)
        self.filter_combo.pack(side=tk.LEFT, padx=5)
        self.filter_combo.bind("<<ComboboxSelected>>", self.update_history_display)

        # История задач (Listbox + Scrollbar)
        history_frame = tk.Frame(root)
        history_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(history_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.history_listbox = tk.Listbox(history_frame, yscrollcommand=scrollbar.set, font=('Arial', 10))
        self.history_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.history_listbox.yview)
        
        self.update_history_display()

        # Добавление новой задачи
        add_frame = tk.Frame(root)
        add_frame.pack(pady=10)
        
        tk.Label(add_frame, text="Новая задача:").pack(side=tk.LEFT)
        self.new_task_entry = tk.Entry(add_frame, width=30)
        self.new_task_entry.pack(side=tk.LEFT, padx=5)
        
        tk.Label(add_frame, text="Тип:").pack(side=tk.LEFT)
        self.new_task_type_combo = ttk.Combobox(add_frame, values=["учёба", "спорт", "работа"], state="readonly", width=10)
        self.new_task_type_combo.pack(side=tk.LEFT, padx=5)
        
        self.add_task_btn = tk.Button(add_frame, text="Добавить задачу", command=self.add_new_task)
        self.add_task_btn.pack(side=tk.LEFT, padx=5)

    def generate_task(self):
        """Генерирует случайную задачу с учётом фильтра."""
        filter_val = self.filter_type.get()
        
        if filter_val == "все":
            filtered_tasks = tasks
        else:
            filtered_tasks = [t for t in tasks if t['type'] == filter_val]
            
        if not filtered_tasks:
            messagebox.showwarning("Нет задач", f"Нет задач типа '{filter_val}'")
            return

        task = random.choice(filtered_tasks)
        
        # Обновляем отображение текущей задачи
        self.current_task_label.config(text=f"Задача: {task['name']} (Тип: {task['type']})")
        
        # Добавляем в историю и сохраняем
        self.history.append(task)
        save_history(self.history)
        
        # Обновляем список истории в GUI
        self.update_history_display()

    def update_history_display(self, event=None):
        """Обновляет отображение истории в Listbox с учётом фильтра."""
        self.history_listbox.delete(0, tk.END)
        
        filter_val = self.filter_type.get()
        
        for task in self.history:
            if filter_val == "все" or task['type'] == filter_val:
                self.history_listbox.insert(tk.END, f"{task['name']} ({task['type']})")

    def add_new_task(self):
        """Добавляет новую задачу в список с проверкой на пустую строку."""
        name = self.new_task_entry.get().strip()
        task_type = self.new_task_type_combo.get()

        if not name or not task_type:
            messagebox.showerror("Ошибка", "Поля 'Задача' и 'Тип' должны быть заполнены!")
            return

        new_task = {"name": name, "type": task_type}
        
        # Добавляем в общий список и сразу генерируем её (или просто добавляем?)
        tasks.append(new_task) 
        
        # Очищаем поля ввода
        self.new_task_entry.delete(0, tk.END)
        
# --- Запуск приложения ---
if __name__ == "__main__":
    root = tk.Tk()
    app = TaskGeneratorApp(root)
    root.mainloop()
