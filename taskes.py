import tkinter as tk
from tkinter import messagebox, ttk
import json
from datetime import datetime

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("مدیریت تسک‌ها")
        self.tasks = []
        self.categories = []

        self.load_categories()
        self.load_tasks()

        # بخش ورودی
        frame_input = tk.Frame(self.root)
        frame_input.pack(pady=10)

        self.entry_task = tk.Entry(frame_input, width=30)
        self.entry_task.grid(row=0, column=0, padx=5)

        self.category_combo = ttk.Combobox(frame_input, values=self.categories, state="readonly")
        self.category_combo.grid(row=0, column=1, padx=5)

        btn_add = tk.Button(frame_input, text="➕ افزودن تسک", command=self.add_task)
        btn_add.grid(row=0, column=2, padx=5)

        # بخش لیست
        self.listbox_tasks = tk.Listbox(self.root, width=50, height=15)
        self.listbox_tasks.pack(padx=10, pady=10)

        # دکمه‌ها
        frame_buttons = tk.Frame(self.root)
        frame_buttons.pack()

        btn_done = tk.Button(frame_buttons, text="✔ انجام شد / نشد", command=self.toggle_task)
        btn_done.grid(row=0, column=0, padx=5)

        btn_delete = tk.Button(frame_buttons, text="🗑 حذف", command=self.delete_task)
        btn_delete.grid(row=0, column=1, padx=5)

        self.refresh_task_list()

    def load_categories(self):
        try:
            with open("categories.json", "r", encoding="utf-8") as f:
                self.categories = json.load(f)
        except FileNotFoundError:
            self.categories = ["شخصی", "کاری", "خرید", "یادگیری"]
            self.save_categories()

    def save_categories(self):
        with open("categories.json", "w", encoding="utf-8") as f:
            json.dump(self.categories, f, ensure_ascii=False, indent=2)

    def load_tasks(self):
        try:
            with open("tasks.json", "r", encoding="utf-8") as f:
                self.tasks = json.load(f)
        except FileNotFoundError:
            self.tasks = []

    def save_tasks(self):
        with open("tasks.json", "w", encoding="utf-8") as f:
            json.dump(self.tasks, f, ensure_ascii=False, indent=2)

    def add_task(self):
        title = self.entry_task.get().strip()
        category = self.category_combo.get().strip()

        if not title:
            messagebox.showwarning("هشدار", "لطفاً عنوان تسک را وارد کنید.")
            return
        if not category:
            messagebox.showwarning("هشدار", "لطفاً یک دسته‌بندی انتخاب کنید.")
            return

        task = {
            "title": title,
            "done": False,
            "created_at": datetime.now().isoformat(),
            "category": category
        }
        self.tasks.append(task)
        self.save_tasks()
        self.entry_task.delete(0, tk.END)
        self.category_combo.set("")
        self.refresh_task_list()

    def toggle_task(self):
        selection = self.listbox_tasks.curselection()
        if not selection:
            messagebox.showwarning("هشدار", "لطفاً یک تسک را انتخاب کنید.")
            return
        index = selection[0]
        self.tasks[index]["done"] = not self.tasks[index]["done"]
        self.save_tasks()
        self.refresh_task_list()

    def delete_task(self):
        selection = self.listbox_tasks.curselection()
        if not selection:
            messagebox.showwarning("هشدار", "لطفاً یک تسک را انتخاب کنید.")
            return
        index = selection[0]
        del self.tasks[index]
        self.save_tasks()
        self.refresh_task_list()

    def refresh_task_list(self):
        self.listbox_tasks.delete(0, tk.END)
        for task in self.tasks:
            status = "✅" if task["done"] else "❌"
            category = f" ({task['category']})" if task.get("category") else ""
            self.listbox_tasks.insert(tk.END, f"{task['title']} [{status}]{category}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()