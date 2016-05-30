

def file_list(source, pattern):
    '''Generates a list of files recursively from a root directory

    Args:
        source: String root directory name
        pattern: (see example)
    Example:
        pattern = re.compile('.*\.(mov|MOV|avi|mpg)$')
    '''
    matches = []
    for root, dirnames, filenames in os.walk(source):
        for filename in filter(lambda name:pattern.match(name),filenames):
            matches.append(os.path.join(root, filename))
    return matches

def recursive_move(src, dest, pattern):
    '''Recursively moves files by extension
    Args:
        src (str): String source directory
        dest (str): String destination directory
        pattern: (see example)
    Example:
        pattern = re.compile('.*\.(mov|MOV|avi|mpg)$')
    '''
    import directories
    import os
    import numpy as np

    filelist = file_list(src, pattern)

    for f in file_list:
        d, name = os.split(f)
        name, ext = os.path.splitext(f)
        child_dir = os.path.split(d)
        dest_dir = dest+child_dir

        # Replace src with dest in file path
        #if !exist create dest/child_d
        directories.mkdir_p(dest_dir)
        #mv file dest/child_d
        os.rename(f, dest_dir+name+ext)
