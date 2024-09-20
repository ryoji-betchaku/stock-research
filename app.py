# app.py

from flask import Flask, render_template, request, jsonify
from data_processor import get_company_data, get_company_news # Import the data processing function
import requests
import csv
import xml.etree.ElementTree as ET
import yfinance as yf

app = Flask(__name__)


from flask import Flask, jsonify
import yfinance as yf
import pandas as pd

app = Flask(__name__)

@app.route('/get_stock_data/<ticker>')
def get_stock_data(ticker):
    data = yf.download(ticker, period="2d")
    print(data.head())
    # Check and ensure the DataFrame has 'Date' and 'Close' columns
    # If 'Date' is not a column but an index
    if 'Date' not in data.columns:
        data.reset_index(inplace=True)
    
    data['Date'] = data['Date'].dt.strftime('%Y-%m-%d')  # Format the date
    simplified_data = {
        'Date': data['Date'].tolist(),
        'Close': data['Close'].tolist() if 'Close' in data.columns else []
    }
    return jsonify(simplified_data)


def get_google_news_rss(query, count=10):
    url = f'https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en'
    response = requests.get(url)
    root = ET.fromstring(response.content)
    items = root.findall('.//item')[:count]
    news = [{'title': item.find('title').text, 'link': item.find('link').text} for item in items]
    return news



@app.route('/', methods=['GET', 'POST'])
def home():
    company_name = ''
    company_data = ''
    company_news = ''
    dates = ''
    closing_prices = ''
    dates2 = ''
    closing_prices2 = ''
    ticker = ''
    news = get_google_news_rss('stock+market+tech', 5)
    if request.method == 'POST':

        company_name = request.form['company_name']
        valid_tickers = get_valid_tickers(company_name)
        print("EnteredValue: " + str(company_name))
        # You can add more logic here if needed (e.g., fetching data for the company)
        #print("CompanyName: " + str(company_name))
        if valid_tickers:
            # Process valid ticker
            # For example, fetching data using yfinance
            # stock_info = yf.Ticker(submitted_ticker).info
            # return render_template('info.html', stock_info=stock_info)
            pass
        else:
            # Handle invalid ticker
            # For example, redirect back to form with an error message
            return render_template('index.html', error="Invalid ticker symbol")
        
        ticker = yf.Ticker(company_name)
        hist = ticker.history(period="3mo")
        sp500 = yf.Ticker("^GSPC")
        hist_sp500 = sp500.history(period="3mo")
        # Process data as needed, e.g., converting to JSON, etc.
        dates = hist.index.strftime('%Y-%m-%d').tolist()
        closing_prices = hist['Close'].tolist()

        dates2 = hist_sp500.index.strftime('%Y-%m-%d').tolist()
        closing_prices2 = hist_sp500['Close'].tolist()

        company_data = get_company_data(company_name)
        company_news = get_company_news(company_name)

       
    return render_template('index.html', company_data=company_data, company_news=company_news, news=news, dates=dates, prices=closing_prices, dates2=dates2, prices2=closing_prices2, ticker=company_name)




def load_csv(file_path):
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)
    

stock_data = load_csv('symbols.csv')
#print(stock_data[0])  # Check the first row to ensure it's loaded correctly

@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    search = request.args.get('q', '').upper()

    suggestions = [stock for stock in stock_data if stock['symbol'].upper().startswith(search)]
    
    return jsonify(suggestions[:10])  # Limit the number of suggestions


# Assuming this function returns a list of valid ticker symbols
def get_valid_tickers(search):
    return any(stock['symbol'] == search for stock in stock_data)


# Not using this as not scalable

# @app.route('/autocomplete', methods=['GET'])
# def autocomplete():
#     query = request.args.get('q', '')
#     print('test')
#     # Use Alpha Vantage API to get stock symbol suggestions
#     # Note: Replace 'YOUR_API_KEY' with your actual Alpha Vantage API key
#     response = requests.get(f'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={query}&apikey=')
#     suggestions = response.json().get('bestMatches', [])
   
#     print([{'symbol': match['1. symbol'], 'name': match['2. name']} for match in suggestions])

#     return jsonify([{'symbol': match['1. symbol'], 'name': match['2. name']} for match in suggestions])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
    
#https://www.nyse.com/publicdocs/nyse/markets/nyse/NYSE_and_NYSE_MKT_Trading_Units_Daily_File.xls