## index.json字段要求:
```json
{
  "root": "docs",
  "files": [
    {
      "path": "guide/intro.md",
      "lines": 42,
      "words": 318,
      "chars": 1904,
      "top_words": [["python", 12], ["file", 8]]
    }
  ]
}
```

## 后端函数签名
```python
def iter_files(root: Path)                      ->  list[Path]
def analyze_file(root: Path, file_path: Path)   ->  dict  
def build_index(root: Path, paths: list[Path])  ->  None  
 
iter_files:   传入一个目标文件夹路径，返回一个列表，储存着目标路径中拥有要求后缀的文件的相对路径。  
analyze_file: 接收root和一个文件的相对路径，分析文件，返回一个统计字典（若无法访问则返回None）。  
build_index:  接受root和包含所有相对路径的列表，并写入index.json。  
```
