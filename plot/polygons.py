def plot_lines(ax, line_list, line_color='white'):
    '''Plot list of shapely lines to matplotlib figure axis

    Args:
        ax: matplotlib axis object
        line_list: shapely MultiLineString object
        line_color: color of lines to be plotted
    '''
    for line in line_list:
        x, y = line.xy
        ax.plot(x, y, color=line_color, alpha=0.7, linewidth=0.5,
                solid_capstyle='round', zorder=2)


def plot_polygon(ax, grid_poly_x, grid_poly_y, poly_color, poly_alpha):
    '''Draw polygon on plot_object'''

    from matplotlib.patches import Polygon
    import matplotlib.pyplot as plt

    #grid_poly_x, grid_poly_y = map_object(grid_plons, grid_plats)
    grid_poly_xy = zip(grid_poly_x, grid_poly_y)
    grid_poly = Polygon(grid_poly_xy, edgecolor=poly_color, facecolor='none',
                        linewidth=1.5, alpha=poly_alpha)
    #plt.gca().add_patch(grid_poly)
    ax.add_patch(grid_poly)


def polygon2mask(grid_lons,grid_lats, mask_polygon, mask_outfile=''):
    '''Create a mask array from polygon(s) on given grid

       if mutliple polygons are used, pass in a list of polygons'''

    import pandas as pd
    import numpy as np
    from shapely.geometry import Polygon, Point, MultiLineString
    import pyproj

    # Create a list if single polygon passed
    if not hasattr(mask_polygon, "__iter__"):
        poly_list = [mask_polygon,]
    else:
        poly_list = mask_polygon

    # Initiate array to store boolean values to
    mask = np.zeros_like(grid_lons)

    #  Get shape of grid for iteration
    x, y = grid_lons.shape

    # WGS84 datum
    wgs84 = pyproj.Proj(init='EPSG:4326')

    # Albers Equal Area Conic (aea)
    nplaea = pyproj.Proj("+proj=laea +lat_0=90 +lon_0=-40 +x_0=0 +y_0=0 \
                       +ellps=WGS84 +datum=WGS84 +units=m +no_defs")

    # Transform polygon and grid coordinates to northern lat AEAC projection
    grid_x_mesh, grid_y_mesh = pyproj.transform(wgs84, nplaea, grid_lons, grid_lats)

    # Step through elements in grid to evaluate if in the study area
    for polygon in poly_list:
        for i in range(x):
            for j in range(y):
                grid_point = Point(grid_x_mesh[i][j], grid_y_mesh[i][j])
                if grid_point.within(polygon):
                    mask[i][j] = 1

    mask_2d = np.flipud(mask)

    if (len(mask_outfile)>0):
        print '\nCreate Panda Dataframes...'
        mask_df = pd.DataFrame(mask)

        print '\nStarting file creation...'
        mask_df.to_csv(mask_outfile, index=False, sep=',', header=False)

    print '\nMask dimensions and num cells contained:'
    print 'Mask shape', mask_2d.shape
    print 'Points within polygon ', len(mask_2d[mask==1])
    print 'Points out of polygon ', len(mask_2d[mask==0])

    return mask_2d


