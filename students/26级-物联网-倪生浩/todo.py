tasks = []  #任务集合

#添加任务
def add_task(tasks, task):
    if not task:
       print("任务不能为空!")
       return

    tasks.append(task)
    print("已添加", task)

#打印任务列表
def show_tasks(tasks):
    if not tasks:
        print("暂无任务")
        return
    
    for i in range(len(tasks)):
        print(f"{i+1}. {tasks[i]}")

while(True):
    print("1.添加任务")
    print("2.查看任务")
    print("3.退出")

    cho = input("请选择：")
    if cho == '1':
        task = input("输入任务：")
        add_task(tasks, task)
    elif cho == '2':
        show_tasks(tasks)
    elif cho == '3':
        print("再见")
        break
    else:
        print("请输入正确的任务")

