# minisearch 测试（8 条）

> 执行环境：Windows + Python 3.13，在 `groups/26级-D2/` 目录下执行。

| # | 场景 | 输入/准备 | 命令 | 预期 | 实际 | 通过 |
|---|------|-----------|------|------|------|------|
| 1 | 正常目录，含子目录 | docs/ 下有 a.md、cn.md、empty.md、sub/b.txt、GBK.txt | `python minisearch.py index docs/` | 生成 index.json；files 含各文件相对路径；按路径排序；字段齐全（path/lines/words/chars/top_words） | 打印「索引 4 个文件」；files 顺序为 a.md → cn.md → empty.md → sub/b.txt（按路径排序，GBK.txt 被跳过）；各条目字段齐全 | ✓ |
| 2 | 空目录 | 新建 empty/，不放任何文件 | `python minisearch.py index empty/` | 打印「索引 0 个文件」；生成空索引（files 为空数组） | 打印「索引 0 个文件」；index.json 为 `{"files": [], "root": ".../empty"}`；退出码 0 | ✓ |
| 3 | 空文件 | docs/empty.md 内容为空 | `python minisearch.py index docs/ --json` | 该文件 lines=0、words=0、chars=0 | index.json 中 empty.md 条目：`{"chars": 0, "lines": 0, "path": "empty.md", "top_words": [], "words": 0}` | ✓ |
| 4 | 目录不存在 | 用不存在的路径 no_such_dir/ | `python minisearch.py index no_such_dir/` | stderr 打印「目录不存在：no_such_dir」；退出码为 1 | stderr 输出「目录不存在:no_such_dir」 | ✓ |
| 5 | 非 UTF-8 文件 | docs/GBK.txt 以 GBK 编码保存（内容：这是一份编码为GBK的文件） | `python minisearch.py index docs/` | 程序不崩溃；stderr 打警告；该文件被跳过，其余文件正常索引 | 程序正常退出；stderr 输出「警告:文件GBK.txt的编码不是utf-8」；files 中无 GBK.txt，其余 4 个文件全部入索引 | ✓ |
| 6 | 同一个词出现多次 | sub/b.txt 中 python 出现 3 次（a.md 中出现 1 次） | `python minisearch.py search "python"` | b.txt 计数为 3；结果按次数降序 | 输出 b.txt: 3（第1行: python）在前，a.md: 1 在后，降序正确 | ✓ |
| 7 | 中文关键词搜索 | cn.md 含「这是索引测试」 | `python minisearch.py search "索引"` | 按子串匹配命中；输出匹配文件及首处匹配行 | 输出 `C:/.../docs/cn.md: 1` + 第1行: 这是索引测试 | ✓ |
| 8 | 搜不到的关键词 | 搜一个肯定没有的词 zzzz | `python minisearch.py search "zzzz"` | 输出「没有找到 "zzzz"」 | 输出「没有找到 "zzzz"」；退出码 0，不崩溃 | ✓ |

## 测试实际输出全文

```
------正常目录，含子目录+非 UTF-8 文件 ------
$ python minisearch.py index docs
警告:文件GBK.txt的编码不是utf-8
索引 4 个文件

------  空目录   ------
$ python minisearch.py index docs/empty
索引 0 个文件

------  空文件  ------
$ python minisearch.py index docs --json
{
  "files": [ ...
    {
      "chars": 0,
      "lines": 0,
      "path": "empty.md",
      "top_words": [],
      "words": 0
    }, ...
  ],
  "root": "C:/Users/NiShh/Desktop/XiW/groups/26级-D2/docs"
}

------  目录不存在  ------
$ python minisearch.py index no_such_dir
目录不存在:no_such_dir

------  同一个词出现多次   ------
$ python minisearch.py search "python"
C:/Users/NiShh/Desktop/XiW/groups/26级-D2/docs/sub/b.txt: 3
  第1行: python
C:/Users/NiShh/Desktop/XiW/groups/26级-D2/docs/a.md: 1
  第1行: python file index

------  中文关键词搜索   ------
$ python minisearch.py search "索引"
C:/Users/NiShh/Desktop/XiW/groups/26级-D2/docs/cn.md: 1
  第1行: 这是索引测试

------  搜不到的关键词   ------
$ python minisearch.py search "zzzz"
没有找到 "zzzz"
```
