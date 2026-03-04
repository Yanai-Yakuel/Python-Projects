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
        Revenue_Growth = info.get('revenueGrowth')
        Profit_Margin = info.get('profitMargins')
        EPS = info.get('trailingEps')
        Dividend_Yield = info.get('dividendYield')

        print(f"Revenue Growth: {Revenue_Growth}")
        print(f"Profit Margin: {Profit_Margin}")
        print(f"EPS: {EPS}")
        print(f"Dividend Yield: {Dividend_Yield}")
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
        check_revenue_growth(Revenue_Growth)
        check_profit_margin(Profit_Margin)
        check_eps(EPS)
        check_dividend_yield(Dividend_Yield)

        print(f"\nScore {score_for_stock}/8")
        if score_for_stock > 4:
            print("Buy stock!")
        elif score_for_stock == 4:
            print("hold")
        else:
            print("Sell stock")


def check_market_cap(value):
    global score_for_stock
    if value is None:      #מרקט קאפ
        print("Market Cap: no data")
    elif value > 215292182528:
        score_for_stock += 1


def check_trailing_pe(value):
    global score_for_stock
    if value is None: ## PE 
        print("Trailing P/E: no data")
    elif value > 26:
        score_for_stock += 1


def check_current_ratio(value):
    global score_for_stock # checks if company can cover short-term debts
    if value is None: 
        print("Current Ratio: no data")
    elif value > 1:
        score_for_stock += 1


def check_debt_to_equity(value):
    global score_for_stock
    if value is None:  # checks company debt level
        print("Debt to Equity: no data")
    elif value > 70:
        score_for_stock += 1

def check_revenue_growth(value):
    global score_for_stock
    if value is None:
        print("Revenue Growth: no data")
    elif value > 0.1:  # צמיחה מעל 10%
        score_for_stock += 1

def check_profit_margin(value):
    global score_for_stock
    if value is None:
        print("Profit Margin: no data")
    elif value > 0.15:  # מרווח רווח מעל 15%
        score_for_stock += 1

def check_eps(value):
    global score_for_stock
    if value is None:
        print("EPS: no data")
    elif value > 0:  # רווח חיובי למניה
        score_for_stock += 1

def check_dividend_yield(value):
    global score_for_stock
    if value is None:
        print("Dividend Yield: no data")
    elif value > 0.02:  # תשואת דיבידנד מעל 2%
        score_for_stock += 1

main()

