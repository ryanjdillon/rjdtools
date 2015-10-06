
class UpdateMapData(object):
    '''
    Args:
        ax:
        map_object:
        pt_data: numpy like array of lat/lon points by date
        pt_dates: numpy array of dates corresponding to pt_data
        pt_num: number of unique points in data to plot

    '''
    def __init__(self, ax, map_object, pt_data, pt_dates, pt_num):

        import datetime
        import numpy as np

        self.ax           = ax
        self.m            = map_object
        self.pt_data      = pt_data
        self.pt_dates_str = pt_dates
        self.dates        = np.empty(len(pt_dates), dtype=object)
        self.pt_num       = pt_num

        #TODO separate to methods
        # style markers
        # position date labels

        #TODO when no point data, but grid quads
        #t0 = datetime.datetime(plt_year, 01, 01)
        #self.dates = np.empty(365, dtype=object)
        #for i in range(365):
        #    self.dates[i] = t0 + datetime.timedelta(days=i)


        for i in range(len(self.pt_dates_str)):
            self.dates[i] = datetime.datetime.strptime(self.pt_dates_str[i],
                                                '%Y-%m-%d')

        # create image artist object for animation
        x,y = self.m(0,0)
        self.pts_dots = [[] for i in range(pt_num)] # animation point global list

        for i in range(self.pt_num):
            self.pts_dots[i] = m.plot(x,y, 'ro', markersize=2,
                                      markeredgewidth=0.0)[0]

        self.frame_num   = len(self.dates)
        self.date_label = ''
        self.date_label = self.ax.text(self.m.xmax*0.05, self.m.ymax*0.90, '',
                                       backgroundcolor='white', zorder = 9)

    def init(self):
        '''erases previously animated data in last step'''

        # Init point locations
        for i in range(self.pt_num):
            self.pts_dots[i].set_data([], [])

        # Init date label
        self.date_label.set_text('')

        # return elements to be removed from plot with each frame
        return self.pts_dots, self.date_label,


    def __call__(self, i):
        '''sets new values to animate with each step'''

        print 'animation frame: {0:3d}'.format(i,)
        idx = self.pt_data.date == self.pt_dates_str[i]
        pt_lons = self.pt_data.lons[idx].values
        pt_lats = self.pt_data.lats[idx].values

        # Set position data for points
        for k in range(len(pt_lons)):
            x, y = self.m(pt_lons[k],pt_lats[k])
            self.pts_dots[k].set_data(x, y)

        for k in range(len(pt_lons), self.pt_num,1):
            self.pts_dots[k].set_data([], [])

        # Create date string and set label data
        yday = self.dates[i].timetuple().tm_yday

        date_str = self.dates[i].strftime('%Y, %b %d')
        print_str = '%s (%3d)' % (date_str, yday)
        self.date_label.set_text(print_str)

        # TODO refactor
        #if save_frames == True:
        #    year = self.dates[i].year
        #    save_date = datetime.datetime(year,9,1)
        #    curr_date = self.dates[i]
        #    if save_date == curr_date:
        #        save_figs(fig, plt_prop, plt_ext, meta, i)


        return self.pts_dots, self.date_label,


