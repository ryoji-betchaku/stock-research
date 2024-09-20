# data_processor.py

import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
import yfinance as yf
import random
import json

stock_list = ['AAPL', 'MSFT', 'GOOGL', 'AMZN']

# Randomly pick 5 unique stocks
#selected_stocks = random.sample(stock_list, 5)

# Function to fetch stock data
def get_stock_info(stock):
    ticker = yf.Ticker(stock)
    hist = ticker.history(period="1mo")
    info = ticker.info
    hist = ticker.history(period="1mo")
    print(info)
    #print(ticker.income_stmt)
    #print(str(ticker.news[0].get('title')) +" - "+ str(ticker.news[1].get('link')))
   
    return {
        "Name": info.get('longName'),
        "Symbol": stock,
        "CurrentPrice": info.get('currentPrice'),
        "TargetHighPrice": info.get('targetHighPrice'),
        "TargetLowPrice": info.get('targetLowPrice'),
        "TargetMeanPrice": info.get('targetMeanPrice'),
        "*Sentiment": get_news_sentiment(str(stock)),
        "P/E Ratio": info.get('trailingPE'),
        "EPS": info.get('trailingEps'),
        "Short Ratio": info.get('shortRatio'),
        "Free Cashflow": info.get('freeCashflow'),
        "Operating Margins": info.get('operatingMargins'),
        "PriceToBook": info.get('priceToBook'),
        "Revenue Growth": info.get('revenueGrowth'),
        "Beta": info.get('beta'),
        "52 Week Change": info.get('52WeekChange'),
        "Sector": info.get('sector'),
        "Industry": info.get('industry'),
        "Website": info.get('website'),
        "Key People": info.get('companyOfficers')[0].get("name"),
        "Business Summary": info.get('longBusinessSummary'),
       
    }


def get_news_sentiment(stock):
    url = f'https://news.google.com/search?q={stock}%20STOCK&hl=en-US&gl=US&ceid=US:en'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract news articles - adjust the selector as needed
    articles = soup.select('article')
    total_sentiment = 0

    for article in articles:
        # Extract text from each article
        text = article.get_text()
        # Perform sentiment analysis
        analysis = TextBlob(text)
        total_sentiment += analysis.sentiment.polarity

    # Calculate average sentiment
    average_sentiment = total_sentiment / len(articles) if articles else 0
    return average_sentiment

# Example usage
#sentiment = get_news_sentiment('OpenAI')
#print(f"Sentiment for MSFT: {sentiment}")
# Fetch and display stock data
#info = get_stock_info('MSFT')
#print(info)

def parse_json_to_table(json_data):
    # Assuming json_data is a string in JSON format
    data_dict = json.loads(json_data)

    table_data = []
    for key, value in data_dict.items():
        row = {'key': key, 'value': value}
        table_data.append(row)

    return table_data



def get_company_data(company_name):

    info = get_stock_info(str(company_name))
     # Convert the stock info to JSON (it's already a dictionary)

    json_data = json.dumps(info, indent=2, default=str)  # 'default=str' helps avoid serialization errors

    table_data = parse_json_to_table(json_data)
    
    return table_data

def get_company_news(company_name):

    ticker = yf.Ticker(company_name)
    #info = str(ticker.news[0].get('title')) +" - "+ str(ticker.news[1].get('link'))

    info = ticker.news
    processed_news = [
        {'title': item['title'], 'link': item['link']} for item in info
    ]
    return processed_news
