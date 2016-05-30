def grid_polycoords(grid_lons,grid_lats):
    '''Returns external coordinates of grid positions to create polygon'''

    import pyproj
    from shapely.geometry import Polygon

    # TODO it may be unessecary to project the points and create Polygon

    # Create lists to append external coordinates to
    grid_x = list()
    grid_y = list()

    # WGS84 datum
    wgs84 = pyproj.Proj(init='EPSG:4326')

    # Albers Equal Area Conic (aea)
    nplaea = pyproj.Proj("+proj=laea +lat_0=90 +lon_0=-40 +x_0=0 +y_0=0 \
                       +ellps=WGS84 +datum=WGS84 +units=m +no_defs")

    # Transform points to create Polygon
    grid_x_mesh, grid_y_mesh = pyproj.transform(wgs84, nplaea, grid_lons,
                                                               grid_lats)
    # Get grid's exterior projected x coordinate values
    [grid_x.append(i) for i in grid_x_mesh[0,:]]
    [grid_x.append(i) for i in grid_x_mesh[1:-1,-1]]
    # The following are read in reverse order to keep position in sequence
    [grid_x.append(i) for i in (grid_x_mesh[-1,:])[::-1]]
    [grid_x.append(i) for i in (grid_x_mesh[1:-1,0])[::-1]]

    # Get grid's exterior projected y coordinate values
    [grid_y.append(i) for i in grid_y_mesh[0,:]]
    [grid_y.append(i) for i in grid_y_mesh[1:-1,-1]]
    # The following are read in reverse order to keep position in sequence
    [grid_y.append(i) for i in (grid_y_mesh[-1,:])[::-1]]
    [grid_y.append(i) for i in (grid_y_mesh[1:-1,0])[::-1]]

    # Create polygon
    grid_poly = Polygon(zip(grid_x, grid_y))
    grid_x, grid_y = grid_poly.exterior.coords.xy

    poly_lons, poly_lats = pyproj.transform(nplaea, wgs84, grid_x,
                                                           grid_y)
    return poly_lons, poly_lats, grid_poly


def plot_lines(ax, line_list, line_color, line_width=0.5, line_style='-'):
    '''Plot polygon lines'''

    for line in line_list:
        x, y = line.xy
        ax.plot(x, y, linestyle=line_style, color=line_color, linewidth=0.5,
                solid_capstyle='round', zorder=2)


def grid_lines(grid_lons, grid_lats, x_intv, y_intv):
    '''Creates polygon lines of grid at given x and y intervals

    Args:
        grid_lons (float): A list of WSG84 grid longitudes (grid x dimension)
        grid_lats (float): A list WSG84 grid latitudes (grid y dimension)
        x_intv (int): The indexing  interval from which values will be
            retrieved from grid_lons
        y_intv (int): The indexing  interval from which values will be
            retrieved from grid_lats

    Returns:
        grid_lines: a list of tuples defining longitudinal and latitudinal grid
        lines at intervals x_intv and y_intv
    '''

    import pyproj
    from shapely.geometry import MultiLineString

    # TODO fix indexing with x,y reveresed

    grid_lines = list()

    # Append tuples with coordinates of defining latitudinal lines
    x_len, y_len = grid_lons.shape
    for i in range(x_intv-1, x_len, x_intv):
        y_line = list()
        for lx,ly in zip(grid_lons[i,:], grid_lats[i,:]):
            y_line.append((ly,lx))
        grid_lines.append(y_line)

    # Append tuples with coordinates of defining longitudinal lines
    for i in range(y_intv-1, y_len, y_intv):
        x_line = list()
        for lx,ly in zip(grid_lons[:,i], grid_lats[:,i]):
            x_line.append((ly,lx))
        grid_lines.append(x_line)

    grid_lines = MultiLineString(grid_lines)

    return grid_lines


