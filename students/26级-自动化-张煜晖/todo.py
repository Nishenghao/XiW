# -*- coding: utf-8 -*-
"""命令行待办清单"""

tasks = []  # 用列表存任务


def add_task(tasks, task):
    """把 task 追加进列表"""
    tasks.append(task)
    print(f"已添加：{task}")


def show_tasks(tasks):
    """把列表里的任务逐条打印出来"""
    if not tasks:
        print("暂时没有任务。")
        return
    print("当前任务：")
    for i, task in enumerate(tasks, start=1):
        print(f"{i}. {task}")


while True:
    print("\n===== 待办清单 =====")
    print("1. 添加任务")
    print("2. 查看任务")
    print("3. 退出")
    choice = input("请输入选项（1/2/3）：").strip()

    if choice == "1":
        task = input("请输入任务内容：").strip()
        if task:
            add_task(tasks, task)
        else:
            print("任务内容不能为空。")
    elif choice == "2":
        show_tasks(tasks)
    elif choice == "3":
        print("再见！")
        break
    else:
        print("无效选项，请输入 1、2 或 3。")
