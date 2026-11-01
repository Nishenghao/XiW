tasks=[]
def add_task(tasks,task):
    tasks.append(task)
    print(f"已添加：{task}")
def show_tasks(tasks):
    print(tasks)
while True:
    print("1.添加任务")
    print("2.查看任务")
    print("3.退出")
    choice=input("请选择；")
    if choice=="1":
        task=input("请输入：")
        add_task(tasks,task)
    elif choice=="2":
        show_tasks(tasks)
    elif choice=="3":
        print("再见")
        break
         

