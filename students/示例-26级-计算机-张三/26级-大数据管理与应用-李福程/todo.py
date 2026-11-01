tasks = []

def add_task(tasks, task):
    tasks.append(task)
    print(f"已添加：{task}")

def show_tasks(tasks):
    if not tasks:
        print("当前没有任务。")
    else:
        for i, task in enumerate(tasks, 1):
            print(f"{i}. {task}")

while True:
    print("\n1. 添加任务")
    print("2. 查看任务")
    print("3. 退出")
    choice = input("请选择：")

    if choice == "1":
        task = input("输入任务：")
        add_task(tasks, task)
    elif choice == "2":
        show_tasks(tasks)
    elif choice == "3":
        print("再见")
        break
    else:
        print("输入有误，请重新输入。")