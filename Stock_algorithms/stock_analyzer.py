import yfinance
import matplotlib.pyplot as plt

def main():
    symbol = input("Enter stock symbol (e.g., AAPL): ").upper()
    stock = yfinance.Ticker(symbol)

    info = stock.info  
    
    try:
        data = stock.history(period="1y", timeout=30)
    except Exception as e:
        print("no data found")
        return
    

    data['MA20'] = data['Close'].rolling(window=20, min_periods=1).mean()
    data['MA50'] = data['Close'].rolling(window=50, min_periods=1).mean()

    print(f"\nFinancial info for {symbol}:")
    print(f"Market Cap: {info.get('marketCap')}")
    print(f"Trailing P/E: {info.get('trailingPE')}")
    print(f"Forward P/E: {info.get('forwardPE')}")
    print(f"Current Ratio: {info.get('currentRatio')}")
    print(f"Debt to Equity: {info.get('debtToEquity')}")
    print(f"Average daily change: {data['Daily Change %'].mean():.2f}%")




    plt.figure(figsize=(10,5))
    plt.plot(data['Close'], label='Close Price', color='blue')
    plt.plot(data['MA20'], label='MA 20', color='green')
    plt.plot(data['MA50'], label='50-day MA', color='orange')
    plt.title(f'{symbol} Close Price & 50-day Moving Average')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)
    plt.show()

main()
