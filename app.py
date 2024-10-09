from flask import Flask, render_template
import yfinance as yf
import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt
import os

# 创建Flask应用
app = Flask(__name__)

@app.route('/')
def index():
    # 获取S&P 500数据
    sp500 = yf.download('SPY', start='2020-01-01', end='2024-10-01')

    # 将数据分为训练集和测试集
    train_data = sp500.loc[:'2024-01-01']
    test_data = sp500.loc['2024-01-02':]

    # 将训练集数据格式调整为Prophet模型要求的格式
    train_data_prophet = train_data.reset_index().rename(columns={'Date': 'ds', 'Close': 'y'})
    test_data_prophet = test_data.reset_index().rename(columns={'Date': 'ds'})

    # 创建并训练Prophet模型
    model_prophet = Prophet()
    model_prophet.fit(train_data_prophet)

    # 预测测试集期间的价格
    future = model_prophet.make_future_dataframe(periods=len(test_data), freq='D')
    forecast = model_prophet.predict(future)

    # 将预测结果与测试集数据合并
    forecast_test = pd.merge(test_data_prophet, forecast[['ds', 'yhat']], on='ds', how='left')

    # 保存预测图像
    plt.figure(figsize=(10, 6))
    plt.plot(train_data.index, train_data['Close'], label='训练数据', color='blue')
    plt.plot(test_data.index, test_data['Close'], label='实际价格', color='green')
    plt.plot(forecast_test['ds'], forecast_test['yhat'], label='预测价格 (Prophet)', color='red')
    plt.title('S&P 500 实际 vs 预测价格 (Prophet)')
    plt.xlabel('日期')
    plt.ylabel('价格')
    plt.legend()

    # 保存图像到static目录下
    image_path = os.path.join('static', 'stock_price.png')
    plt.savefig(image_path)
    
    # 渲染index.html页面
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
