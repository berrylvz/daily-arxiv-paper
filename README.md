# arXiv Daily Paper

一个简洁的 Python 工具：按关键词抓取 arXiv 论文，提取标题、链接、摘要，调用 DeepSeek API 翻译摘要为中文，并输出为按日期命名的 Markdown 日报。

## 功能

- 按关键词抓取 arXiv 论文
- 提取标题、链接、英文摘要
- 使用 DeepSeek API 翻译中文摘要
- 支持 `--date YYMMDD` 按指定自然日过滤 arXiv 更新时间
- 按 `cs` 和 `stat` 主分类过滤结果，和 `DailyArxiv/` 一致
- 每个关键词先搜索 50 篇，再在过滤后保存前 15 篇
- 输出单个 Markdown 文件，按关键词分节

## 目录结构

```text
.
├── PLAN.md
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── run.sh
├── main.py
├── config.py
└── src/
    ├── __init__.py
    ├── logger.py
    ├── models.py
    ├── arxiv_client.py
    ├── translator.py
    ├── writer.py
    └── utils.py
```

## 安装

1. 创建虚拟环境并安装依赖：

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. 配置环境变量：

```bash
cp .env.example .env
```

编辑 `.env`，填入你的 `DEEPSEEK_API_KEY`。

## 配置

所有核心配置都在 [config.py](./config.py)：

- `KEYWORDS`
- `SEARCH_MAX_RESULTS_PER_KEYWORD`
- `SAVE_MAX_RESULTS_PER_KEYWORD`
- `OUTPUT_DIR`
- `DEEPSEEK_MODEL`
- `REQUEST_TIMEOUT`
- `RETRY_TIMES`
- `ARXIV_BASE_URL`
- `TARGET_PRIMARY_CATEGORIES`

默认关键词：

- `Vision Language Action`
- `world model`
- `world action model`
- `robot`

## 运行

默认抓取当天更新时间对应的论文：

```bash
python main.py
```

抓取指定日期，例如 2026 年 6 月 25 日：

```bash
python main.py --date 260625
```

也可以使用一键脚本：

```bash
bash run.sh
bash run.sh --date 260625
```

`run.sh` 面向类 Unix 环境。Windows 用户直接使用 `python main.py --date 260625` 即可。

## 输出

输出目录默认是 `outputs/`，文件名格式为 `YYMMDD.md`。

例如：

- 默认当天：`outputs/260629.md`
- 指定日期：`outputs/260625.md`

Markdown 内容包含：

- 生成日期
- 目标抓取日期
- 关键词数量
- 论文总数
- 每个关键词下的论文标题、链接、英文摘要、中文摘要

## 注意事项

- 该实现仅参考需求，不复用 `DailyArxiv/` 或 `deepseek-api.py` 中的代码
- 日期过滤基于 arXiv 返回的更新时间字段
- 分类过滤与 `DailyArxiv/` 保持一致，仅保留 `cs.*` 和 `stat.*`
- 每个关键词请求 arXiv 时最多搜索 50 篇，过滤后最多保存 15 篇；不足 15 篇则全部保存
- 如果某篇论文翻译失败，程序会继续执行，并在输出中标记“翻译失败”
- 如果某个关键词没有匹配论文，输出中会保留该章节并注明无匹配论文
- 如果 `.env` 中缺少 `DEEPSEEK_API_KEY`，程序会直接报错退出

## Reference

https://github.com/Ed1sonChen/DailyArxiv