def calc_psi_coords(lons, lats):
    ''' Calcuate psi points from centered grid points'''

    import numpy as np
    import pyproj

    # Create Geod object with WGS84 ellipsoid
    g = pyproj.Geod(ellps='WGS84')

    # Get grid field dimensions
    ydim, xdim = lons.shape

    # Create empty coord arrays
    lons_psi = np.zeros((ydim+1, xdim+1))
    lats_psi = np.zeros((ydim+1, xdim+1))

    # Calculate internal points
    #--------------------------
    for j in range(ydim-1):
        for i in range(xdim-1):
            lon1 = lons[j,i]     # top left point
            lat1 = lats[j,i]
            lon2 = lons[j+1,i+1] # bottom right point
            lat2 = lats[j+1,i+1]
            # Calc distance between points, find position at half of dist
            fwd_az, bck_az, dist = g.inv(lon1,lat1,lon2,lat2)
            lon_psi, lat_psi, bck_az = g.fwd(lon1,lat1,fwd_az,dist*0.5)
            # Assign to psi interior positions
            lons_psi[j+1,i+1] = lon_psi
            lats_psi[j+1,i+1] = lat_psi

    # Caclulate external points (not corners)
    #----------------------------------------
    for j in range(ydim):
        # Left external points
        #~~~~~~~~~~~~~~~~~~~~~
        lon1 = lons_psi[j+1,2] # left inside point
        lat1 = lats_psi[j+1,2]
        lon2 = lons_psi[j+1,1] # left outside point
        lat2 = lats_psi[j+1,1]
        # Calc dist between points, find position at dist*2 from pos1
        fwd_az, bck_az, dist = g.inv(lon1,lat1,lon2,lat2)
        lon_psi, lat_psi, bck_az = g.fwd(lon1,lat1,fwd_az,dist*2.)
        lons_psi[j+1,0] = lon_psi
        lats_psi[j+1,0] = lat_psi

        # Right External points
        #~~~~~~~~~~~~~~~~~~~~~~
        lon1 = lons_psi[j+1,-3] # right inside point
        lat1 = lats_psi[j+1,-3]
        lon2 = lons_psi[j+1,-2] # right outside point
        lat2 = lats_psi[j+1,-2]
        # Calc dist between points, find position at dist*2 from pos1
        fwd_az, bck_az, dist = g.inv(lon1,lat1,lon2,lat2)
        lon_psi, lat_psi, bck_az = g.fwd(lon1,lat1,fwd_az,dist*2.)
        lons_psi[j+1,-1] = lon_psi
        lats_psi[j+1,-1] = lat_psi

    for i in range(xdim):
        # Top external points
        #~~~~~~~~~~~~~~~~~~~~
        lon1 = lons_psi[2,i+1] # top inside point
        lat1 = lats_psi[2,i+1]
        lon2 = lons_psi[1,i+1] # top outside point
        lat2 = lats_psi[1,i+1]
        # Calc dist between points, find position at dist*2 from pos1
        fwd_az, bck_az, dist = g.inv(lon1,lat1,lon2,lat2)
        lon_psi, lat_psi, bck_az = g.fwd(lon1,lat1,fwd_az,dist*2.)
        lons_psi[0,i+1] = lon_psi
        lats_psi[0,i+1] = lat_psi

        # Bottom external points
        #~~~~~~~~~~~~~~~~~~~~~~~
        lon1 = lons_psi[-3,i+1] # bottom inside point
        lat1 = lats_psi[-3,i+1]
        lon2 = lons_psi[-2,i+1] # bottom outside point
        lat2 = lats_psi[-2,i+1]
        # Calc dist between points, find position at dist*2 from pos1
        fwd_az, bck_az, dist = g.inv(lon1,lat1,lon2,lat2)
        lon_psi, lat_psi, bck_az = g.fwd(lon1,lat1,fwd_az,dist*2.)
        lons_psi[-1,i+1] = lon_psi
        lats_psi[-1,i+1] = lat_psi

    # Calculate corners:
    #-------------------
    # top left corner
    #~~~~~~~~~~~~~~~~
    lon1 = lons_psi[2,2] # bottom right point
    lat1 = lats_psi[2,2]
    lon2 = lons_psi[1,1] # top left point
    lat2 = lats_psi[1,1]
    # Calc dist between points, find position at dist*2 from pos1
    fwd_az, bck_az, dist = g.inv(lon1,lat1,lon2,lat2)
    lon_psi, lat_psi, bck_az = g.fwd(lon1,lat1,fwd_az,dist*2.)
    lons_psi[0,0] = lon_psi
    lats_psi[0,0] = lat_psi
    # top right corner
    #~~~~~~~~~~~~~~~~~
    lon1 = lons_psi[2,-3] # bottom left point
    lat1 = lats_psi[2,-3]
    lon2 = lons_psi[1,-2] # top right point
    lat2 = lats_psi[1,-2]
    # Calc dist between points, find position at dist*2 from pos1
    fwd_az, bck_az, dist = g.inv(lon1,lat1,lon2,lat2)
    lon_psi, lat_psi, bck_az = g.fwd(lon1,lat1,fwd_az,dist*2.)
    lons_psi[0,-1] = lon_psi
    lats_psi[0,-1] = lat_psi
    # bottom left corner
    #~~~~~~~~~~~~~~~~~~~
    lon1 = lons_psi[-3,2] # top right point
    lat1 = lats_psi[-3,2]
    lon2 = lons_psi[-2,1] # bottom left point
    lat2 = lats_psi[-2,1]
    # Calc dist between points, find position at dist*2 from pos1
    fwd_az, bck_az, dist = g.inv(lon1,lat1,lon2,lat2)
    lon_psi, lat_psi, bck_az = g.fwd(lon1,lat1,fwd_az,dist*2.)
    lons_psi[-1,0] = lon_psi
    lats_psi[-1,0] = lat_psi
    # bottom right corner
    #~~~~~~~~~~~~~~~~~~~~
    lon1 = lons_psi[-3,-3] # top left point
    lat1 = lats_psi[-3,-3]
    lon2 = lons_psi[-2,-2] # bottom right point
    lat2 = lats_psi[-2,-2]
    # Calc dist between points, find position at dist*2 from pos1
    fwd_az, bck_az, dist = g.inv(lon1,lat1,lon2,lat2)
    lon_psi, lat_psi, bck_az = g.fwd(lon1,lat1,fwd_az,dist*2.)
    lons_psi[-1,-1] = lon_psi
    lats_psi[-1,-1] = lat_psi

    return lons_psi, lats_psi


