from pathlib import Path
import sys
from collections import Counter
import re

#传入一个目标路径，返回一个列表，储存着目标路径中拥有要求后缀的文件的相对路径。
def iter_files(root):
    root = Path(root)
    #检验目录是否存在
    if not root.is_dir():
        print(f'目录不存在:{root}')
        sys.exit(1)
    
    selects = ['.md', '.txt']   #需要查找的后缀
    path = []   #储存符合后缀的文件路径
    
    for file_paths in root.rglob('*'):
        if file_paths.suffix.lower() in selects and file_paths.is_file():
            path.append(file_paths.relative_to(root).as_posix())

    return sorted(path)

#接收一个包含路径的列表，对对应文件分析，生成对应的json。
def analyze_file(root,path):
    root = Path(root)
    for file_path in path:
        try:    #通过以utf-8打开文件判断格式
            with open(root/file_path,'r',encoding='utf-8') as f:
                context = f.read()
                
                lines = len(context.splitlines())
                chars = len(context)
                
                #提取出context中的单词，数字，单个汉字，并自动统计排序放入dic中
                num = re.findall(r'\d+',context)
                alpha = re.findall(r'[a-zA-Z]+',context)
                chinese = re.findall(r'[\u4e00-\u9fa5]',context)    #通过unicode编码识别汉字
                dic = Counter(num+alpha+chinese)
                dic = sorted(words.items(), key = lambda x:(-x[1], x[0]))
                dic = [list(i) for i in words]
                words = len(dic)
                
        except UnicodeDecodeError:  #跳过非utf-8文件
            print(f'警告:文件{file_path}的编码不是utf-8',file=sys.stderr)
            break;
    
    
    
    
