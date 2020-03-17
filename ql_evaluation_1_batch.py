from util.title_search import get_ids_called
from query_likelyhood import QueryLikelyhoodModal

modal = QueryLikelyhoodModal()

print('k', 'recall', 'precision', sep=',')

f = open('data/query.txt', 'r', encoding='utf-8')
for k in [3, 10, 20, 50, 100, 200, 500, 1000]:
    recalls = []
    precisions = []
    for query in f.readlines():
        query = query.rstrip('\n')
        ids = get_ids_called(query)
        result = modal.get_rank(query, k)
        count  = 0
        for i, (prob, tid) in enumerate(result):
            if str(tid) in ids:
                count += 1
        recall = count / k
        recalls.append(recall)
        if len(ids) != 0:
            precision = count / len(ids)
        else:
            precision = 0
        precisions.append(precision)
        # print(query, recall, precision, count, len(ids), sep=',')
    print(k, 'recall', 'precision', sep=',')

