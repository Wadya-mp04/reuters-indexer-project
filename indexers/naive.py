from reuters_loader.tokenizer import *
import time 

def naiveIndexer(docs: dict[int, dict[str,str]]):           #naive indexer takes doc dictionary
    start_time = time.perf_counter()
    F = []
    for doc in docs:                                        #iterates thru all docs in dict 
        tokenized = naiveTokenizer(docs[doc]['body'])       #use nltk word_tokenize to produce tokens
        for term in tokenized:                              #loop through each token and create term/docID pairs in tuples
            F.append((term,doc))                        
    
    F.sort()                                                #sort pair list
    out = []
    prev = None                                             #remove duplicates
    for pair in F:
        if pair != prev:
            out.append(pair)
            prev = pair
    F=out
    result = buildIndex(F)                                  #func to convert pairs to index (dict[term] = [postings list])
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print(f"Naive indexing for all files took: {elapsed_time:.4f} seconds")
    return result

        

def buildIndex (F:list[tuple[str,int]]):
    index = {}
    for term, doc_id in F:
        if term not in index:
            index[term] = []
        # since F has no duplicates, appending yields unique docIDs in ascending order
        index[term].append(doc_id)
    return index

def pairManager(docs: dict[int, dict[str,str]], omit_punc: bool, no_number: bool, case_folding: bool, no_sw: bool): #for dictionary table (to get nonpositional postings!) exact same as iteratore in naive indexer but we dont use naive Tokenzier necassarily
    F = []
    for doc in docs:                                        
        tokenized = tokenizer(docs[doc]['body'],omit_punc, no_number, case_folding, no_sw)       
        for term in tokenized:                              #loop through each token and create term/docID pairs in tuples
            F.append((term,doc))                        
    
    F.sort()                                                #sort pair list
    out = []
    prev = None                                             #remove duplicates
    for pair in F:
        if pair != prev:
            out.append(pair)
            prev = pair
    F=out
    return out          #sorted and unique docID,term pairs --> nonpositional postings!!!


