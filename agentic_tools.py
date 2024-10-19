proxy = "proxy.us.ibm.com:8080"

import requests
from bs4 import BeautifulSoup

def search(query):
    url = 'https://duckduckgo.com/'
    params = {
        'q': query
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }

    proxies = {
        'http': proxy,
        'https': proxy
    }
    
    response = requests.get(url, params=params, headers=headers, proxies=proxies)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []
        for a in soup.find_all('Result'):
            title = a.get_text()
            href = a['href']
            results.append({'title': title, 'href': href})
        return results
    else:
        return f"Error: {response.status_code}"

def query_duckduckgo(query):
    url = 'https://api.duckduckgo.com/'
    params = {
        'q': query,
        'format': 'json',
        'pretty': 1
    }
    headers = {
        'User-Agent': 'YourAppName/1.0 (https://yourapp.example; your-email@example.com)'
    }

    session = requests.Session()
    session.headers.update(headers)

    if proxy:
        session.proxies = {
            'http': proxy,
            'https': proxy
        }

    response = session.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        print(data)
        return data.get('Result', [])
    else:
        return f"Error: {response.status_code}"
    
from duckduckgo_search import DDGS

def search_duckduckgo(query):
    results = DDGS(proxy=proxy).text(query)
    return results
    
import yfinance as yf

def get_stock_data(ticker, period='1mo', interval='1d'):
    session = requests.Session()
    session.proxies = {
        'http': proxy,
        'https': proxy
    }

    stock = yf.Ticker(ticker, session=session)
    data = stock.history(period=period, interval=interval)
    return data

import requests

def get_hko_weather():
    url = 'https://data.weather.gov.hk/weatherAPI/opendata/weather.php'
    params = {
        'dataType': 'rhrread',  # Real-time weather data
        'lang': 'en'            # Language: 'en' for English
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        temperature = data['temperature']['data'][0]['value']
        humidity = data['humidity']['data'][0]['value']
        weather_desc = data['icon'][0]  # Weather icon code
        return {
            'temperature': temperature,
            'humidity': humidity,
            'weather_description': weather_desc
        }
    else:
        return f"Error: {response.status_code} - {response.text}"
    
import requests

def get_global_weather(latitude, longitude):
    url = 'https://api.open-meteo.com/v1/forecast'
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'current_weather': True
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        current_weather = data['current_weather']
        return {
            'temperature': current_weather['temperature'],
            'windspeed': current_weather['windspeed'],
            'weather_code': current_weather['weathercode']
        }
    else:
        return f"Error: {response.status_code} - {response.text}"
    
import arxiv

def search_arxiv(query, max_results=5):
    client = arxiv.Client()
    
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance,
    )
    
    results = []
    for result in client.results(search):
        results.append({
            'title': result.title,
            'authors': [author.name for author in result.authors],
            'summary': result.summary,
            'url': result.entry_id
        })
    
    return results

import wikipediaapi
import requests

def query_wikipedia(title):
    wiki = wikipediaapi.Wikipedia('watsonx',proxies={'http': proxy,'https':proxy})
    page = wiki.page(title)

    if page.exists():
        return {
            "title": page.title,
            "summary": page.summary,
            "url": page.fullurl
        }
    else:
        return "Page not found."