import pandas as pd
def clear_dates(df):
    df['Text'] = df['Title'] + " " + df['Article'] + " " + df['Tags']
    df = df.drop(columns=['Title', 'Article', 'Tags'])
    df = df[df['Text'].notnull()]
    isnull = df['Date'].isnull()
    for i in range(1, df.shape[0]):
        if isnull.iloc[i]:
            df['Date'].iloc[i] = df['Date'].iloc[i - 1]
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.drop_duplicates(['Text'])
    return df

def delete_words(df):
    marks = ['!', '\"', "\'", '\(', '\)', '\-', '\+', ',', '\.', ';', ':', '<', '>', '\[', '\]', '%', '\$']
    for m in marks:
        df['Text'] = df['Text'].replace(m, " ", regex=True)
    numbers = [str(i) for i in range(10)]
    for n in numbers:
        df['Text'] = df['Text'].replace(n, " ", regex=True)
    df['Text'] = df['Text'].str.lower()
    aux_words = [
        'даже',
        "еще",
        "именно",
        "как раз",
        "только",
        "просто",
        "прямо",
        "буквально",
        "хоть",
        "хотя бы",
        "почти",
        "чуть не",
        "чуть ли не",
        "едва ли",
        "все таки",
        "все же",
        "но",
        "да",
        "или",
        "то есть",
        "именно",
        "как то",
        "будь то",
        "то",
        "не",
        "ли",
        "как и",
        "чем",
        "тем",
        "словно",
        "точно",
        "в целом",
        "в общем",
        "в основном",
        "во многом",
        "во",
        "без малого",
        "в итоге",
        "в результате",
        "к слову",
        "в идеале",
        "в частности",
        "что",
        "а вдобавок",
        "а именно",
        "а также",
        "а то",
        "будто",
        "вдобавок",
        "даже",
        "же",
        "едва",
        "ежели",
        "если",
        "зато",
        "зачем",
        "или",
        "как",
        "когда",
        "коли",
        "из",
        "однако",
        "пока",
        "потому",
        "пусть",
        "также",
        "тоже",
        "хотя",
        "точно",
        "чем",
        "чтобы",
        "без",
        "близ",
        "во",
        "вместо",
        "вне",
        "для",
        "до",
        "за",
        "из",
        "из за",
        "из под",
        "кроме",
        "между",
        "на",
        "над",
        "об",
        "от",
        "перед",
        "по",
        "под",
        "при",
        "про",
        "ради",
        "со",
        "сквозь",
        "среди",
        "через",
        "здесь"
    ]
    for w in aux_words:
        df['Text'] = df['Text'].replace(" " + w + " ", " ", regex=True)
        df['Text'] = df['Text'].replace("^" + w + " ", " ", regex=True)
        df['Text'] = df['Text'].replace(" " + w + "$", " ", regex=True)
    letters = list(map(chr, range(ord('а'), ord('я')+1)))
    for l in letters:
        df['Text'] = df['Text'].replace(" " + l + " ", " ", regex=True)
        df['Text'] = df['Text'].replace("^" + l + " ", " ", regex=True)
        df['Text'] = df['Text'].replace(" " + l + "$", " ", regex=True)
    return df

import re

