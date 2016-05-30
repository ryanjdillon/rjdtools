def structured_shape(x):
    if x.dtype.fields is not None:
        return list(x.shape) + [len(x.dtype.fields)]
    else:
        return x.shape
