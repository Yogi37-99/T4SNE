import requests
from bs4 import BeautifulSoup

def webpage_parser(url,out_dir):
    res = requests.get(url)
    html_page = res.content
    soup = BeautifulSoup(html_page, 'html.parser')
    text = soup.find_all(text=True)
    output = ''

    blacklist = [
        '[document]',
        'noscript',
        'header',
        'html',
        'meta',
        'head', 
        'input',
        'script',
        'button',
        'head',
        'footer',
        # there may be more elements you don't want, such as "style", etc.
    ]

    for i in range(len(text)):
        t = text[i]
        if t.parent.name not in blacklist:
            if len(t) > 1:
                #print(i,t)
                f = open(f'{out_dir}/p{i}.txt','w',encoding="utf-8")
                f.write(t)
                f.close()
            output += '{}_'.format(t)
    return output

url = 'https://www.mayoclinic.org/diseases-conditions/dyslexia/symptoms-causes/syc-20353552#:~:text=Dyslexia%20is%20a%20learning%20disorder,the%20brain%20that%20process%20language.'
out_dir = './text_files'

webpage_parser(url,out_dir)

#print(output)
#print(set(parents))

