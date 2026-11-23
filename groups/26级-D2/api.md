## 输入输出标准
```
输入：ask '问题字符串'
输出：{
  "answer": "...",
  "sources": ["docs/招新.md:12"],
  "latency": 1.8,
  "tokens": {"prompt": 123, "completion": 45}
}
错误: 缺 key ->   环境变量 'LLM_API_KEY' 未设置
      缺索引  ->  没有找到.json 文件，请先运行 $minisearch.py index docs/ 来创建索引文件。
      超时    ->  请求超时或连接错误，请检查网络连接或稍后再试。
      空返回  ->  没有返回内容，请检查网络连接或稍后再试。
```
