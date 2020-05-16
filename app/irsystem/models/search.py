from .database import query_drink, query_embeddings, query_drink_vbytes
from scipy.spatial.distance import cdist
from gensim.models import Word2Vec
from gensim.models.phrases import Phraser
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
import pandas as pd
import numpy as np
import json
import string

DESC_MAP = pd.read_csv('app/static/descriptor_mapping.csv').set_index('raw descriptor')
STEMMER = SnowballStemmer('english')
PUNC_TABLE = str.maketrans({c: None for c in string.punctuation})
STOP_WORDS = set(stopwords.words('english'))
PHRASER = Phraser.load('app/static/trigram.pkl')
EMBEDDINGS = query_embeddings()

SEARCH_THRESH = 0.5
KEYWORD_THRESH = 0.7
KEYWORD_COUNT = 5

class Args:
    def __init__(self, data, dtype, pmin, pmax, amin, amax, base):
        self.data = data # str or list
        self.dtype = dtype # str
        self.pmin = pmin # float
        self.pmax = pmax # float
        self.amin = amin # float
        self.amax = amax # float
        self.base = base # str

    def __eq__(self, value):
        if isinstance(value, Args):
            return self.__dict__ == value.__dict__
        return NotImplemented

def score(dist):
    return round(100 * (1 - dist), 0)

def make_query(data):
    # Fetch query vector from drink name
    if type(data) == str:
        vbytes = query_drink_vbytes(data)
        if vbytes is None:
            return [], data
        return np.array(json.loads(vbytes)), data
    # Form query vector from word embeddings
    if type(data) == list:
        emb_dict = {e.word: np.array(json.loads(e.vbytes)) for e in EMBEDDINGS}
        q_vectors = [emb_dict[d] for d in data if d in emb_dict]
        return sum(q_vectors) / len(q_vectors), None
    return None, None

def search_drinks(drinks, query, drink_name=None):
    if query is None:
        return [(d, None) for d in drinks]

    # Search database results for k nearest neighbors
    d_vectors = [np.array(json.loads(d.vbytes)) for d in drinks if d.name != drink_name]
    knn_data = np.array(d_vectors).reshape(len(d_vectors), -1)
    dst_vec = cdist([query], knn_data, 'cosine')[0]
    ind_vec = np.argsort(dst_vec)
    
    return [(drinks[i], score(dst_vec[i])) for i in ind_vec if dst_vec[i] <= SEARCH_THRESH]

def extract_keywords(text, query):
    if query is None:
        return []
    emb_dict = {e.word: np.array(json.loads(e.vbytes)) for e in EMBEDDINGS}
    tokens = word_tokenize(text)
    stem_to_word = {}
    for t in tokens:
        word = str.lower(t.translate(PUNC_TABLE))
        stem = STEMMER.stem(word)
        if len(stem) > 1 and stem not in STOP_WORDS:
            if stem not in stem_to_word:
                stem_to_word[stem] = set()
            stem_to_word[stem].add(word)
    phrased = PHRASER[list(stem_to_word)]
    norms = set()
    norm_to_word = {}
    for phr in phrased:
        if phr in set(DESC_MAP.index):
            norm = DESC_MAP['level_3'][phr]
            if norm in emb_dict:
                if norm not in norm_to_word:
                    norm_to_word[norm] = []
                norm_to_word[norm] += [word for stem in phr.split('_') for word in stem_to_word[stem]]
                norms.add(norm)
    norms = list(norms)
    vectors = [emb_dict[e] for e in norms]
    knn_data = np.array(vectors).reshape(len(vectors), -1)
    dst_vec = cdist([query], knn_data, 'cosine')[0]
    ind_vec = np.argsort(dst_vec)
    res = []
    for i in ind_vec[:KEYWORD_COUNT]:
        if dst_vec[i] > KEYWORD_THRESH:
            break
        res += norm_to_word[norms[i]]
    # Reversing ensures longer keywords are processed first for proper bolding
    # E.g. bold "apples" before "apple" so the 's' doesn't get ignored
    return sorted(res, reverse=True)
