from util.title_search import get_ids_called
from query_likelyhood import QueryLikelyhoodModal

modal = QueryLikelyhoodModal()

print('query', 'recall', 'precision', 'hit', 'ground_truth', sep=',')

f = open('data/query.txt', 'r', encoding='utf-8')
recalls = []
precisions = []
for query in f.readlines():
    query = query.rstrip('\n')
    ids = get_ids_called(query)
    result = modal.get_rank(query, 10)
    count  = 0
    for i, (prob, tid) in enumerate(result):
        if str(tid) in ids:
            count += 1
    recall = count / 10
    recalls.append(recall)
    if len(ids) != 0:
        precision = count / len(ids)
    else:
        precision = 0
    precisions.append(precision)
    print(query, recall, precision, count, len(ids), sep=',')

