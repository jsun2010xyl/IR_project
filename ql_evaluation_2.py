from query_likelyhood import QueryLikelyhoodModal

modal = QueryLikelyhoodModal()

print('query', 'recall', 'precision', 'hit', 'ground_truth', sep=',')

f = open('data/query.txt', 'r', encoding='utf-8')
recalls = []
precisions = []
for query in f.readlines():
    query = query.rstrip('\n')
    result = modal.get_rank(query)
    count  = 0
    gt = 0
    for i, (prob, tid) in enumerate(result):
        if i < 10 and prob != 0:
            count += 1
        if prob != 0:
            gt += 1
    recall = count / 10
    recalls.append(recall)
    if gt != 0:
        precision = count / gt
    else:
        precision = 0
    precisions.append(precision)
    print(query, recall, precision, count, gt, sep=',')

