from random import choice as ch


def append_for(data):
    num = ch(list(data.keys()))
    data[num] -= 1
    return num
