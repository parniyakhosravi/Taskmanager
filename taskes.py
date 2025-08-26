import json
from datetime import datetime
tasks = []


def show_menu():
    print("\n--- منوی مدیریت تسک‌ها ---")
    print("1. اضافه کردن تسک جدید")
    print("2. نمایش همه‌ی تسک‌ها")
    print("3. علامت‌گذاری تسک به عنوان انجام‌شده")
    print("4. حذف تسک")
    print("5. مرتب‌سازی بر اساس زمان")
    print("6. خروج")

def Load_tasks_from_file(filename="tasks.json"):
    global tasks
    try:
        with open(filename,"r" , encoding="utf-8") as f:
            tasks = json.load(f)
        print("📂 تسک‌ها بارگذاری شدند.")
    except FileNotFoundError:
        tasks= []
        print("📂 فایل پیدا نشد، لیست جدید ساخته شد.")        

def save_tasks_to_file(filename = "tasks.json"):
    with open(filename, "w" , encoding="utf-8") as f:
        json.dump(tasks,f,ensure_ascii=False, indent=4)
    print("📁 تسک‌ها ذخیره شدند.")
def add_task():
    title = input("عنوان تسک را وارد کنید: ")
    task = {
        "title": title,
        "done" : False,
        "created_at": datetime.now().isoformat()
    }
    tasks.append(task)
    save_tasks_to_file()
    print("✅ تسک اضافه شد.")
def show_tasks():
    if not tasks :
        print("is nill!!!!")
    else: 
        for i,task in enumerate(tasks,start=1):
            status = "✅" if task["done"] else "❌"
            print(f"{i}.{task['title']}[{status}] - crated_at: {task['created_at']}")

def mark_done():
    show_tasks()
    try:
        index = int(input("inter your num:"))-1
        if 0 <= index<len(tasks):
            tasks[index]["done"] = True
            save_tasks_to_file()
            print("✅ تسک علامت‌گذاری شد.")
        else:
             print("شماره‌ی نامعتبر.")
    except ValueError:
            print("لطفاً عدد وارد کنید.")

def delete_task():
    show_tasks()
    try:
        index = int(input("enter your remove num:"))-1
        if 0 <= index < len(tasks):
            removed = tasks.pop(index)
            save_tasks_to_file()
            print(f"❌ تسک '{removed['title']}' حذف شد.")
        else:
            print("شماره‌ی نامعتبر.")
    except ValueError:
        print("لطفاً عدد وارد کنید.")
def sort_tasks_by_time():
    tasks.sort(key=lambda task: task["created_at"])
    print("📅 تسک‌ها بر اساس زمان مرتب شدند.")
load_tasks_from_file()
while True:
    show_menu()
    choice = input("انتخاب شما: ")
    if choice == "1":
        add_task()
    elif choice == "2":
        show_tasks()
    elif choice == "3":
        mark_done()
    elif choice == "4":
        delete_task()
    elif choice == "5":
        sort_tasks_by_time()
    elif choice == "6":
        print("خروج از برنامه...")
        break
    else:
        print("انتخاب نامعتبر.")
    