import time

def single (term:str,index: dict[str,list[int]]):
    start_time = time.perf_counter()
    if index.get(term):
        result = index[term]
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        print(f"Single query took: {elapsed_time:.4f} seconds")
        return result
    else:
        print(f'index doesnt have {term}')
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        print(f"Single query took: {elapsed_time:.4f} seconds")
        return ''

start_time = time.perf_counter()
end_time = time.perf_counter()
elapsed_time = end_time - start_time
print(f"Naive indexing for all files took: {elapsed_time:.4f} seconds")


def AND (term1:str,term2:str,index:dict[str,list[int]]):
    start_time = time.perf_counter()    
    if index.get(term1):
        list1 = index[term1]
    else:
        print(f'index doesnt have {term1}')
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        print(f"AND query took: {elapsed_time:.4f} seconds")
        return ''
    if index.get(term2):
        list2 = index[term2]
    else:
        print(f'index doesnt have {term2}')
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        print(f"AND query took: {elapsed_time:.4f} seconds")
        return ''

    # print('for context: ')
    # print(f'({term1}) -> {list1[:10]}')
    # print(f'({term2}) -> {list2[:10]}')
    result = []
    p1 =0
    p2 =0
    while(p1 < len(list1) and p2 < len(list2)):
        if (list1[p1] == list2[p2]):
            result.append(list1[p1])
            p1+=1
            p2+=1
        elif(list1[p1] > list2[p2]):
            p2+=1
        else:
            p1+=1
    
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print(f"AND query took: {elapsed_time:.4f} seconds")
    return result

def OR (term1:str,term2:str,index:dict[str,list[int]]):
    start_time = time.perf_counter()
    if index.get(term1):
        list1 = index[term1]
    else:
        print(f'index doesnt have {term1}')
        return ''
    if index.get(term2):
        list2 = index[term2]
    else:
        print(f'index doesnt have {term2}')
        return ''

    # print('for context: ')
    # print(f'({term1}) -> {list1}')
    # print(f'({term2}) -> {list2}')
    result = []
    p1 =0
    p2 =0
    while(p1 < len(list1) and p2 < len(list2)):
        if (list1[p1] == list2[p2]):
            result.append(list1[p1])
            p1+=1
            p2+=1
        elif(list1[p1] > list2[p2]):
            result.append(list2[p2])
            p2+=1
        else:
            result.append(list1[p1])
            p1+=1
    while (p1 < len(list1)):
        result.append(list1[p1])
        p1+=1
    while(p2 < len(list2)):
        result.append(list2[p2])
        p2+=1

    return result


