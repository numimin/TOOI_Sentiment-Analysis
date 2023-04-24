import json
from bs4 import BeautifulSoup
import urllib.request
import re
import sys
import datetime

def dl_url(url, parse, _print=False, encoding='utf-8'):
    try:
        with urllib.request.urlopen(url, timeout=60) as f:
            if encoding == 'utf-8':
                html = f.read().decode(encoding)
            else:
                html = f.read()
        data = parse(url, html)
        if not data:
            return
        (title, article, tags, date) = data
        if _print:
            print(f"Title: {title}, Date: {date}, Tags: {tags}")
            print(article)
        return (url, title, article, tags, date)
    except:
        print("Error")

def dl_vk_data(group_id, parse, offset=0, count=5, use_js_emulator=False, _print=True, encoding='utf-8'):
    with urllib.request.urlopen(f'https://api.vk.com/method/wall.get?access_token=247f3d70247f3d70247f3d70d6276dfd5c2247f247f3d70478c4cc7443965779421d6d7&owner_id={group_id}&v=5.131&offset={offset}&count={count}', timeout=60) as f:
        json_string = f.read().decode('utf-8')
    json_res = json.loads(json_string)['response']
    datas = []
    for item in json_res['items']:
        if _print:
            print("-" * 50)
        text = item['text']
        if _print:
            print(text)
        title = ""
        try:
            title = item['title']
        except:
            print("No title")
        datas.append(("", title, text, [], None))
        #url = re.search("(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))", text)
        match_url = re.search("https?://www.interfax.ru/.*", text)
        if not match_url is None:
            data = dl_url(match_url[0], parse, _print, encoding)
            if not data is None:
                datas.append(data)
        match_url = re.search("https?://(www.)?ria.ru/.*", text)
        if not match_url is None:
            data = dl_url(match_url[0], parse, _print, encoding)
            if not data is None:
                datas.append(data)
        match_url = re.search("https?://(www.)?rbc.ru/.*", text)
        if not match_url is None:
            data = dl_url(match_url[0], parse, _print, encoding)
            if not data is None:
                datas.append(data)
        for attachment in item['attachments']:
            link = attachment.get('link')
            print(link)
            if not link:
                continue
            url = link['url']
            if _print:
                print(url)
            data = dl_url(url, parse, _print, encoding)
            if not data is None:
                datas.append(data)
    return datas
            
def parse_title_rbc(soup):
    title_html = soup.find("div", class_="article__header__title")
    if not title_html:
        return ""
    
    return str(title_html.h1.string).strip()

def parse_article_rbc(soup):
    article_html = soup.find("div", class_="article__text")
    if not article_html:
        return ""
    
    paragraphs = article_html.find_all(re.compile("(p|h|li)"))
    article = ""
    for block in paragraphs:
        for s in block.stripped_strings:
            article += str(s) + " "
    return article

def parse_tags_rbc(soup):
    tags_html = soup.find("div", class_="article__tags__container")
    if not tags_html:
        return []
    
    tags = []
    for tag in map(lambda s: str(s.string), tags_html.find_all("a")):
        tags.append(tag)
    return tags

def parse_date_rbc(url):
    date = re.findall("[0-9]+/", url)
    if len(date) != 2:
        return None
    
    year = int(date[2][:-1])
    month = int(date[1][:-1])
    day = int(date[0][:-1])
    return datetime.datetime(year, month, day)

def parse_rbc(url, html):
    soup = BeautifulSoup(html)
    title = parse_title_rbc(soup)
    article = parse_article_rbc(soup)
    tags = parse_tags_rbc(soup)
    date = parse_date_rbc(url)
    
    return (title, article, tags, date)

def parse_title_ria(soup):
    title_html = soup.find("div", class_="article__title")
    if not title_html:
        return ""
    second_title_html = soup.find("h1", class_="article__second-title")
    if not second_title_html:
        return ""
    
    return str(title_html.string) + ". " + str(second_title_html.string)

def parse_article_ria(soup):
    article_html = soup.find_all("div", class_="article__text")
    if not article_html:
        return ""
    
    article = ""
    for block in article_html:
        for s in block.stripped_strings:
            article += str(s) + " "
    return article

def parse_tags_ria(soup):
    tags_html = soup.find_all("a", class_="article__tags-item")
    if not tags_html:
        return []
    
    tags = []
    for tag in tags_html:
        tags.append(str(tag.string))
    return tags

def parse_date_ria(url):
    date = re.search("/[0-9]+/", url).group()[1:-1]
    year = int(date[0:4])
    month = int(date[4:6])
    day = int(date[6:8])
    return datetime.datetime(year, month, day)
    
