import sys
import re
import json
import argparse
from pathlib import Path
from collections import Counter
INDEX_PATH=Path(__file__).resolve().parent / "index.json"

# ===== 后端区：iter_files / analyze_file / build_index（倪生浩）=====

'''传入一个目标路径，返回一个列表，储存着目标路径中拥有要求后缀的文件的相对路径。'''
def iter_files(root):
    root = Path(root)
    selects = ['.md', '.txt']   #需要查找的后缀
    paths = []   #储存符合后缀的文件路径
    
    #目录不存在
    if not root.is_dir():
        print(f'目录不存在:{root}', file=sys.stderr)
        sys.exit(1)
    
    for file_path in root.rglob('*'):
        if file_path.suffix.lower() in selects and file_path.is_file():
            paths.append(file_path.relative_to(root).as_posix())    #储存相对路径 (root).path:Path -> [paths]  
    
    return sorted(paths)    

'''接收root和单个文件的相对路径，分析一个文件，返回一个统计字典（或者None）'''
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
    text = re.findall(r'[a-zA-Z]+',context.lower()) + re.findall(r'[\u4e00-\u9fa5]',context)
    counter = Counter(text)
    text_dic = sorted(counter.items(), key = lambda x:(-x[1], x[0])) #二级排序

    return {
        "path": file_path,
        "lines": len(context.splitlines()),
        "words": len(text),
        "chars": len(context),
        "top_words": [list(i) for i in text_dic[:5]]
    }

'''接受root和包含所有相对路径的列表，写入index.json'''
def build_index(root,paths):
    root = Path(root)

    files = []  #储存所有文件的file
    for file_path in paths:
        file = analyze_file(root, file_path)
        if file is not None:
            files.append(file)

    index = {"root": root.resolve().as_posix(), "files": files}
    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")

    print(f"索引{len(files)}个文件")

# ===== 前端区：search + main（李科学）=====

def search(keyword):
    """读 index.json，统计关键词在每个文件的出现次数，按次数降序输出。"""
    try:
        with open(INDEX_PATH, encoding="utf-8") as f:
            index = json.load(f)
    except FileNotFoundError:
        print("还没有索引，请先运行：python minisearch.py index docs/", file=sys.stderr)
        sys.exit(1)

    root = Path(index["root"])
    kw = keyword.lower()
    results = []

    for record in index["files"]:
        file_path = root / record["path"]
        try:
            with open(file_path, encoding="utf-8") as f:
                lines = f.readlines()
        except OSError:
            continue

        count = 0
        first_line = ""
        for line in lines:
            hits = line.lower().count(kw)
            if hits > 0:
                count += hits
                if not first_line:
                    first_line = line.strip()

        if count > 0:
            results.append((count, record["path"], first_line))

    results.sort(key=lambda item: (-item[0], item[1]))

    if not results:
        print(f'没有找到 "{keyword}"')
        return

    for count, path, first_line in results:
        print(f"{path}: {count} 次")
        if first_line:
            print(f"  首次出现：{first_line}")


def main():
    parser = argparse.ArgumentParser(description="minisearch 极简文档搜索")
    sub = parser.add_subparsers(dest="command", required=True)

    index_parser = sub.add_parser("index", help="为指定目录建索引")
    index_parser.add_argument("directory", help="目标目录，如 docs/")

    search_parser = sub.add_parser("search", help="在索引中搜索关键词")
    search_parser.add_argument("keyword", help="关键词，如 python")

    args = parser.parse_args()

    if args.command == "index":
        paths = iter_files(args.directory)
        build_index(args.directory, paths)
    elif args.command == "search":
        search(args.keyword)


if __name__ == "__main__":
    main()
    
    
    
