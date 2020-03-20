from util.title_search import get_ids_called
from query_likelyhood import QueryLikelyhoodModal

modal = QueryLikelyhoodModal()

print('query', 'precision', 'recall', 'hit', 'ground_truth', sep=',')

f = open('data/query.txt', 'r', encoding='utf-8')
for query in f.readlines():
    query = query.rstrip('\n')
    ids = get_ids_called(query)
    result = modal.get_rank(query, 10)
    count  = 0
    for i, (prob, tid) in enumerate(result):
        if str(tid) in ids:
            count += 1
    precision = count / 10
    if len(ids) != 0:
        recall = count / len(ids)
    else:
        recall = 0
    print(query, precision, recall, count, len(ids), sep=',')

