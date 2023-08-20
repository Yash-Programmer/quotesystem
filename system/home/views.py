from django.shortcuts import render
import requests
from lxml import etree, html
from bs4 import BeautifulSoup

letters=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',]
# Create your views here.

def get_quote():
    url = "https://www.azquotes.com/"
    response = requests.get(url)
    html_content = response.content
    tree = etree.HTML(html_content)
    link_element = tree.xpath("""//*[@id="landing-content"]/div/div[1]/div/div[1]/div/div[3]/div/div[1]/p/a""")
    # link_text = link_element.text_content()
    return link_element

def index(request):
    url = "https://www.azquotes.com/"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        target_element = soup.find("a", class_="title")
        text = target_element.get_text()
        print(text)
    soup = BeautifulSoup(response.content, "html.parser")

    div_element = soup.find("div", class_="q_user")
    a_element = div_element.find("a")
    author = a_element.get_text()
    href_value = a_element["href"]
    href_value = "/persona?query=" + href_value[8:]
    
    print(href_value)
    
    array = []
    upper_letters=[]
    for i in range(len(letters)):
        array.append(f'/authors?letter={letters[i]}')
        upper_letters.append(letters[i].upper())
        
    alphabet_pairs = zip(array, upper_letters)    
    return render(request, 'index.html', {'alphabet_pairs': alphabet_pairs, 'quote': text, 'author': author, "url": href_value})