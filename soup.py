import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
import yfinance as yf
import random

stock_list = ['AAPL', 'MSFT', 'GOOGL', 'AMZN']

# Randomly pick 5 unique stocks
#selected_stocks = random.sample(stock_list, 5)

# Function to fetch stock data
def get_stock_info(stock):
    ticker = yf.Ticker(stock)
    hist = ticker.history(period="1mo")
    info = ticker.info
    #print(info)
    return {
        "Name": info.get('longName'),
        "Symbol": stock,
        "P/E Ratio": info.get('trailingPE'),
        "EPS": info.get('trailingEps'),
        "FreeCashflow": info.get('freeCashflow'),
        "OperatingMargins": info.get('operatingMargins'),
        "PriceToBook": info.get('priceToBook'),
        "revenueGrowth": info.get('revenueGrowth'),
        "Beta": info.get('beta'),
        "52 Week Change": info.get('52WeekChange')
    }


def get_news_sentiment(stock):
    url = f'https://news.google.com/search?q={stock}&hl=en-US&gl=US&ceid=US:en'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract news articles - adjust the selector as needed
    articles = soup.select('article')
    total_sentiment = 0

    for article in articles:
        # Extract text from each article
        text = article.get_text()
        # Perform sentiment analysis
        print(text)
        analysis = TextBlob(text)
        total_sentiment += analysis.sentiment.polarity

    # Calculate average sentiment
    average_sentiment = total_sentiment / len(articles) if articles else 0
    return average_sentiment

# URL of Yahoo Finance's most active stocks page
url = 'https://finance.yahoo.com/most-active'

# Fetch the page content
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Find the table or the specific part of the page where the most active stocks are listed
# The specific parsing code will depend on the structure of the Yahoo Finance page
# Typically, you would look for a <table> element or a list of <div> elements containing the stock data

# Example (this will need to be adjusted based on the actual page structure):
most_active_stocks = soup.find_all('tr', {'class': 'simpTblRow'})[:10]  # Assuming the data is in table rows

for stock in most_active_stocks:
    # Extract the relevant data from each stock element
    # This will depend on the HTML structure
    # Example: stock.find('td', {'class': 'someClassName'}).get_text()
    print(stock)
    pass

# Example usage
#sentiment = get_news_sentiment('OpenAI')
#print(f"Sentiment for MSFT: {sentiment}")
# Fetch and display stock data
#info = get_stock_info('MSFT')
#print(info)

