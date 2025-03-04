# 抖音主页爬虫API

这是一个基于Flask的Web API服务，用于爬取抖音用户主页的信息。

## 功能特点

- 支持抓取抖音用户主页的视频列表
- 获取视频标题、点赞数等信息
- 支持自定义抓取数量
- 使用Selenium进行动态页面抓取
- 实现反爬虫策略

## 技术栈

- Python 3.x
- Flask
- Selenium
- BeautifulSoup4
- Chrome WebDriver

## 安装说明

1. 克隆项目到本地：
   ```bash
   git clone [你的仓库URL]
   cd pachong
   ```

2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

3. 确保已安装Chrome浏览器和对应版本的ChromeDriver

## 使用方法

1. 启动服务器：
   ```bash
   python app.py
   ```

2. 访问API：
   ```
   GET http://localhost:5000/api/douyin/homepage?url=[抖音主页URL]&count=[获取数量]
   ```

   参数说明：
   - url: 抖音用户主页URL（必需）
   - count: 要获取的视频数量（可选，默认10）

## 部署说明

本项目可以部署在Railway平台上：

1. 在Railway平台上关联GitHub仓库
2. 配置环境变量（如需要）
3. Railway会自动检测requirements.txt并安装依赖
4. 需要在Railway的配置中添加Chrome和ChromeDriver的安装命令

## 注意事项

- 请遵守抖音的使用条款和政策
- 建议适当限制请求频率
- 部署时需要确保环境中已正确配置Chrome和ChromeDriver

## 许可证

MIT License