def plot_norwecom(fig, ax, map_prop, plt_prop, plt_ext, g2_plons, g2_plats,
                    sa_plons=None, sa_plats=None, plot_data=False, res='l'):
    '''Plots the model study area with polygons and animated data'''

    from mpl_toolkits.basemap import Basemap
    import numpy as np

    # Define ellipsoid object for distance measurements
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    g = pyproj.Geod(ellps='WGS84') # Use WGS84 ellipsoid TODO make variable
    r_equator = g.a # earth's radius at equator
    r_poles = g.b   # earth's radius through poles

    # Map dimensions
    #~~~~~~~~~~~~~~~~
    lon0, lat0, map_width, map_height = center_map(sa_plons, sa_plats, 1.1)
    lon0, lat0, map_width, map_height = center_map(g2_plons, g2_plats, 1.1)

    # Basemap projection
    #~~~~~~~~~~~~~~~~~~~~
    #m = Basemap(projection='nplaea',boundinglat=50,lon_0=5,resolution='l')
    m = Basemap(width=map_prop['width'],height=map_prop['height'],
                rsphere=(r_equator, r_poles),\
                resolution=res, projection='laea',\
                lat_ts=map_prop['lat0'],\
                lat_0=map_prop['lat0'],lon_0=map_prop['lon0'], ax=ax)

    # Draw parallels and meridians
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    m.drawparallels(np.arange(-80.,81.,5.), labels=[1,0,0,0], fontsize=10,
                    linewidth=0.5, dashes=(None,None), color='#d6d6d6')

    m.drawmeridians(np.arange(-180.,181.,10.), labels=[0,0,0,1], fontsize=10,
                    linewidth=0.5, dashes=(None,None), color='#d6d6d6')

    m.drawmapboundary(fill_color=map_colors['water'])

    m.fillcontinents(color=map_colors['land'], lake_color=map_colors['land']) #aqua

    return m


def save_figs(fig, plt_prop, plt_ext, meta, frame):
        import datetime
        date_run = meta['date_run'].strftime('%Y-%m-%d_%H%M%S')
        out_dir = './'+date_run+'_str'+meta['strategy']+'/'
        mkdir_p(out_dir)
        #time_str = self.dates[i].strftime('%Y-%m-%d')
        out_file =        date_run + \
                   '_svn'+meta['svn'] + \
                   '_pop'+meta['population'] + \
                   '_spd'+meta['speed'] + \
                   '_str'+meta['strategy'] + \
                   '_'+ '%03d' % frame + \
                   plt_ext

        # TODO save with date and meta
        #fig.tight_layout()
        #ax = fig.get_ax
        [i.set_linewidth(0.01) for i in ax.spines.itervalues()]
        fig.savefig(out_dir+out_file, dpi=plt_prop['dpi'])


if __name__ == '__main__':

    import datetime
    import numpy as np
    import pyproj
    import string
    import matplotlib.pyplot as plt
    import matplotlib.animation as animation

    import plot_tools

    pt_dates = np.unique(whale_data['date'].values)

    # Plot configuration
    plt_dpi = 600
    plt_ext = '.png'
    alphabet = list(string.ascii_uppercase) # list of letters for subplot labeling
    today = (datetime.datetime.now()).strftime('%Y-%m-%d_%H%M%S')

    plt_colors  = {'near_black':'#2f2f2f','light_red':'#ffb2b2','light_blue':'#b2b2ff'}
    map_colors  = {'land':'#aabebe','water':'#ffffff','lake':'#aabebe'}

    # Define Plot
    fig, ax = plt.subplots()

    [i.set_linewidth(0.01) for i in ax.spines.itervalues()]

    plt_num = 0
    plt_h   = 6
    plt_w   = 6
    plt_prop = {'width':plt_w*plt_dpi, 'height':plt_h*plt_dpi, 'dpi':plt_dpi}
    map_prop = {'lon0':12.0, 'lat0':72.0, 'width':3800000, 'height':3000000}
    m = plot_norwecom(fig, ax, map_prop, plt_prop, plt_ext, res='l')

    # Animate Data
    particle_num = 50
    ud = UpdateMapData(ax, m, data, pt_dates, particle_num)

    anim = animation.FuncAnimation(fig, ud, init_func=ud.init,
                                   frames=ud.frame_num, blit=False)
    plt.show()

    #TODO savefigs
    #save_frames = False
    #out_date = meta['date_run'].strftime('%Y-%m-%d_%H%M%S')
    #out_dir = './figures/videos/'
    #vid_outfile = out_date + '.mp4'

    #fig.set_size_inches(4,4)

    #dpi = 600
    #writer = animation.writers['ffmpeg'](fps=5)

    #anim.save(out_dir+vid_outfile, writer=writer, dpi=dpi)
