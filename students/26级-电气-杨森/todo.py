tasks = []

def add_task(tasks, task):
    tasks.append(task)

def show_tasks(tasks):
    for item in tasks:
        print(item)

while True:
    print("1. 添加任务")
    print("2. 查看任务")
    print("3. 退出")
    choice = input("请选择：")

    if choice == "1":
        task_text = input("输入任务：")
        add_task(tasks, task_text)
        print(f"已添加：{task_text}")
    elif choice == "2":
        show_tasks(tasks)
    elif choice == "3":
        print("再见")
        break
    else:
        print("输入选项无效，请输入1、2、3！")
