from django.shortcuts import render
import requests
import re
import multiprocessing
from functools import partial
from bs4 import BeautifulSoup
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from lxml import etree, html
import time
# Create your views here.
def getHTMLdocument(url): # for retrying if connection error due to timeout
    page = ''
    while page == '':
        try:
            page = requests.get(url)
            break
        except:
            print("Connection refused by the server..")
            print("Let me sleep for 5 seconds")
            print("ZZzzzz...")
            time.sleep(5)
            print("Was a nice sleep, now let me continue...")
            continue
    return page.text

def quotes_page(session, url):
    content = getHTMLdocument(url)
    soup = BeautifulSoup(content, 'html.parser') 
    mydivs = soup.find_all("a", {"class": "title"})
    return mydivs

def get_author(url):
    response = requests.get(url)
    html_content = response.content
    tree = html.fromstring(html_content)
    link_element = tree.xpath("""//*[@id="fly-scroll-container"]/div[1]/div/ul/li[2]/div/div[1]/a""")[0]
    link_text = link_element.text_content()
    print(link_text)
    return link_text

author_list = []
context = {}
popular_author = {}


def author(letter, page):
    author_list = []
    popular_author = {}
    context = {}

    try:
        URL = f"https://www.azquotes.com/quotes/authors/{letter}/" if page == 1 else f"https://www.azquotes.com/quotes/authors/{letter}/{page}"
        HEADERS = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'
        }
        webpage = requests.get(URL, headers=HEADERS)
        soup = BeautifulSoup(webpage.content, "html.parser")
        dom = etree.HTML(str(soup))

        for i in range(1, 101):
            link = dom.xpath(f'//*[@id="content"]/div/div[1]/div/section/table/tbody/tr[{i}]/td[1]/a/@href')[0]
            url = "https://www.azquotes.com" + link
            author_url='persona?query='+link[8:]
            author_name = dom.xpath(f'//*[@id="content"]/div/div[1]/div/section/table/tbody/tr[{i}]/td[1]/a/text()')[0]
            author_dob = dom.xpath(f'//*[@id="content"]/div/div[1]/div/section/table/tbody/tr[{i}]/td[3]/text()')[0].strip()

            author_list.append([author_name, author_url, author_dob])
            context[author_name] = [author_url, author_dob]

        if page == 1:
            for num in range(1, 7):
                popular_author_name = dom.xpath(f'//*[@id="content"]/div/div[1]/div/section/div[1]/ul/li[{num}]/div/a/text()')[0].strip()
                popular_author_url = dom.xpath(f'//*[@id="content"]/div/div[1]/div/section/div[1]/ul/li[{num}]/div/a/@href')[0].strip()
                popular_author[popular_author_name] = popular_author_url
    except:
        pass

    return context, popular_author


def author_page(request):
    page = request.GET.get("page", 1)
    page = int(page)
    letter = request.GET.get("letter", 1)
    
    page_nums = [f'/authors?letter=a&page={i}' for i in range(1,26)]

    context, popular_author = author(letter, page)

    return render(request, 'author.html', {
        'context': context,
        'popular_person': popular_author,
        'letter': letter[0].upper(),
        'page_nums': page_nums
    })
def quotes_page(url):
    content = getHTMLdocument(url)
    soup = BeautifulSoup(content, 'html.parser')
    mydivs = soup.find_all("a", {"class": "title"})
    return [quote.getText() for quote in mydivs]

def get_author(url):
    response = requests.get(url)
    html_content = response.content
    tree = html.fromstring(html_content)
    link_element = tree.xpath("""//*[@id="fly-scroll-container"]/div[1]/div/ul/li[2]/div/div[1]/a""")[0]
    link_text = link_element.text_content()
    return link_text

def fetch_quotes_page(url, page_num):
    with requests.Session() as session:
        quotes = quotes_page(f"{url}?p={page_num}")
        return quotes
def persona(request):
    query = request.GET.get('query', "none")
    quote_list = []

    base_url = "https://www.azquotes.com"
    url = f"{base_url}/author/{query}"
    author_name = get_author(url)

    num_pages = 5
    with multiprocessing.Pool() as pool:
        fetch_quotes_partial = partial(fetch_quotes_page, url)
        results = pool.map(fetch_quotes_partial, range(1, num_pages + 1))

    for quotes in results:
        quote_list.extend(quotes)

    quote_list = list(set(quote_list))
    quote_author = get_author(url)
    return render(request, 'persona.html', {'quote_list': quote_list, 'quote_author': quote_author})  
