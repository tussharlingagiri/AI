import requests
import json
import pandas as pd

# function to get historical stock data
def get_stock_data(stock_symbol):
    api_key = 'YOUR_API_KEY'
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&market=LSE&symbol={stock_symbol}&apikey={api_key}'
    response = requests.get(url)
    if response.status_code != 200:
        return "Error: Invalid stock symbol or API key"
    data = json.loads(response.text)
    return data

# function to analyze stock data
def analyze_stock(stock_data):
    if type(stock_data) == str:
      return stock_data
    # convert data to pandas dataframe
    df = pd.DataFrame(stock_data['Time Series (Daily)']).T
    # calculate 50-day moving average
    df['50ma'] = df['4. close'].astype(float).rolling(window=50).mean()
    # calculate 200-day moving average
    df['200ma'] = df['4. close'].astype(float).rolling(window=200).mean()
    # check if stock is currently trading above its 50-day moving average
    if float(df.iloc[-1]['4. close']) > float(df.iloc[-1]['50ma']):
        # check if stock is currently trading above its 200-day moving average
        if float(df.iloc[-1]['4. close']) > float(df.iloc[-1]['200ma']):
            return 'Buy'
        else:
            return 'Hold'
    else:
        return 'Sell'

# list of UK stock symbols
stock_symbols = ['BP.L', 'GSK.L', 'HSBA.L', 'BARC.L', 'VOD.L']
# lists to store stocks to buy, sell, and hold
stocks_to_buy = []
stocks_to_sell = []
stocks_to_hold = []

# iterate through the list of stock symbols
for stock_symbol in stock_symbols:
    stock_data = get_stock_data(stock_symbol)
    analysis = analyze_stock(stock_data)
    if analysis == "Buy":
        stocks_to_buy.append(stock_symbol)
    elif analysis == "Sell":
        stocks_to_sell.append(stock_symbol)
    elif analysis == "Hold":
        stocks_to_hold.append(stock_symbol)

# print out the lists of stocks to buy, sell, and hold
print("Stocks to buy:", stocks_to_buy)
print("Stocks to sell:", stocks_to_sell)
print("Stocks to hold:", stocks_to_hold)
