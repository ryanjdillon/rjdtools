def autocrop_img(filename):
    '''Call ImageMagick mogrify from bash to autocrop image'''
    import subprocess
    import os

    cwd, img_name = os.path.split(filename)

    bashcmd = 'mogrify -trim %s' % img_name
    process = subprocess.Popen(bashcmd.split(), stdout=subprocess.PIPE, cwd=cwd)
    #output = process.communicate()[0]
    #print output


def urlify(s):
     import re

     # Remove all non-word characters (everything except numbers and letters)
     s = re.sub(r"[^\w\s]", '', s)
     # Replace all runs of whitespace with an underscore
     s = (re.sub(r"\s+", '_', s)).lower()
     return s
