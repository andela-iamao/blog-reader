#!/usr/bin/env python2

import urllib2
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from heapq import nlargest
from collections import defaultdict
from string import punctuation
from bs4 import BeautifulSoup

def getTextFromUrl(url):
    try:
        page = urllib2.urlopen(url).read().decode('utf8')
        soup = BeautifulSoup(page, 'lxml')
        text = ' '.join(map(lambda p: p.text, soup.find_all('p')))
        return text.encode('ascii', errors='replace').replace("?", " ")
    except:
        print 'Sorry the source of this link is not supported as of this time'
        return False


def summarizeText(text, n):
    if text == False:
        exit()
    sentences = sent_tokenize(text)
    if n > len(sentences):
        print 'I cannot summarize in more sentence than the original text'
        exit()
    
    words = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english') + list(punctuation))
    all_words = [word for word in words if word not in stop_words]
    frequency = FreqDist(all_words)
    ranking = defaultdict(int)

    for index, sentence in enumerate(sentences):
        for w in word_tokenize(sentence.lower()):
            if w in frequency:
                ranking[index] += frequency[w]
    
    return ''.join([sentences[i] for i in sorted(nlargest(n, ranking, key=ranking.get))]).strip('\n\t')

article = raw_input('> Enter blog URL: ')
sentence_length = int(raw_input('> How many sentences should I summarize in ? '))
print '\nSUMMARY: \n', summarizeText(getTextFromUrl(article), sentence_length)