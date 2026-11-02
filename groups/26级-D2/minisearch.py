from pathlib import Path
import sys
from collections import Counter
import re
import json
INDEX_PATH=Path(__file__).resolve().parent / "index.json"

# ===== 后端区：iter_files / analyze_file / build_index（倪生浩）=====

#传入一个目标路径，返回一个列表，储存着目标路径中拥有要求后缀的文件的相对路径。
def iter_files(root):
    root = Path(root)
    selects = ['.md', '.txt']   #需要查找的后缀
    paths = []   #储存符合后缀的文件路径
    
    #目录不存在
    if not root.is_dir():
        print(f'目录不存在:{root}', file=sys.stderr)
        sys.exit(1)
    
    for file_paths in root.rglob('*'):
        if file_paths.suffix.lower() in selects and file_paths.is_file():
            paths.append(file_paths.relative_to(root).as_posix())
    
    return sorted(paths)

#接收root和一个文件的相对路径，分析一个文件，返回一个统计字典（或者None）
def analyze_file(root, file_path):
    root = Path(root)
    
    try:    #通过以utf-8打开文件判断格式
        with open(root/file_path,'r',encoding='utf-8') as f:
            context = f.read()
    except UnicodeDecodeError:  #非utf-8文件
        print(f'警告:文件{file_path}的编码不是utf-8',file=sys.stderr)
        return None
    except PermissionError:  #无权限    
        print(f"警告：无权限读取 {file_path}", file=sys.stderr)
        return None

    #通过unicode编码识别汉字
    text = re.findall(r'[a-zA-Z]+',context) + re.findall(r'[\u4e00-\u9fa5]',context)
    counter = Counter(text)
    text_dic = sorted(counter.items(), key = lambda x:(-x[1], x[0])) #二级排序

    return {
        "path": file_path,
        "lines": len(context.splitlines()),
        "words": len(text),
        "chars": len(context),
        "top_words": [list(i) for i in text_dic[:5]]
    }

#接受root和包含所有相对路径的列表，写入index.json
def build_index(root,paths):
    root = Path(root)

    files = []  #储存所有文件的file
    for file_path in paths:
        file = analyze_file(root, file_path)
        if file is not None:
            files.append(file)

    index = {"root": root.as_posix(), "files": files}
    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")

    print(f"索引了{len(files)}个文件")

    
    
    
    
