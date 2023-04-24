import pandas as pd
df = pd.read_csv("./all.csv", parse_dates=True)

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

df['Date'] = pd.to_datetime(df['Date'])
words = [
    "газпром",
    "газ",
    "нефть",
    "бензин",
    "санкции",
    "кризис",
    "рубль",
    "рост",
    "падение",
    "цена",
    "подорожание",
    "удешевение"
]
_filter = df['Text'].str.contains(" " + stemming(words[0]) + " ")
for w in words:
    s = stemming(w)
    _filter |= df['Text'].str.contains(" " + s + " ")
    _filter |= df['Text'].str.contains("^" + s + " ")
    _filter |= df['Text'].str.contains(" " + s + "$")
df['HasWords'] = _filter

funds = pd.read_excel("./gazprom-moscow-exchange.xlsx")
funds['Дата'] = pd.to_datetime(funds['Дата'], dayfirst=True)
funds['Change'] = 0
funds = funds.sort_values("Дата")
for i in range(1, funds.shape[0]):
    funds['Change'].iloc[i] = funds['Цена avg'].iloc[i] - funds['Цена avg'].iloc[i - 1]

import datetime

changes = {}
for i in range(1, funds.shape[0]):
    start = funds["Дата"].iloc[i - 1]
    end = funds["Дата"].iloc[i]
    date = start
    while date < end:
        changes[str(date)] = funds['Change'].iloc[i]
        date += datetime.timedelta(days=1)
        
df['Change'] = 0
for i in range(df.shape[0]):
    date = df["Date"].iloc[i]
    if str(date) in changes:
        change = changes[str(date)]
        df["Change"].iloc[i] = change

df['ChangeSign'] = 0
for i in range(df.shape[0]):
    if df['HasWords'].iloc[i]:
        df['ChangeSign'].iloc[i] = 1 if df['Change'].iloc[i] > 0 else 0 if df['Change'].iloc[i] == 0 else -1

df = df.drop(columns=["Unnamed: 0"])
df.to_csv('./signed.csv', encoding='utf-8-sig')