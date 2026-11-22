import minisearch
import os, sys
import json, time
from pathlib import Path
import argparse
from collections import Counter
import re,requests,time

def read_json():
    try:
        with open(minisearch.INDEX_PATH, 'r', encoding='utf-8') as f:
            content = json.load(f)
            return content
    except FileNotFoundError:
        print(f"没有找到.json 文件，请先运行 $minisearch.py index docs/ 来创建索引文件。")
        sys.exit(1)

def config():
    key = os.environ.get("LLM_API_KEY")
    if not key:
        print("环境变量 'LLM_API_KEY' 未设置")
        sys.exit(1)
    model = os.environ.get("LLM_MODEL", "gui-plus")
    base_url = os.environ.get("LLM_BASE_URL", "https://ws-aprqsrn7do03hxdr.cn-beijing.maas.aliyuncs.com/compatible-mode/v1")
    return {
        "key": key,
        "model": model,
        "base_url": base_url
    }

def search(query, content, top=3, en_term=1, zh_term=0.4):
    ZH = re.compile(r'[\u4e00-\u9fa5]')
    EN = re.compile(r'[a-zA-Z]+')
    en = [w.lower() for w in EN.findall(query)]
    zh = ZH.findall(query)

    root = Path(content["root"])
    files = content["files"]
    counts = []     #[(file_path, line_number, relative_number, line_content), ...]
    for file in files:
        file_path = Path(root / file["path"])
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for i, line in enumerate(lines, 1):
                en_count = sum(line.lower().count(word) for word in en)
                zh_count = sum(line.count(char) for char in zh)
                c = en_count * en_term + zh_count * zh_term
                if c > 0:
                    counts.append((file_path, i, c, line.strip()))
    counts.sort(key=lambda x: (-x[2], x[1], x[0]))  # 按相关度降序排序，相关度相同按行号升序，行号相同按文件路径升序
    return counts[:top]

def llm_post(counts,query):
    content = [{'role': 'system', 'content': '1. 只根据给出的资料回答；2. 每个结论后面标出处 file:line；3. 资料里没有，就回答「文档里没有」，不许编。'},
               {'role': 'user', 'content': '请根据以下资料回答问题：\n' + '\n'.join([f"{count[0]}:{count[1]} {count[3]}" for count in counts])+'\n\n请回答问题：\n'+query}]
    con = config()
    for t in range(2):
        try:
            resp = requests.post(
                    con['base_url'].rstrip('/') + '/chat/completions',
                    headers={'Authorization': 'Bearer ' + con['key']},
                    json={
                        'model': con['model'],
                        'messages': content,
                    },
                    timeout=30,
            )
            if resp.status_code >= 500 and t == 0:
                continue
            content = resp.json()["choices"][0]["message"]["content"]
            if not content:
                print("没有返回内容，请检查网络连接或稍后再试。",file=sys.stderr)
                sys.exit(1)
            return content
        except(requests.exceptions.Timeout, requests.exceptions.ConnectionError):
            if t == 1:
                print("请求超时或连接错误，请检查网络连接或稍后再试。",file=sys.stderr)
                sys.exit(1)
            time.sleep(2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="增强检索") 
    sub = parser.add_subparsers(dest="command", help="子命令", required=True)

    # 子命令: ask
    ask_parser = sub.add_parser("ask", help="问答")
    ask_parser.add_argument("query", type=str, help="查询内容")
    ask_parser.add_argument("--top", type=int, default=3, help="选择前几个相关句")
    ask_parser.add_argument("--json", action="store_true", help="以 JSON 格式输出")

    args = parser.parse_args()

    if args.command == "ask":
        query = args.query
        top = args.top
        json_output = args.json

        js = read_json()
        counts = search(query, js, top)
        t = time.time()
        content = llm_post(counts, query)
        latency = time.time() - t
        if json_output:
            output = {
                "answer": content,
                "sources": [f'{count[0]}:{count[1]}\n' for count in counts],
                "latency": latency,
                'tokens': {'prompt': sum(len(count[3].split()) for count in counts), 'completion': len(content.split())},
            }
            print(json.dumps(output, ensure_ascii=False, indent=4))
        else:
            print(content)
            for count in counts:
                print(f'来源: [{count[0]}:{count[1]}]')
