from nltk.tokenize import word_tokenize, RegexpTokenizer
from nltk.corpus import stopwords
import re


_WORDS_ONLY = RegexpTokenizer(r"[A-Za-z]+(?:'[A-Za-z]+)?")          # regex by AI to remove numbers AND punctuation
_ALNUM_WORDS = RegexpTokenizer(r"[A-Za-z0-9]+(?:'[A-Za-z0-9]+)?")   # regex to remove punctuation only!!!
STOPWORDS = set(stopwords.words('english'))

def naiveTokenizer(body: str):
    if not body:
        return []
    return word_tokenize(body)

def tokenizer(body: str, omit_punc: bool, no_number: bool, case_folding: bool, no_sw: bool):

    tokens = []
    if not body:
        return tokens

    if (omit_punc==0 and no_number==0 and case_folding==0 and no_sw == 0): 
        return naiveTokenizer(body)

    # 1) Start from a baseline token stream
    #    If you plan to omit punctuation, go straight to the regex tokenizer (cleaner).
    if omit_punc:
        tokens = _ALNUM_WORDS.tokenize(body)

    # 2) Remove numbers 
    if no_number:
        tokens = _WORDS_ONLY.tokenize(body)

    # 3) Case-fold before any dictionary-based filters
    if case_folding:
        for t in tokens:
            t.casefold()

    # 4) Stopword filter (don’t mutate while iterating!)
    if no_sw:
        tokens = [t for t in tokens if t not in STOPWORDS]

    return tokens

