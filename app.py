from flask import Flask, render_template_string
import yfinance as yf

# 创建 Flask 应用
app = Flask(__name__)

@app.route('/')
def index():
    # 获取 S&P 500 数据（最近一个月）
    sp500 = yf.download('SPY', period='1mo')

    # 将数据转化为HTML表格
    data_html = sp500.to_html()

    # 渲染 HTML 页面，展示数据
    return render_template_string("""
        <html>
            <head>
                <title>S&P 500 数据</title>
            </head>
            <body>
                <h1>S&P 500 最近一个月的数据</h1>
                <div>{{ data|safe }}</div>
            </body>
        </html>
    """, data=data_html)

if __name__ == '__main__':
    app.run(debug=True)
