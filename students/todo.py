tasks = []

def add_task(tasks, task):
    tasks.append(task)

def show_tasks(tasks):
    for i in tasks:
        print(i)

while True:
    print("1. 添加任务")
    print("2. 查看任务")
    print("3. 退出")
    c = input("请选择：")

    if c == "1":
        t = input("输入任务：")
        add_task(tasks, t)
        print(f"已添加：{t}")
    elif c == "2":
        show_tasks(tasks)
    else:
        print("再见")
