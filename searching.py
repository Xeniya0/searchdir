# <doc>
#     ...
# </doc>
from dataclasses import dataclass
import gzip
from lxml import etree
import Abstract
import re
import string
from collections import Counter
from analysis import analyze


@dataclass
class Abstract:
    """Data abstract"""
    ID: int
    title: str
    abstract: str
    url: str

    @property
    def fulltext(self):
        return ' '.join([self.title, self.abstract])


def load_documents():
    # open a filehandle to the gzipped Wikipedia dump
    with gzip.open('path/file', 'rb') as f:
        doc_id = 1
        # iterparse will yield the entire `doc` element once it finds the
        # closing `</doc>` tag
        for _, element in etree.iterparse(f, events=('end',), tag='doc'):
            title = element.findtext('./title')
            url = element.findtext('./url')
            abstract = element.findtext('./abstract')

            yield Abstract(ID=doc_id, title=title, url=url, abstract=abstract)

            doc_id += 1
            # the `element.clear()` call will explicitly free up the memory
            # used to store the element
            element.clear()
            
# import Stemmer
#
# STEMMER = Stemmer.Stemmer('english')
#
# def tokenize(text):
#     return text.split()
#
# def lowercase_filter(text):
#     return [token.lower() for token in tokens]
#
# def stem_filter(tokens):
#     return STEMMER.stemWords(tokens)


PUNCTUATION = re.compile('[%s]' % re.escape(string.punctuation))

def punctuation_filter(tokens):
    return [PUNCTUATION.sub('', token) for token in tokens]

def analyze(text):
    tokens = tokenize(text)
    tokens = lowercase_filter(tokens)
    tokens = punctuation_filter(tokens)
    tokens = stopword_filter(tokens)
    tokens = stem_filter(tokens)

    return [token for token in tokens if token]

class Index:
    def __init__(self):
        self.index = {}
        self.documents = {}

    def index_document(self, document):
        if document.ID not in self.documents:
            self.documents[document.ID] = document

        for token in analyze(document.fulltext):
            if token not in self.index:
                self.index[token] = set()
            self.index[token].add(document.ID)

def _results(self, analyzed_query):
    return [self.index.get(token, set()) for token in analyzed_query]

def search(self, query):
    """
    Boolean search; this will return documents that contain all words from the
    query, but not rank them (sets are fast, but unordered).
    """
    analyzed_query = analyze(query)
    results = self._results(analyzed_query)
    documents = [self.documents[doc_id] for doc_id in set.intersection(*results)]

    return documents

# частота вхождений



@dataclass
class Abstract:
    # snip
    def analyze(self):
        # Counter will create a dictionary counting the unique values in an array:
        # {'london': 12, 'beer': 3, ...}
        self.term_frequencies = Counter(analyze(self.fulltext))

    def term_frequency(self, term):
        return self.term_frequencies.get(term, 0)

def index_document(self, document):
    if document.ID not in self.documents:
        self.documents[document.ID] = document
        document.analyze()


def search(self, query, search_type='AND', rank=True):
    # snip
    if rank:
        return self.rank(analyzed_query, documents)
    return documents


def rank(self, analyzed_query, documents):
    results = []
    if not documents:
        return results
    for document in documents:
        score = sum([document.term_frequency(token) for token in analyzed_query])
        results.append((document, score))
    return sorted(results, key=lambda doc: doc[1], reverse=True)


import math

def document_frequency(self, token):
    return len(self.index.get(token, set()))

def inverse_document_frequency(self, token):
    return math.log10(len(self.documents) / self.document_frequency(token))

def rank(self, analyzed_query, documents):
    results = []
    if not documents:
        return results
    for document in documents:
        score = 0.0
        for token in analyzed_query:
            tf = document.term_frequency(token)
            idf = self.inverse_document_frequency(token)
            score += tf * idf
        results.append((document, score))
    return sorted(results, key=lambda doc: doc[1], reverse=True)