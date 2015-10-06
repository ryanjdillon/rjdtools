def plotimage(filename, mapobject, x, y):
    '''Plot image to map_object'''

    import Image
    image = np.array(Image.open(filename))
    im = OffsetImage(image, zoom=1)
    ab = AnnotationBbox(im, (x, y), xycoords='data', frameon=False)

    m._check_ax().add_artist(ab)


def draw_contour(ax, map_object, lons, lats, vals, plt_alpha, cmap):
    '''Ploat values as interpolated color gradient'''

    import numpy as np
    import matplotlib.pyplot as plt
    import scipy

    #TODO calc and save as .bin levels/norm

    # requires 2d (meshed) input arrays
    x, y = map_object(lons,lats)
    levels=np.arange(20000, 7500000, 500)#(2,18,0.5)

    #density_img = plt.imshow(vals)#,interpolation='nearest',
                             #cmap = cmap)#,norm=norm)

    # TODO use ax instead of map object?
    return map_object.contourf(x, y, vals, levels, cmap = cmap,#cm.jet,
                               extend = 'upper', alpha=plt_alpha,
                               antialiased=True)


def draw_mesh(ax, x, y, vals, plt_alpha, cmap):
    '''Plots data as grid'''

    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.colors import BoundaryNorm

    #TODO calc and save as .bin levels/norm

    vmin = 20000
    vmax = 7500000
    # requires 2d (meshed) input arrays
    levels=np.arange(vmin, vmax, 500)#(2,18,0.5)
    #norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)

    return ax.pcolormesh(x, y, vals, vmin=1.)#, cmap=cmap)#, alpha=plt_alpha)


def center_map(lons,lats,scale):
    '''Automatically determin dimensions of map.

       Assumes -90 < Lat < 90 and -180 < Lon < 180, and
       latitude and logitude are in decimal degrees'''

    import numpy as np
    import pyproj

    # TODO add cond to set width to either pythag or direct width

    north_lat = np.max(lats)
    south_lat = np.min(lats)
    west_lon =  np.max(lons)
    east_lon =  np.min(lons)

    # find center of data
    # average between max and min longitude
    lon0 = ((west_lon-east_lon)/2.0)+east_lon

    # define ellipsoid object for distance measurements
    g = pyproj.Geod(ellps='WGS84') # Use WGS84 ellipsoid TODO make variable
    earth_radius = g.a # earth's radius in meters

    # Use pythagorean theorom to determine height of plot
    # divide b_dist by 2 to get width of triangle from center to edge of data
    # area
    # inv returns [0]forward azimuth, [1]back azimuth, [2]distance between

    # a_dist = the height of the map (i.e. mapH)
    b_dist = g.inv(west_lon, north_lat, east_lon, north_lat)[2]/2
    c_dist = g.inv(west_lon, north_lat, lon0, south_lat)[2]

    mapH = pow(pow(c_dist,2)-pow(b_dist,2),1./2)
    lat0 = g.fwd(lon0,south_lat,0,mapH/2)[1]

    # distance between max E and W longitude at most southern latitude
    mapW = g.inv(west_lon, south_lat, east_lon, south_lat)[2]

    return lon0, lat0, mapW, mapH
