allowed=["add","show","exit"]
def check(whiteaction):
    for whiteaction in allowed:
        if action==whiteaction:
            return True
    return False

while True:
    action=input("请输入动作：")
    result=check(action)
    if result==True:
        print("允许")
    elif result==False:
        print("这个动作没被授权")