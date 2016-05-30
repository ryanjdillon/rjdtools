def print_pandas_table(data_frame):
    '''Prints pandas dataframe to table in console'''

    from StringIO import StringIO
    import prettytable

    output = StringIO()
    data_frame.to_csv(output)
    output.seek(0)
    pt = prettytable.from_csv(output)
    print pt
