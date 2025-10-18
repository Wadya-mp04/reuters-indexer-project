from reuters_loader import *
from indexers import *
from queries.query import *
import nltk
import time  # <-- added

print(f'{len(docs)} documents retrieved')

index = None  # global

def race_build_times():
    """Build Naive and SPIMI indexes once each and report setup times."""
    print("\n=== Naive vs SPIMI: Build-Time Race ===")
    t0 = time.perf_counter()
    _naive = naiveIndexer(docs)
    t1 = time.perf_counter()
    naive_time = t1 - t0
    print(f"Naive build time: {naive_time:.4f} s")

    t0 = time.perf_counter()
    _spimi = spimiIndexer(docs)
    t1 = time.perf_counter()
    spimi_time = t1 - t0
    print(f"SPIMI build time: {spimi_time:.4f} s")

    # quick winner note
    winner = "Naive" if naive_time < spimi_time else "SPIMI"
    print(f"Winner: {winner} ({min(naive_time, spimi_time):.4f}s)\n")
    # note: we don't assign to the global 'index'—this race is standalone

def menu():
    global index  # <-- tell Python we mean the global 'index'

    while True:
        # top menu
        print("Hello! Welcome to Waddah's Indexer Project!")
        print("*******************************************")
        print("Please pick which query you'd like:")
        print("1. Single term")
        print("2. AND query")
        print("3. OR query")
        print("4. Race: Build Naive vs SPIMI")  # <-- new option
        print("5. print compression table")
        print("6. Exit")
        print("*******************************************")
        try:
            q_in = int(input('answer: '))
        except ValueError:
            print("Invalid input, try again.\n"); continue

        if q_in == 6:
            print('goodbye.'); return
        if q_in == 4:
            race_build_times()
            continue
        if q_in== 5:
            print_table()
            continue
        if q_in not in (1,2,3,4,5):
            print("Invalid choice.\n"); continue

        # indexer menu
        while True:
            print("*******************************************")
            print("Which Indexer would you prefer?")
            print("1. Naive Indexer")
            print("2. SPIMI Indexer (todo)")
            print("3. Back")
            print("*******************************************")
            try:
                i_in = int(input('answer: '))
            except ValueError:
                print("Invalid input, try again.\n"); continue
            if i_in == 3:
                break
            elif i_in == 1:
                if index is None:
                    print("Building naive index... (one-time)")
                    index = naiveIndexer(docs)  # build once, then reuse
                    print("Index ready!\n")

                # run query
                if q_in == 1:
                    term = input("Enter term: ").strip()
                    result = single(term, index)
                    print(f"{len(result)} docs:", result[:20], "...\n")
                elif q_in == 2:
                    t1 = input("term1: ").strip()
                    t2 = input("term2: ").strip()
                    result = AND(t1, t2, index)
                    print(f"{len(result)} docs:", result[:20], "...\n")
                elif q_in == 3:
                    t1 = input("term1: ").strip()
                    t2 = input("term2: ").strip()
                    result = OR(t1, t2, index)
                    print(f"{len(result)} docs:", result[:20], "...\n")

            elif i_in == 2:
                spimiIndex = spimiIndexer(docs)
                if q_in == 1:
                    term = input("Enter term: ").strip()
                    result = single(term, spimiIndex)
                    print(f"{len(result)} docs:", result[:20], "...\n")
                elif q_in == 2:
                    t1 = input("term1: ").strip()
                    t2 = input("term2: ").strip()
                    result = AND(t1, t2, spimiIndex)
                    print(f"{len(result)} docs:", result[:20], "...\n")
                elif q_in == 3:
                    t1 = input("term1: ").strip()
                    t2 = input("term2: ").strip()
                    result = OR(t1, t2, spimiIndex)
                    print(f"{len(result)} docs:", result[:20], "...\n")

            else:
                print("Invalid choice.\n")

menu()

#for context: I was comparing the niave indexer with a compressed index
# query_test = ['your','life','zue',('your','be'),('zone','war'),('humidity','restored')]
# naive_index = naiveIndexer(docs)
# compressed_index = buildIndex(pairManager(docs,1,1,1,1))

# print("naive indexer:")
# for i in range(6):
#     if i>=3:
#         print(f'{query_test[i][0]} AND {query_test[i][1]} :')
#         result = AND(query_test[i][0],query_test[i][1],naive_index)
#     else:
#         print(f'{query_test[i]}:')
#         result = single(query_test[i], naive_index)

#     print(result)

# print("compressed indexer:")
# for i in range(6):
#     if i>=3:
#         print(f'{query_test[i][0]} AND {query_test[i][1]} :')
#         result = AND(query_test[i][0],query_test[i][1],compressed_index)
#     else:
#         print(f'{query_test[i]}:')
#         result = single(query_test[i], compressed_index)

#     print(result)
# subproject 3.2 end


