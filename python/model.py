import pandas as pd
df = pd.read_csv("./signed.csv", parse_dates=True)
df['Date'] = pd.to_datetime(df['Date'])

with open("./words.txt", 'r', encoding='UTF-8') as file:
    lines = [line.rstrip() for line in file]
lines.append('газпром')

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

lines = list(set([stemming(line) for line in lines]))
for line in lines:
    for c in line:
        if c in "$#-0123456789":
            lines.remove(line)
            break
        if c in "abcdefghijklmnopqrstuvxyz":
            lines.remove(line)
            break

dictionary = {}
for i in range(len(lines)):
    dictionary[lines[i]] = i

import numpy as np
import math

idf = np.zeros(len(dictionary))
for i in range(df.shape[0]):
    words = list(set(df['Text'].iloc[i].split()))
    for w in words:
        if w in dictionary:
            idf[dictionary[w]] += 1
idf = np.log(df.shape[0] / idf)
for i in range(len(dictionary)):
    if math.isinf(idf[i]):
        idf[i] = 0

def vectorize(text, dictionary):
    words = text.split()
    tf = np.zeros(len(dictionary))
    for w in words:
        if w in dictionary:
            tf[dictionary[w]] += 1
    tf /= len(words)
    return tf * idf

import scipy

vectors = scipy.sparse.csr_matrix((df.shape[0], len(dictionary)), dtype = np.float64).toarray()
for i in range(df.shape[0]):
    vector = vectorize(df['Text'].iloc[i], dictionary)
    for j in range(len(dictionary)):
        vectors[i, j] = vector[j]

from sklearn.linear_model import LogisticRegression
count = int(df.shape[0] * 0.8)
X = vectors
y = df['ChangeSign']

lr = LogisticRegression(random_state=0, verbose=10, n_jobs=-1, C=50, solver='saga').fit(X[:count], y[:count])
lr.score(X[:count], y[:count])
lr.score(X[count:], y[count:])

import pickle
with open("./logistic.model", 'wb') as f:
    pickle.dump(lr, f)