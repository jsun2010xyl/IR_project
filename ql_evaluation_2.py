from query_likelyhood import QueryLikelyhoodModal

modal = QueryLikelyhoodModal()

print('query', 'precision', 'recall', 'hit', 'ground_truth', sep=',')

f = open('data/query.txt', 'r', encoding='utf-8')
for query in f.readlines():
    query = query.rstrip('\n')
    result = modal.get_rank(query)
    count  = 0
    gt = 0
    k = 100
    for i, (prob, tid) in enumerate(result):
        if i < k and prob != 0:
            count += 1
        if prob != 0:
            gt += 1
    precision = count / k
    if gt != 0:
        recall = count / gt
    else:
        recall = 0
    print(query, precision, recall, count, gt, sep=',')

