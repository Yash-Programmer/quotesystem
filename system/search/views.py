from django.shortcuts import render
import ast
import requests
import openai
from lxml import html
# Create your views here.
def img(innovator):
    url = f"https://www.bing.com/images/search?q={innovator}"
    xpath_expression = '//*[@id="mmComponent_images_2"]/ul[1]/li[1]/div/div[1]/a/div/img/@src'

    response = requests.get(url)
    tree = html.fromstring(response.content)
    image_src = tree.xpath(xpath_expression)
    return image_src[0]
def search(request):
    openai.api_key = "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"
    quote_list = []
    
    innovator = request.GET.get('query', 'none')
    name = innovator.lower().split()
    for i in range(len(name)):
        name[i] = name[i][0].upper() + name[i][1:]
    innovator = ""

    for word in name:
        innovator += word+" "
    
    prompts = [
            {"prompt": f'''Write 25 famous quotes by {innovator} in python no quotation mark, seperated by one /n''', "max_tokens": 3000},
            
    ]  
        
    responses = []

    for prompt in prompts:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt["prompt"],
            max_tokens=prompt["max_tokens"],
            stop=None
        )
        responses.append(response.choices[0].text.strip())
    original_list = responses[0].split("/n")
    cleaned_list = [string.strip() for string in original_list]
    try:
        cleaned_list = [item for item in original_list if item.strip() != '']
    except:
        pass
    print(cleaned_list)
    # try:
    #     print(eval(responses[0]))
    # except:
    #     print(ast.literal_eval(responses[0]))
    return render(request, 'search.html', {'quote_list': cleaned_list, 'quote_author': innovator, 'img': img(innovator + ' square image')})