def regrid_idxs(grid1_lons, grid1_lats, grid2_lons, grid2_lats):
    '''Generate an array with dimensions of grid1 containing index positions
       of nearest cell positions in grid2 '''

    import numpy as np

    idxfile = 'regrid_idxs.bin'

    # if no pickle file available, perform operations
    try:
        with open(idxfile, 'rb') as infile:
            regrid_idx_array = np.load(infile)

    # if pickle fail available, load data to return
    except IOError as e:
        print("     ({})".format(e))

        print '     grid1 shape', grid1_lons.shape
        print '     grid2 shape', grid2_lons.shape

        grid1_y, grid1_x = grid1_lons.shape
        grid2_y, grid2_x = grid2_lons.shape

        dist = np.zeros((grid2_y, grid2_x))
        regrid_idx_array = np.empty((grid1_y, grid1_x), dtype=object)

        # Define ellipsoid to use for distance calculations
        g = pyproj.Geod(ellps='WGS84')

        # Loop through each cell in grid1
        print '\n     Create re-gridding indexes...'
        for y in range(grid1_y):
            for x in range(grid1_x):
                grid1_lon = grid1_lons[y][x]
                grid1_lat = grid1_lats[y][x]
                # Compare each grid 1 cell to all grid2 cells
                for yy in range(grid2_y):
                    for xx in range(grid2_x):
                        grid2_lon = grid2_lons[yy][xx]
                        grid2_lat = grid2_lats[yy][xx]
                        # Assign distance between old lat/lon and new lat/lons to array
                        fwd_az, bck_az, dist[yy][xx] = g.inv(grid1_lon,grid1_lat,
                                                             grid2_lon,grid2_lat)
                # find the lowest distance value in array by the default axis
                amin = dist.argmin()
                # divide num of cells in x direction by low position = idxs
                grid2_idx_y, grid2_idx_x = divmod(amin, grid2_x)
                # For each old grid position, store new grid index position
                regrid_idx_array[y][x] = (grid2_idx_y, grid2_idx_x)

        np.save(open(idxfile, 'wb'), regrid_idx_array)

    return regrid_idx_array


def create_coords(lon_start, lat_start, lon_end, lat_end, cells_w ,cells_h ):
    ''' Create arrays of latitude and longitude from bounds and cell dimensions'''

    # Create sequence of lon/lat from center of cells
    # "mesh" to create a grid from num of lons and num of lats
    # add +1 gives boundary vals to cells with correct number of cells
    lons = np.linspace(lon_start, lon_end, num = num_cells_w+1)[:num_cells_w]
    lats = np.linspace(lat_start, lat_end, num = num_cells_h+1)[:num_cells_h]
    lons,lats =  np.meshgrid(lons,lats)

    # Change grid to linear array of values, then repeat for each day in file
    # Shift coordinate position to center of cells
    lons = np.tile(np.ravel(lons), num_days) + (lon_cellsize/2.)
    lats = np.tile(np.ravel(lats), num_days) - (lat_cellsize/2.)

    return lons, lats, lon_cellsize, lat_cellsize


