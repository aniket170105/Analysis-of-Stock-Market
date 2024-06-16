import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import numpy as np
import re
from newspaper import Article
import os
from groq import Groq
import time


def getNewsLinkGoogle(ticker_name):
    search_url = "https://www.google.com/search?q=yahoo+finance+{}&tbm=nws&prmd=nivsbmtz&source=lnt&tbs=qdr:d&sa=X".format(ticker_name)
    r = requests.get(search_url)                        ###################Think how can we add second page result
    soup = BeautifulSoup(r.text, 'html.parser')
    atags = soup.find_all('a')
    hrefs = [link['href'] for link in atags]
    return strip_unwanted_urls(hrefs)

def strip_unwanted_urls(urls):
    exclude_list = ['maps', 'policies', 'preferences', 'accounts', 'support','google']
    val = []
    for url in urls:
        if 'https://' in url and not any(exclude_word in url for exclude_word in exclude_list):
            res = re.findall(r'(https?://\S+)', url)[0].split('&')[0]
            val.append(res)
    return list(set(val))

def getNewsLinkFinviz(ticker_name):
    url = f'https://finviz.com/quote.ashx?t={ticker_name}'
    req = Request(url=url, headers={'user-agent': 'my-app'})
    response = urlopen(req)
    html = BeautifulSoup(response, features='html.parser')
    news_table = html.find(id='news-table')
    news_link = []
    for row in news_table.findAll('tr'):
        # title = row.a.text
        # news_link.append([date, time, title])
        # news_link.append()
        temp = []
        for x in row.find_all('a', href=True):
            temp.append(x['href'])
        news_link.append(temp)
    return news_link[:15]

def extract_real_number(text):
    # Define a regex pattern for a real number between 0 and 1
    pattern = r'\b0?\.\d+\b'

    # Search for the pattern in the text
    match = re.search(pattern, text)

    if match:
        # Convert the matched string to a float and return
        return float(match.group())
    else:
        # Return None if no match is found
        return None

def dosingleSentiment(text):
    client = Groq(
                api_key='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',
            )
    prompt = f'''Do the sentiment analysis of this article and give out a real value between 0 and 1, 0 showing negative sentiment and 1 showing positive sentiment. Only output real value between 0 and 1.
    Article:
    {text}
    '''
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "you are a helpful assistant."
            },
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama3-70b-8192",
    )
    print(chat_completion.choices[0].message.content)
    return extract_real_number(chat_completion.choices[0].message.content)

def doSentimentAnalysis(news_link):
    analysis_value = []
    for x in news_link:
        article = Article(x)
        article.download()
        article.parse()
        analysis_value.append(dosingleSentiment(article.text))
        time.sleep(5)   ### Working Fine
    return np.array(analysis_value).mean()

def appSentiment(ticker_name):
    urls = getNewsLinkGoogle(ticker_name=ticker_name)
    return doSentimentAnalysis(urls)



###Testing Done Working Fine
## Ready to integrate in Website
# print(appSentiment('AMZN'))