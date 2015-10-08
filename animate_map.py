
class AnimateMap(object):
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
        self.dates        = np.unique(pt_dates)
        self.pt_num       = pt_num

        #TODO separate to methods
        # style markers
        # position date labels

        #TODO when no point data, but grid quads
        #t0 = datetime.datetime(plt_year, 01, 01)
        #self.dates = np.empty(365, dtype=object)
        #for i in range(365):
        #    self.dates[i] = t0 + datetime.timedelta(days=i)


        #for i in range(len(self.pt_dates_str)):
        #    self.dates[i] = datetime.datetime.strptime(self.pt_dates_str[i],
        #                                        '%Y-%m-%d')

        # create image artist object for animation
        x,y = self.m(0,0)
        self.pts_dots = [[] for i in range(pt_num)] # animation point global list

        for i in range(self.pt_num):
            self.pts_dots[i] = self.m.plot(x,y, 'ro', markersize=2,
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
        idx = self.pt_data.date == self.dates[i]
        pt_lons = self.pt_data.lon[idx].values
        pt_lats = self.pt_data.lat[idx].values

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


def save_frames(fig, plt_prop, plt_ext, meta, frame):

        import datetime
        import plot_tools.format as ptformat

        date_run = meta['date_run'].strftime('%Y-%m-%d_%H%M%S')
        out_dir = './'+date_run+'_str'+meta['strategy']+'/'
        mkdir_p(out_dir)

        #time_str = self.dates[i].strftime('%Y-%m-%d')

        out_file = date_run + \
                   '_svn'+meta['svn'] + \
                   '_pop'+meta['population'] + \
                   '_spd'+meta['speed'] + \
                   '_str'+meta['strategy'] + \
                   '_'+ '%03d' % frame + \
                   plt_ext

        # TODO save with date and meta
        ax = fig.get_ax
        ptformat.set_border_width(ax, linewidth=0.1)

        out_file = out_dir+out_file

        fig.savefig(out_file, dpi=plt_prop['dpi'])
        ptformat.autocrop_img(out_file)

        return None


def save_animation(outfile, anim_object, dpi, fps):
    '''Save matplotlib animation to video file'''

    # TODO autocrop border
    # http://www.renevolution.com/understanding-ffmpeg-part-iii-cropping/

    import matplotlib.animation as animation

    writer = animation.writers['ffmpeg'](fps=fps)
    anim_object.save(outfile, writer=writer, dpi=dpi)

    return None


def get_sample_data(num_days, num_particles, lon_start, lat_start):

    import pandas as pd
    import numpy as np
    import random
    import datetime

    dates = [datetime.datetime.now().date() + \
             datetime.timedelta(days=i) for i in range(num_days)]

    dfs = list()
    for i in range(num_particles):
        particle_ids = [i for _ in range(num_days)]
        lons = list()
        lats = list()
        for k in range(num_days):
            lon_start += random.random()*random.choice([-1,1])
            lat_start += random.random()*random.choice([-1,1])
            lons.append(lon_start)
            lats.append(lat_start)
            data_array = np.array([dates, particle_ids,lons, lats]).T
            dfs.append(pd.DataFrame(data_array))

    data = pd.concat(dfs, ignore_index=True)
    data.columns = ['date', 'id', 'lon', 'lat']

    return data, dates


if __name__ == '__main__':

    import matplotlib.pyplot as plt
    import plot_tools.maps as ptmaps
    import matplotlib.animation as animation

    # Generate example data
    data, dates = get_sample_data(60, 20, 10.0, 62.0)

    # Define Plot
    fig, ax = plt.subplots()

    # Create basemap
    map_props  = ptmaps.center_basemap(data['lon'], data['lat'], 1.2, True)
    map_colors = ptmaps.get_mapcolors()

    m = ptmaps.draw_basemap(ax, map_prop, map_colors, res='l')

    # Animate Data
    ud = AnimateMap(ax, m, data, dates, 20)

    anim = animation.FuncAnimation(fig, ud, init_func=ud.init,
                                   frames=ud.frame_num, blit=False)

    plt.show()
