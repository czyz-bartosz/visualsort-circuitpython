import os

def array_shuffle(arr):
    for i in range(len(arr) - 1, 0, -1):
        j = get_random(0, i)
        arr[i], arr[j] = arr[j], arr[i]
    return arr


def get_random(start, stop):
    return int.from_bytes(os.urandom(2), "big") % stop + start
