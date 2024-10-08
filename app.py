import yfinance as yf
import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt

# Fetch S&P 500 data
sp500 = yf.download('SPY', start='2020-01-01', end='2024-10-01')

# Split the data into training and test sets
train_data = sp500.loc[:'2024-01-01']  # Training data (2020 to the beginning of 2024)
test_data = sp500.loc['2024-01-02':]   # Test data (after the beginning of 2024)

# Prepare the data format required by the Prophet model
train_data_prophet = train_data.reset_index().rename(columns={'Date': 'ds', 'Close': 'y'})
test_data_prophet = test_data.reset_index().rename(columns={'Date': 'ds'})

# Create and train the Prophet model
model_prophet = Prophet()
model_prophet.fit(train_data_prophet)

# Forecast future prices for the test data period
future = model_prophet.make_future_dataframe(periods=len(test_data), freq='D')
forecast = model_prophet.predict(future)

# Merge the forecast results with the test data to align timestamps
forecast_test = pd.merge(test_data_prophet, forecast[['ds', 'yhat']], on='ds', how='left')

# Visualize actual and predicted prices
plt.figure(figsize=(10, 6))
plt.plot(train_data.index, train_data['Close'], label='Training Data', color='blue')
plt.plot(test_data.index, test_data['Close'], label='Actual Prices', color='green')
plt.plot(forecast_test['ds'], forecast_test['yhat'], label='Predicted Prices (Prophet)', color='red')
plt.title('S&P 500 Actual vs Predicted Prices (Prophet)')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.show()

# Optional: Visualize trends, seasonal components, etc.
model_prophet.plot_components(forecast)
plt.show()