class Porter:
    PERFECTIVEGROUND =  re.compile(u"((ив|ивши|ившись|ыв|ывши|ывшись)|((?<=[ая])(в|вши|вшись)))$")
    REFLEXIVE = re.compile(u"(с[яь])$")
    ADJECTIVE = re.compile(u"(ее|ие|ые|ое|ими|ыми|ей|ий|ый|ой|ем|им|ым|ом|его|ого|ему|ому|их|ых|ую|юю|ая|яя|ою|ею)$")
    PARTICIPLE = re.compile(u"((ивш|ывш|ующ)|((?<=[ая])(ем|нн|вш|ющ|щ)))$")
    VERB = re.compile(u"((ила|ыла|ена|ейте|уйте|ите|или|ыли|ей|уй|ил|ыл|им|ым|ен|ило|ыло|ено|ят|ует|уют|ит|ыт|ены|ить|ыть|ишь|ую|ю)|((?<=[ая])(ла|на|ете|йте|ли|й|л|ем|н|ло|но|ет|ют|ны|ть|ешь|нно)))$")
    NOUN = re.compile(u"(а|ев|ов|ие|ье|е|иями|ями|ами|еи|ии|и|ией|ей|ой|ий|й|иям|ям|ием|ем|ам|ом|о|у|ах|иях|ях|ы|ь|ию|ью|ю|ия|ья|я)$")
    RVRE = re.compile(u"^(.*?[аеиоуыэюя])(.*)$")
    DERIVATIONAL = re.compile(u".*[^аеиоуыэюя]+[аеиоуыэюя].*ость?$")
    DER = re.compile(u"ость?$")
    SUPERLATIVE = re.compile(u"(ейше|ейш)$")
    I = re.compile(u"и$")
    P = re.compile(u"ь$")
    NN = re.compile(u"нн$")

    def stem(word):
        word = word.lower()
        word = word.replace(u'ё', u'е')
        m = re.match(Porter.RVRE, word)
        if m is None:
            return word
        if m.groups():
            pre = m.group(1)
            rv = m.group(2)
            temp = Porter.PERFECTIVEGROUND.sub('', rv, 1)
            if temp == rv:
                rv = Porter.REFLEXIVE.sub('', rv, 1)
                temp = Porter.ADJECTIVE.sub('', rv, 1)
                if temp != rv:
                    rv = temp
                    rv = Porter.PARTICIPLE.sub('', rv, 1)
                else:
                    temp = Porter.VERB.sub('', rv, 1)
                    if temp == rv:
                        rv = Porter.NOUN.sub('', rv, 1)
                    else:
                        rv = temp
            else:
                rv = temp
            
            rv = Porter.I.sub('', rv, 1)

            if re.match(Porter.DERIVATIONAL, rv):
                rv = Porter.DER.sub('', rv, 1)

            temp = Porter.P.sub('', rv, 1)
            if temp == rv:
                rv = Porter.SUPERLATIVE.sub('', rv, 1)
                rv = Porter.NN.sub(u'н', rv, 1)
            else:
                rv = temp
            word = pre+rv
        return word
    stem=staticmethod(stem)

def stemming(s):
    s = s.split()
    s = map(lambda ss: Porter.stem(ss), s)
    return " ".join(s)
def stem(df):
    for i in range(df.shape[0]):
        df['Text'].iloc[i] = stemming(df['Text'].iloc[i])
    return df

import datetime
def preprocess(df):
    df = clear_dates(df)
    df = delete_words(df)
    df = stem(df)
    df = df[df['Date'] >= datetime.datetime(2015, 1, 1)]
    return df

df = pd.read_csv("./interfax.csv", parse_dates=True)
interfax = preprocess(df)

df = pd.read_csv("./ria.csv", parse_dates=True)
ria = preprocess(df)

df = pd.read_csv("./rbc.csv", parse_dates=True)
import math

def parse_date(url):
    if (not isinstance(url, str) and math.isnan(url)):
        return None
    date = re.findall("[0-9]+/", url)
    if len(date) != 3:
        return None
    
    year = int(date[2][:-1])
    month = int(date[1][:-1])
    day = int(date[0][:-1])
    try:
        return datetime.datetime(year, month, day)
    except:
        return None
for i in range(df.shape[0]):
    df["Date"].iloc[i] = parse_date(df["URL"].iloc[i])

rbc = preprocess(df)

df = pd.concat([interfax, ria, rbc])
df = df.sort_values('Date', ascending=False)
df = df[df['Date'] >= datetime.datetime(2015, 1, 1)]
for i in range(df.shape[0]):
    date = df['Date'].iloc[i]
    df['Date'].iloc[i] = datetime.datetime(date.year, date.month, date.day)
df.to_csv('./all.csv', encoding='utf-8-sig')