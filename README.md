# Emby 工具集

本项目包含了一系列用于 Emby 的工具，主要包括一个信息报告脚本和一个自定义CSS样式文件。

## 目录结构

```
.
├── emby_css/
│   └── custom.css
├── emby_reporter/
│   ├── config.ini
│   ├── main.py
│   └── requirements.txt
└── README.md
```

---

## 1. Emby 信息报告器 (`emby_reporter`)

这是一个 Python 脚本，可以连接到您的 Emby 服务器，获取服务器运行状态和媒体库内容数量，并生成一份适配于 Telegram 的 Markdown 格式报告。

### 使用方法

**a. 配置服务器信息**

打开 `emby_reporter/config.ini` 文件，填入您的 Emby 服务器地址和 API 密钥：

```ini
[emby]
url = http://your-emby-server-address:8096
api_key = YOUR_API_KEY
```

**b. 安装依赖**

在您的终端中，进入 `emby_reporter` 目录，然后运行以下命令安装所需的 Python 库：

```bash
cd emby_reporter
pip install -r requirements.txt
```

**c. 运行脚本**

完成配置和安装后，运行主脚本：

```bash
python main.py
```

脚本将在控制台输出格式化好的报告，您可以直接复制粘贴到 Telegram 中。

---

## 2. Emby 自定义CSS (`emby_css`)

这是一个用于美化 Emby Web 界面的自定义 CSS 文件。它主要优化了字体的显示，并解决了长标题在界面上无法完整显示并换行的问题。

### 使用方法

**a. 找到 Emby 的自定义 CSS 设置**

1.  登录您的 Emby 服务器，进入“控制台”。
2.  在左侧菜单中找到“Emby server - 通用”选项。
3.  在“自定义CSS”或“Custom CSS”文本框中，您可以粘贴 CSS 代码。

**b. 应用 CSS**

将 `emby_css/custom.css` 文件中的**全部内容**复制并粘贴到 Emby 的自定义 CSS 输入框中，然后保存设置。

刷新 Emby 页面即可看到效果。

### 主要功能

*   **字体优化**：引入了“霞鹜文楷”等字体，优化了字幕和标题的显示效果。
*   **长标题换行**：强制使媒体库中的长标题能够换行显示，避免了标题被截断的问题。
*   **可配置**：您可以直接在 CSS 文件中修改字体大小、颜色等参数，以满足您的个性化需求。
