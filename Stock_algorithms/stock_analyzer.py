import yfinance
import matplotlib.pyplot as plt

score_for_stock = 0


def main():
        global score_for_stock
        score_for_stock = 0


        symbol = input("Enter stock symbol (like AAPL): ").upper()
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

        Market_Cap = info.get('marketCap')
        Trailing_PE = info.get('trailingPE')
        Current_Ratio = info.get('currentRatio')
        Debt_to_Equity = info.get('debtToEquity')

        print(f"Market Cap: {Market_Cap}")
        print(f"Trailing P/E: {Trailing_PE}")
        print(f"Current Ratio: {Current_Ratio}")
        print(f"Debt to Equity: {Debt_to_Equity}")

        data['Daily Change %'] = data['Close'].pct_change() * 100

        if data.empty:
            print("No  data available")
            return



        plt.figure(figsize=(10,5))
        plt.plot(data['Close'], label='Close Price', color='blue')
        plt.plot(data['MA20'], label='MA 20', color='green')
        plt.plot(data['MA50'], label='50-day MA', color='orange')
        plt.title(f'{symbol} Close Price & 50-day Moving Average')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        plt.grid(True)
        plt.show(block=True)

        check_market_cap(Market_Cap)
        check_trailing_pe(Trailing_PE)
        check_current_ratio(Current_Ratio)
        check_debt_to_equity(Debt_to_Equity)

                
        print(f"\nScore {score_for_stock}/4")
        if score_for_stock > 2:
            print("Buy stock!")
        elif score_for_stock   
        else:
            print("Sell stock")
        


def check_market_cap(value):
    global score_for_stock
    if value is None:
        print("Market Cap: no data")
    elif value > 215292182528:
        score_for_stock += 1


def check_trailing_pe(value):
    global score_for_stock
    if value is None:
        print("Trailing P/E: no data")
    elif value > 26:
        score_for_stock += 1


def check_current_ratio(value):
    global score_for_stock
    if value is None:
        print("Current Ratio: no data")
    elif value > 1:
        score_for_stock += 1


def check_debt_to_equity(value):
    global score_for_stock
    if value is None:
        print("Debt to Equity: no data")
    elif value > 70:
        score_for_stock += 1

main()

