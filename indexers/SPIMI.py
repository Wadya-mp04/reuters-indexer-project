# spimi.py
from reuters_loader.tokenizer import tokenizer
import time

def spimiIndexer(docs: dict[int, dict[str, str]]):
    """Build an inverted index using SPIMI algorithm (in-memory)."""
    start_time = time.perf_counter()
    index = {}

    for doc_id, doc in docs.items():
        # Use the SPIMI tokenizer (omit punctuation, no numbers, lowercase)
        tokens = tokenizer(doc['body'], omit_punc=True, no_number=False, case_folding=True, no_sw=False)
        seen_in_doc = set()  # to avoid duplicate docIDs per term in the same document

        for term in tokens:
            if term in seen_in_doc:
                continue  # skip duplicate terms in same doc
            seen_in_doc.add(term)

            if term not in index:
                index[term] = [doc_id]
            else:
                # append only if this doc_id isn't already at the end (avoids duplicates)
                if index[term][-1] != doc_id:
                    index[term].append(doc_id)

    end_time = time.perf_counter()
    print(f"SPIMI indexing took: {end_time - start_time:.4f} seconds")
    return index
