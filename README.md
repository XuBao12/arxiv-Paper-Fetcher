# arXiv Paper Fetcher

一个自动从 arXiv 获取特定研究领域论文的系统。

## 功能特点

- 根据配置的类别和搜索词自动从 arXiv 获取论文
- 提供方便配置的 Web 界面
- PDF 下载和组织
- 记录论文获取活动的日志
- 使用 Markdown 格式美观展示论文
- 错误处理和用户友好的错误消息
- AI驱动的论文问答系统，可以用自然语言查询和分析论文

## 安装

1. 克隆此仓库:
```bash
git clone https://github.com/yourusername/arxiv-paper-fetcher.git
cd arxiv-paper-fetcher
```

2. 安装所需的依赖:
```bash
pip install -r requirements.txt
```

## 配置

### Web 界面

1. 启动 Web 服务器:
```bash
python main.py
```

2. 在浏览器中打开 `http://localhost:8080`

3. 配置您的设置:
   - 选择 arXiv 类别（如 cs.CV 表示计算机视觉）
   - 添加搜索词
   - 设置最大结果数
   - 指定输出目录

4. 点击 "Save Configuration" 保存设置

5. 点击 "Fetch Papers Now" 手动触发论文获取

### 手动配置

您也可以手动编辑 `config.json` 文件:

```json
{
    "categories": [
        "cs.CV"
    ],
    "search_terms": [
        "image restoration",
        "image reconstruction",
        "image denoising",
        "image super-resolution",
        "image inpainting"
    ],
    "max_results": 20,
    "output_dir": "papers"
}
```

## 使用方法

### Web 界面

1. 启动 Web 服务器:
```bash
python main.py
```

2. 访问 `http://localhost:8080` 进入 Web 界面

3. 配置设置:
   - 选择一个或多个 arXiv 类别
   - 添加搜索词（每行一个）
   - 设置最大结果数
   - 指定输出目录

4. 点击 "Fetch Papers Now" 执行:
   - 从 arXiv 获取论文
   - 将它们保存为 Markdown 文件
   - 以格式化视图显示

### AI 聊天功能

1. 点击主页上的 "Ask AI About Papers" 按钮进入聊天界面。

2. 首次使用时，您需要设置 OpenAI API Key:
   - 点击 "API Setup" 按钮
   - 输入您的 OpenAI API 密钥
   - 选择要使用的模型
   - 保存配置

3. 使用聊天界面向 AI 提问:
   - 询问特定研究领域的最新论文
   - 请求论文摘要或解释
   - 比较不同论文的研究方法
   - 获取特定概念的解释

4. AI 会使用 arXiv API 搜索并获取相关论文，帮助您理解和分析研究内容。

### 命令行

要手动获取论文:
```bash
python main.py --fetch
```

要指定端口运行 Web 服务:
```bash
python main.py --port 8888
```

### 论文展示

获取论文后，您将看到:
- 论文标题和作者
- 发布日期
- 摘要要点
- 完整摘要
- PDF 下载链接

## AI 聊天功能设置

要使用 AI 聊天功能，您需要拥有 OpenAI API 密钥。如果您没有，可以在 [OpenAI 官网](https://platform.openai.com/signup) 注册并获取。

### 设置步骤：

1. 启动应用程序
2. 点击首页的 "Ask AI About Papers" 按钮
3. 在聊天页面，点击 "API Setup" 按钮
4. 输入以下信息：
   - OpenAI API 密钥
   - 可选：如果您使用代理或自定义终端，可以设置 Base URL
   - 选择要使用的 AI 模型（默认为 GPT-3.5 Turbo）
5. 点击 "Save Configuration" 保存设置
6. 点击 "Go to Chatbot" 返回聊天界面并开始使用

### 使用提示：

可以向 AI 提出以下类型的问题：
- "查找关于机器学习的最新 arXiv 论文"
- "解释什么是变分自编码器"
- "总结这篇论文的主要观点：[论文ID]"
- "比较 YOLO 和 RCNN 在目标检测中的异同"
- "寻找引用了 Transformer 架构的计算机视觉论文"

AI 将调用 arXiv API 搜索相关论文，分析其内容，并提供有深度的回答。

## 目录结构

```
arxiv-paper-fetcher/
├── main.py                # 主入口文件
├── config.json            # 配置文件
├── requirements.txt       # Python 依赖
├── papers/                # 下载的论文目录
├── src/                   # 源代码目录
│   ├── __init__.py        # 包初始化文件
│   ├── arxiv_fetcher.py   # 主要论文获取逻辑
│   ├── app.py             # Flask Web 应用
│   ├── web_chatbot.py     # AI 聊天功能
│   ├── mcp_client.py      # MCP 客户端
│   ├── static/            # 静态文件目录
│   │   └── css/
│   │       └── style.css  # 自定义样式
│   └── templates/         # HTML 模板
│       ├── index.html     # 主 Web 界面
│       ├── papers.html    # 论文显示模板
│       ├── chatbot.html   # AI 聊天界面
│       ├── setup.html     # API 设置界面
│       ├── error.html     # 错误页面模板
│       └── no_papers.html # 未找到论文模板
└── arxiv_fetcher.log      # 日志文件
```

## 日志

系统将所有活动记录到 `arxiv_fetcher.log` 文件中。您可以查看此文件来监控论文获取过程并排除任何问题。

## 许可证

此项目根据 MIT 许可证授权 - 有关详细信息，请参阅 [LICENSE](LICENSE) 文件。

## 可用的 arXiv 类别

一些常见类别:
- cs.AI (人工智能)
- cs.CL (计算和语言)
- cs.LG (机器学习)
- cs.CV (计算机视觉)
- cs.NE (神经和进化计算)
- stat.ML (机器学习)

有关类别的完整列表，请访问: https://arxiv.org/help/api/user-manual#subject_classifications


## Contributing

Feel free to submit issues and enhancement requests!