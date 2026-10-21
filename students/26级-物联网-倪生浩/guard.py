allowed = ["add", "show", "exit"] #白名单

def check(action):
    for i in allowed:
        if i == action:
            return True
    return False

action = input("输入动作：")
if(check(action)):
    print("允许")
else:
    print("拒绝：这个动作没被授权")
