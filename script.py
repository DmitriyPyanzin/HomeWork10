def check(n):
    if type(n) == int:
        return n

    if 'В' in n:
        return 2
    if 'Д' in n:
        return 3
    if 'К' in n:
        return 4
    return 11