def parse_ria(url, html):
    soup = BeautifulSoup(html)
    title = parse_title_ria(soup)
    article = parse_article_ria(soup)
    tags = parse_tags_ria(soup)
    date = parse_date_ria(url)
    
    return (title, article, tags, date)

def parse_title_interfax(soup):
    title_html = soup.find("h1", itemprop="headline")
    if not title_html:
        return ""
    return title_html.string

def parse_article_interfax(soup):
    article_html = soup.find("article", itemprop="articleBody")
    if not article_html:
        return ""
    
    article = ""
    for p in article_html.find_all("p"):
        for s in p.stripped_strings:
            article += str(s) + " "
    return article

def parse_tags_interfax(soup):
    tags_html = soup.find("div", class_="textMTags")
    if not tags_html:
        return []
    
    tags = []
    for a in tags_html.find_all("a"):
        tags.append(str(a.string))
    return tags

def parse_date_interfax(soup):
    date_html = soup.find("aside", class_="textML")
    if not date_html:
        return None
    date = date_html.find("time")['datetime']
    return datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M")

def parse_interfax(url, html):
    soup = BeautifulSoup(html)
    title = parse_title_interfax(soup)
    article = parse_article_interfax(soup)
    tags = parse_tags_interfax(soup)
    date = parse_date_interfax(soup)
        
    return (title, article, tags, date)

all_data = []
offset = len(all_data)
def dl(offset, maximum=1000):
    start_offset = offset
    first_date = datetime.datetime(2015, 1, 1)
    needs_dl = True
    count = 5
    while needs_dl:
        print(offset)
        datas = dl_vk_data(-24228287, parse_interfax, offset=offset, count=count, _print=False, encoding='koi8')
        print(len(datas))
        for data in datas:
            (title, article, tags, date) = data
            print(title)
            print(date)
            all_data.append(data)
            if not date is None and date < first_date:
                needs_dl = False
        if len(datas) == 0:
            needs_dl = False
        offset += count
        if offset - start_offset > maximum:
            needs_dl = False

while True:
    offset = len(all_data)
    start_offset = offset
    dl(offset)
    end_offset = len(all_data)
    if end_offset <= start_offset:
        break
    data = [list(d) for d in all_data]
    df = pd.DataFrame(data, columns=['Title', 'Article', 'Tags', 'Date'])
    df.to_csv('./interfax.csv', encoding='utf-8-sig')

all_data = []
offset = len(all_data)
def dl(offset, maximum=1000):
    start_offset = offset
    first_date = datetime.datetime(2015, 1, 1)
    needs_dl = True
    count = 5
    while needs_dl:
        print(offset)
        datas = dl_vk_data(-15755094, parse_ria, offset=offset, count=count, _print=False)
        print(len(datas))
        for data in datas:
            (title, article, tags, date) = data
            print(title)
            print(date)
            all_data.append(data)
            if not date is None and date < first_date:
                needs_dl = False
        if len(datas) == 0:
            needs_dl = False
        offset += count
        if offset - start_offset > maximum:
            needs_dl = False

offset = len(all_data)
while True:
    start_offset = offset
    dl(offset)
    end_offset = len(all_data)
    offset = end_offset
    if end_offset <= start_offset:
        break
    data = [list(d) for d in all_data]
    df = pd.DataFrame(data, columns=['Title', 'Article', 'Tags', 'Date'])
    df.to_csv('./ria.csv', encoding='utf-8-sig')

all_data = []
offset = len(all_data)
def dl(offset, maximum=1000):
    start_offset = offset
    first_date = datetime.datetime(2015, 1, 1)
    needs_dl = True
    count = 5
    while needs_dl:
        print(offset)
        datas = dl_vk_data(-25232578, parse_rbc, offset=offset, count=count, _print=False)
        print(len(datas))
        for data in datas:
            (url, title, article, tags, date) = data
            print(title)
            print(date)
            print(url)
            all_data.append(data)
            if not date is None and date < first_date:
                needs_dl = False
        if len(datas) == 0:
            needs_dl = False
        offset += count
        if offset - start_offset > maximum:
            needs_dl = False

offset = len(all_data)
while True:
    start_offset = offset
    dl(offset)
    end_offset = len(all_data)
    offset = end_offset
    if end_offset <= start_offset:
        break
    data = [list(d) for d in all_data]
    df = pd.DataFrame(data, columns=["URL", 'Title', 'Article', 'Tags', 'Date'])
    df.to_csv('./rbc.csv', encoding='utf-8-sig')