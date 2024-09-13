import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Sample data generation function
def generate_sample_data(start_date, end_date):
    dates = pd.date_range(start_date, end_date)
    prices = np.random.randn(len(dates)).cumsum() + 100  # Random walk
    return pd.DataFrame({'Date': dates, 'Price': prices}).set_index('Date')

# Simple Moving Average strategy
def moving_average_strategy(data, short_window=40, long_window=100):
    signals = pd.DataFrame(index=data.index)
    signals['Price'] = data['Price']
    signals['Short_MA'] = data['Price'].rolling(window=short_window, min_periods=1).mean()
    signals['Long_MA'] = data['Price'].rolling(window=long_window, min_periods=1).mean()
    signals['Signal'] = 0
    signals['Signal'][short_window:] = np.where(signals['Short_MA'][short_window:] > signals['Long_MA'][short_window:], 1, 0)
    signals['Position'] = signals['Signal'].diff()
    return signals

# Backtesting the strategy
def backtest_strategy(data, signals):
    initial_capital = 10000
    signals['Position'].fillna(0, inplace=True)
    signals['Holdings'] = signals['Position'].cumsum() * data['Price']
    signals['Cash'] = initial_capital - (signals['Position'] * data['Price']).cumsum()
    signals['Total'] = signals['Cash'] + signals['Holdings']
    return signals

if __name__ == "__main__":
    # Generate sample data
    data = generate_sample_data('2023-01-01', '2024-01-01')

    # Apply trading strategy
    signals = moving_average_strategy(data)
    results = backtest_strategy(data, signals)

    # Plotting results
    plt.figure(figsize=(12, 8))
    plt.subplot(3, 1, 1)
    plt.plot(data.index, data['Price'], label='Price')
    plt.plot(signals.index, signals['Short_MA'], label='Short MA')
    plt.plot(signals.index, signals['Long_MA'], label='Long MA')
    plt.title('Stock Price and Moving Averages')
    plt.legend()

    plt.subplot(3, 1, 2)
    plt.plot(signals.index, signals['Holdings'], label='Holdings')
    plt.title('Portfolio Holdings')
    plt.legend()

    plt.subplot(3, 1, 3)
    plt.plot(signals.index, signals['Total'], label='Total Portfolio Value')
    plt.title('Total Portfolio Value')
    plt.legend()

    plt.tight_layout()
    plt.show()