def calc_grid_res(grid_lons, grid_lats):
    '''Returnds arrays of horizontal and vertical min, max & avg resolutions'''
    import pyproj
    import numpy as np

    grid_y, grid_x = grid_lons.shape

    g = pyproj.Geod(ellps='WGS84')

    row_dists = np.zeros(grid_y*(grid_x-1))
    col_dists = np.zeros(grid_x*(grid_y-1))
    vert_res = np.zeros(3)
    horiz_res = np.zeros(3)

    for y in range(grid_y):
        for x in range(grid_x-1):
            lon1 = grid_lons[y,x]
            lat1 = grid_lats[y,x]
            lon2 = grid_lons[y,x+1]
            lat2 = grid_lats[y,x+1]
            fwd_az, back_az, dist =  g.inv(lon1, lat1, lon2, lat2)
            row_dists[x+(y*(grid_x-1))] = dist

    for x in range(grid_x):
        for y in range(grid_y-1):
            lon1 = grid_lons[y,x]
            lat1 = grid_lats[y,x]
            lon2 = grid_lons[y+1,x]
            lat2 = grid_lats[y+1,x]
            fwd_az, back_az, dist =  g.inv(lon1, lat1, lon2, lat2)
            col_dists[y+(x*(grid_y-1))] = dist

    #TODO make sure calc here isn't in error with diff lons/lats
    lon_cellsize = abs(grid_lons[0][0] - grid_lons[0][1])
    lat_cellsize = abs(grid_lats[0][0] - grid_lats[1][0])

    # Calculate the cell area in m^2
    cell_area = np.empty_like(grid_lons)
    cell_area[:] = -999.0
    y,x = grid_lons.shape
    for i in range(y):
        for j in range(x):
            lon = grid_lons[i][j]
            lat = grid_lats[i][j]
            fwd_az, back_az, cell_width =  g.inv(lon, lat,
                                                 lon+lon_cellsize, lat)

            fwd_az, back_az, cell_height = g.inv(lon, lat,
                                                 lon, lat-lat_cellsize)

            cell_area[i][j] = cell_width * cell_height

    vert_res[0] = np.amin(row_dists)
    vert_res[1] = np.amax(row_dists)
    vert_res[2] = np.average(row_dists)

    horiz_res[0] = np.amin(col_dists)
    horiz_res[1] = np.amax(col_dists)
    horiz_res[2] = np.average(col_dists)

    return vert_res, horiz_res, cell_area


def regrid(g1_data, g2_shape):
    '''Regrid 2d data from old to new norewcom grids'''

    regrid_idx_array = np.load('regrid_idxs.bin')

    g1_y, g1_x = g1_data.shape
    g2_y, g2_x = g2_shape

    g2_data = np.zeros((g2_y,g2_x))

    for y in range(g1_y):
        for x in range(g1_x):
            new_y, new_x = regrid_idx_array[y][x]
            g2_data[new_y][new_x] = g1_data[y][x]
    return g2_data


def calc_cell_areas(mesh_lons, mesh_lats, cells_w, cells_h, num_days):
    ''' Calculate cell areas as rectangles
    '''
    import pyproj
    import numpy as np

    # Define ellipsoid
    g = pyproj.Geod(ellps='WGS84')

    #TODO make sure calc here isn't in error with diff lons/lats
    lon_cellsize = abs(mesh_lons[0][0] - mesh_lons[0][1])
    lat_cellsize = abs(mesh_lats[0][0] - mesh_lats[1][0])

    # Calculate the cell area in m^2
    cell_area = np.empty_like(mesh_lons)
    cell_area[:] = -999.0
    y,x = mesh_lons.shape
    for i in range(y):
        for j in range(x):
            lon = mesh_lons[i][j]
            lat = mesh_lats[i][j]
            fwd_az, back_az, cell_width =  g.inv(lon, lat,
                                                 lon+lon_cellsize, lat)

            fwd_az, back_az, cell_height = g.inv(lon, lat,
                                                 lon, lat-lat_cellsize)

            cell_area[i][j] = cell_width * cell_height

    print 'cell area <=0',cell_area[cell_area <= 0]

    # Create 1D array of areas, repeated for each day of data
    #areas = np.tile(np.ravel(cell_area), num_days)

    return cell_area #TODO figure out how you want to output this


