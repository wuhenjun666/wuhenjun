from flask import Flask, request, jsonify
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import json
import time

app = Flask(__name__)
# 配置CORS，允许所有来源的请求
CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "OPTIONS"]}})

def get_homepage_info(url, count):
    # 配置 Chrome 选项，添加反爬策略参数
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("window-size=1920,1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    # 初始化 WebDriver
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # 访问目标网址
        driver.get(url)

        # 等待页面渲染
        time.sleep(5)

        # 获取页面源码
        html_content = driver.page_source

        # 解析 HTML
        soup = BeautifulSoup(html_content, "html.parser")

        # 查找所有符合条件的标签
        li_tags = soup.find_all("li", class_="wqW3g_Kl WPzYSlFQ OguQAD1e")
        name_tags = soup.find("span", class_="arnSiSbK")
        id_tags = soup.find("span", class_="OcCvtZ2a")

        if not all([li_tags, name_tags, id_tags]):
            return {"error": "无法找到所需的页面元素"}

        data = []
        for i, li in enumerate(li_tags):
            if i >= (count if count else 10):
                break

            item = {}
            lines = id_tags.text.splitlines()
            last_line = lines[-1]
            item["name"] = name_tags.text
            item["id"] = last_line[4:]

            a_tag = li.find("a")
            span_tag = li.find("span", class_="BgCg_ebQ")
            p_tag = li.find("p", class_="eJFBAbdI H4IE9Xgd")

            if a_tag and a_tag.has_attr("href"):
                a_href = a_tag["href"].rstrip('/')
                parts = a_href.split('/')
                item["url"] = "https://www.douyin.com/" + "/".join(parts[-2:])

            item["like"] = span_tag.text if span_tag else None
            item["title"] = p_tag.text if p_tag else None

            data.append(item)

        return data

    except Exception as e:
        return {"error": str(e)}
    finally:
        driver.quit()

@app.route('/api/douyin/homepage', methods=['GET'])
def homepage_info():
    url = request.args.get('url')
    count = request.args.get('count', type=int, default=10)

    if not url:
        return jsonify({"error": "URL参数是必需的"}), 400

    if not url.startswith('https://www.douyin.com/'):
        return jsonify({"error": "只支持抖音网址"}), 400

    try:
        data = get_homepage_info(url, count)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)