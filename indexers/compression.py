# compression.py
from indexers import buildIndex, pairManager
from reuters_loader.tokenizer import tokenizer
from reuters_loader import docs  # assumes docs is a dict[int, {'title','body'}]

def count_tokens(docs, omit_punc, no_number, case_folding, no_sw):
    """Return total token count across all docs for a given tokenizer configuration."""
    total = 0
    for doc in docs:
        total += len(tokenizer(docs[doc]['body'], omit_punc, no_number, case_folding, no_sw))
    return total

def count_nonpos_postings(docs, omit_punc, no_number, case_folding, no_sw):
    """Return total unique (term, docID) pair count."""
    return len(pairManager(docs, omit_punc, no_number, case_folding, no_sw))

def count_terms(docs, omit_punc, no_number, case_folding, no_sw):
    """Return dictionary size (# of distinct terms)."""
    index = buildIndex(pairManager(docs, omit_punc, no_number, case_folding, no_sw))
    return len(index)

def percent_delta(prev, cur):
    return round(100 * (prev - cur) / prev, 2) if prev else 0

def percent_total(base, cur):
    return round(100 * (base - cur) / base, 2) if base else 0

def print_table():
    # compute all values dynamically
    configs = [
        ("unfiltered", 0,0,0,0),
        ("no punctuation", 1,0,0,0),
        ("no numbers", 1,1,0,0),
        ("case folded", 1,1,1,0),
        ("no stopwords (150)", 1,1,1,1),
    ]

    stats = []
    for name, punc, num, case, sw in configs:
        tokens = count_tokens(docs, punc, num, case, sw)
        npp = count_nonpos_postings(docs, punc, num, case, sw)
        terms = count_terms(docs, punc, num, case, sw)
        stats.append((name, tokens, npp, terms))

    base_tokens, base_npp, base_terms = stats[0][1], stats[0][2], stats[0][3]
    prev_tokens, prev_npp, prev_terms = base_tokens, base_npp, base_terms

    print(f"{'Preprocessing Step':<20} | {'Distinct Terms':>14} {'Δ%':>6} {'T%':>6} | "
          f"{'Nonpos. Postings':>17} {'Δ%':>6} {'T%':>6} | {'Tokens':>10} {'Δ%':>6} {'T%':>6}")
    print("-" * 92)

    for name, tokens, npp, terms in stats:
        d_terms = percent_delta(prev_terms, terms)
        t_terms = percent_total(base_terms, terms)

        d_npp = percent_delta(prev_npp, npp)
        t_npp = percent_total(base_npp, npp)

        d_tok = percent_delta(prev_tokens, tokens)
        t_tok = percent_total(base_tokens, tokens)

        print(f"{name:<20} | {terms:>14} {d_terms:>6.1f} {t_terms:>6.1f} | "
              f"{npp:>17} {d_npp:>6.1f} {t_npp:>6.1f} | {tokens:>10} {d_tok:>6.1f} {t_tok:>6.1f}")

        prev_tokens, prev_npp, prev_terms = tokens, npp, terms

if __name__ == "__main__":
    print_table()
