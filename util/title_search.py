def get_ids_called(title):
    ids = []
    f = open('data/mxm_779k_matches.txt', "r", encoding='utf-8')
    for line in f.readlines():
        line = line.rstrip('\n')
        if line[0] == '#':
            continue
        tid1, artist1, title1, tid2, artist2, title2 = line.split('<SEP>')
        if title2.lower() == title.lower():
            ids.append(tid2)
    return ids

# print(get_ids_called('Dream'))
# print(get_ids_called('dangerous'))
# print(get_ids_called('why'))