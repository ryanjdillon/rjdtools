
def get_fig_name(out_dir, plt_ext):
    '''Generate a figure output name with current date'''

    import datetime

    today = datetime.datetime.now()
    today_str = datetime.datetime.strftime(today,'%Y-%m-%d_%H%M%S')

    fig_name = out_dir + today_str + plt_ext

    return fig_name


def save_fig(out_file, dpi, crop=True):

    import plot_tools.format as ptformat
    import matplotlib.pyplot as plt

    # Save and crop
    plt.savefig(out_file, dpi=dpi)
    ptformat.autocrop_img(out_file)


def autocrop_img(filename, output=False):
    '''Call ImageMagick mogrify from bash to autocrop image'''

    import subprocess
    import os

    cwd, img_name = os.path.split(filename)

    bashcmd = 'mogrify -trim %s' % img_name
    process = subprocess.Popen(bashcmd.split(), stdout=subprocess.PIPE, cwd=cwd)

    if output==True:
        output = process.communicate()[0]
        print output


def set_border_width(ax, linewidth=0.1):
    '''Sets width of border lines to specified width'''

    [i.set_linewidth(linewidth) for i in ax.spines.itervalues()]

    return None


def urlify(string):
    '''Replace whitespace and special characters in a string'''

    import re

    # Remove all characters except numbers and letters'''
    string = re.sub(r"[^\w\s]", '', string)
    # Replace all runs of whitespace with an underscore
    string = (re.sub(r"\s+", '_', s)).lower()

    return s
