
def bootstrap(data, k, n):
    if n is None:
        n = len(data)
    ret = []
    for _ in range(k):
        ret.append(data.sample(n=n, replace=True, random_state=17))
    return ret
