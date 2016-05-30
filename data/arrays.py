def minidx(iterable):
    '''Return value and index position of min value in array'''

    val, idx = min((val, idx) for (idx, val) in enumerate(iterable))
    return val, idx


def array_argsort(array, axis=0):
    '''Return index of sorted array'''

    index = list(np.ix_(*[np.arange(i) for i in array.shape]))
    index[axis] = array.argsort(axis)
    return index



