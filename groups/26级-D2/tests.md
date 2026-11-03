# minisearch 测试（8 条）

> 

| # | 场景 | 输入/准备 | 命令 | 预期 | 通过 | 通过 |
|---|------|-----------|------|------|------|------|
| 1 | 正常目录，含子目录 | docs/ 下有 a.md、sub/b.txt | `python minisearch.py index docs/` | 生成 index.json；files 含 a.md 和 sub/b.txt 两个相对路径；按路径排序；字段齐全（path/lines/words/chars/top_words） | | |
| 2 | 空目录 | 建 empty/，不放任何文件 | `python minisearch.py index empty/` | 打印「索引0个文件」；生成空索引（files 为空数组） | | |
| 3 | 空文件 | docs/empty.md 内容为空 | `python minisearch.py index docs/` | 该文件 lines=0、words=0、chars=0 | | |
| 4 | 目录不存在 | 用不存在的路径 no_such_dir/ | `python minisearch.py index no_such_dir/` | 打印「目录不存在：no_such_dir」；退出码为 1 | | |
| 5 | 非 UTF-8 文件 | 用 GBK 编码存 docs/gbk.txt | `python minisearch.py index docs/` | 程序不崩溃；能正常生成索引（容错跳过或按约定处理） | | |
| 6 | 同一个词出现多次 | 某文件里 python 出现 3 次 | `python minisearch.py search "python"` | 该文件计数为 3；结果按次数降序 | | |
| 7 | 中文关键词搜索 | 某文件含「索引」 | `python minisearch.py search "索引"` | 按子串匹配命中；输出匹配文件及首处匹配行 | | |
| 8 | 搜不到的关键词 | 搜一个肯定没有的词 zzzz | `python minisearch.py search "zzzz"` | 输出「没有找到"zzzz"」 | | |

## 组内分工（按实际改姓名）
- 每人至少 2 条：A → #1 #2；B → #3 #4；C → #5 #6；我 → #7 #8

## 填通过时的核对点
- #2 必须是「索引0个文件」
- #3 三个计数全为 0
- #4 退出码必须为 1（可用 `echo $?` 查看）
- #5 不能崩
- #8 文案要带引号关键词