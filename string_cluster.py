import numpy as np

from collections import defaultdict
from sklearn.cluster import dbscan


def jaro(s, t):

    s_len = len(s)
    t_len = len(t)

    if s_len == 0 and t_len == 0:
        return 1

    match_distance = (max(s_len, t_len) // 2) - 1

    s_matches = [False] * s_len
    t_matches = [False] * t_len

    matches = 0
    transpositions = 0

    for i in range(s_len):
        start = max(0, i - match_distance)
        end = min(i + match_distance + 1, t_len)

        for j in range(start, end):
            if t_matches[j]:
                continue
            if s[i] != t[j]:
                continue
            s_matches[i] = True
            t_matches[j] = True
            matches += 1
            break

    if matches == 0:
        return 0

    k = 0
    for i in range(s_len):
        if not s_matches[i]:
            continue
        while not t_matches[k]:
            k += 1
        if s[i] != t[k]:
            transpositions += 1
        k += 1

    return ((matches / s_len) +
            (matches / t_len) +
            ((matches - transpositions / 2) / matches)) / 3


s = ['NEW YORK', 'NEW YORK CITY', 'N YORK', 'SEATTLE', 'SEATTLE CITY']


def jaro_metric(x, y):
    i, j = int(x[0]), int(y[0])
    return 1 - jaro(data[i], data[j])


def get_clusters(string_seq, metric=jaro_metric, eps=0.15):
    X = np.arange(len(string_seq)).reshape(-1, 1)
    global data
    data = string_seq
    classes, labels = dbscan(X, metric=metric, eps=eps, min_samples=2)
    clusters = defaultdict(list)

    for string, label in zip(string_seq, labels):
        clusters[label].append(string)

    return clusters


print(get_clusters(s))


