from query_likelihood import QueryLikelihoodModal

modal = QueryLikelihoodModal()

print('query', 'recall', 'precision', 'hit', 'ground_truth', sep=',')

f = open('data/query.txt', 'r', encoding='utf-8')
querys = f.readlines()
for k in range(1, 30):
    recalls = []
    precisions = []
    for query in querys:
        query = query.rstrip('\n')
        result = modal.get_rank(query, smoothing=False)
        count  = 0
        gt = 0
        for i, (prob, tid) in enumerate(result):
            if i < k and prob != 0:
                count += 1
            if prob != 0:
                gt += 1
        recall = count / k
        recalls.append(recall)
        if gt != 0:
            precision = count / gt
        else:
            precision = 0
        precisions.append(precision)
    print(k,  sum(recalls) / len(recalls) if len(recalls)!=0 else 0, sum(precisions) / len(precisions) if len(precisions)!=0 else 0, sep=',')

