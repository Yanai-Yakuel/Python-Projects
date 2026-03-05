import yfinance
import matplotlib.pyplot as plt
import json
import os
import datetime

score_for_stock = 0
SCORES_FILE = "stock_algorithms/stock_scores.json"

##############JSON_FILE_SAVE###################
def handle_scores(symbol, score):
    os.makedirs("stock_algorithms", exist_ok=True)
    if os.path.exists(SCORES_FILE):
        with open(SCORES_FILE, 'r') as f:
            scores = json.load(f)
    else:
        scores = {}

    scores[symbol] = {
        "score": score,
        "date": str(datetime.date.today())
    }

    with open(SCORES_FILE, 'w') as f:
        json.dump(scores, f, indent=4)

    print(f"Saved! {symbol}: {score}/9")
###################################################


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
        return3

    if data.empty:
        print("No data available")
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
############PRAPH ############################
    plt.figure(figsize=(10, 5))
    plt.plot(data['Close'], label='Close Price', color='blue')
    plt.plot(data['MA20'], label='MA 20', color='green')
    plt.plot(data['MA50'], label='50-day MA', color='orange')
    plt.title(f'{symbol} Close Price & Moving Averages')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)
    plt.show(block=True)


##############call_functions###############
    check_market_cap(Market_Cap)
    check_trailing_pe(Trailing_PE)
    check_current_ratio(Current_Ratio)
    check_debt_to_equity(Debt_to_Equity)
    check_revenue_growth(Revenue_Growth)
    check_profit_margin(Profit_Margin)
    check_eps(EPS)
    check_dividend_yield(Dividend_Yield)
    check_moving(data)

    print(f"\nScore {score_for_stock}/9")
    if score_for_stock > 5:
        print("Buy stock!")
    elif score_for_stock == 5:
        print("Hold")
    else:
        print("Sell stock")

    handle_scores(symbol, score_for_stock)

################calc_functions######################

def check_market_cap(value):
    global score_for_stock
    if value is None:
        print("Market Cap: no data")
    elif value > 10_000_000_000:
        score_for_stock += 1


def check_trailing_pe(value):
    global score_for_stock
    if value is None:
        print("Trailing P/E: no data")
    elif 0 < value < 25:
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
    elif value < 50:
        score_for_stock += 1


def check_revenue_growth(value):
    global score_for_stock
    if value is None:
        print("Revenue Growth: no data")
    elif value > 0.1:
        score_for_stock += 1


def check_profit_margin(value):
    global score_for_stock
    if value is None:
        print("Profit Margin: no data")
    elif value > 0.15:
        score_for_stock += 1


def check_eps(value):
    global score_for_stock
    if value is None:
        print("EPS: no data")
    elif value > 0:
        score_for_stock += 1


def check_dividend_yield(value):
    global score_for_stock
    if value is None:
        print("Dividend Yield: no data")
    elif value > 0.02:
        score_for_stock += 1


def check_moving(data):
    global score_for_stock
    if data['MA20'].iloc[-1] > data['MA50'].iloc[-1]:
        score_for_stock += 1

#########################################################

while True:
    main()
    a = input("Do you want to analyze again? Y/N: ").upper()
    if a != "Y":
        print("Thanks for using the program!")
        break