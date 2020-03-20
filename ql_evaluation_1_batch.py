from util.title_search import get_ids_called
from query_likelihood import QueryLikelihoodModal

modal = QueryLikelihoodModal()

print('k', 'recall', 'precision', sep=',')

f = open('data/query.txt', 'r', encoding='utf-8')
querys = f.readlines()
for k in range(1, 30):
    precisions = []
    recalls = []
    for query in querys:
        query = query.rstrip('\n')
        ids = get_ids_called(query)
        result = modal.get_rank(query, k, smoothing=False)
        count  = 0
        for i, (prob, tid) in enumerate(result):
            if str(tid) in ids:
                count += 1
        precision = count / k
        precisions.append(precision)
        if len(ids) != 0:
            recall = count / len(ids)
        else:
            recall = 0
        recalls.append(recall)
        # print(query, recall, precision, count, len(ids), sep=',')
    print(k,  sum(recalls) / len(recalls) if len(recalls)!=0 else 0, sum(precisions) / len(precisions) if len(precisions)!=0 else 0, sep=',')