import gebco
import plot_tools
import pandas
import numpy as np

def plot_bathymetry(gebco_path, lons, lats):
    lat0, mapW, mapH = plot_tools.plot_tools.center_map(lons,lats, 1.1)

    lons, lats, z = gebco.getGebcoData(gebco_path,np.min(lons),np.max(lons),
                                                  np.min(lats),np.max(lats))

    return bathy_lons, bathy_lats, z

def gridlatlon(lons,lats,z):
    '''Make 2D grid from lons, lats, value arrays

    returns a 2D array with columns and rows coresponding to lons, lats'''
    lat_vals, lat_idx = np.unique(lats, return_inverse=True)
    lon_vals, lon_idx = np.unique(lons, return_inverse=True)
    vals_array = np.empty(lat_vals.shape + lon_vals.shape)
    vals_array.fill(np.nan)
    vals_array[lat_idx, lon_idx] = vals

    return vals_array

def get_tracks(track_file):
    track_df = pandas.DataFrame.from_csv(track_file, index_col=False)
    lons = track_df['Longitude'].values
    lats = track_df['Latitude'].values
    #TODO read in real depth positions
    z = np.zeros_like(lons)
    z = np.random.random_sample()*-20
    return lons, lats, z

if __name__ == '__main__':

    import matplotlib.pyplot as plt

    track_path = '/home/ryan/Desktop/phd/projects/rune_bottlenose_data/134668/134668-Locations.csv'
    gebco_path = '/media/ryan/data1/asf-fellowship/data/BODC-bathymetric/data/30_arc-second'
    z_scale = 1.0

    lons, lats, z = get_tracks(track_path)
    bathy_lons, bathy_lats, z = plot_bathymetry(gebco_path, lons, lats)
    data = gridlatlon(lons,lats,z)

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

##########

    from mayavi import mlab

    # Slice data
    #data = data[:1000, 900:1900]

    mlab.figure(size=(400, 320), bgcolor=(0.16, 0.28, 0.46))
    mlab.surf(data, colormap='gist_earth', warp_scale=0.2,
                        vmin=100, vmax=0)
    # The data takes a lot of memory, and the surf command has created a
    # copy. We free the inital memory.
    del data

    # A view of the canyon
    mlab.view(-5.9, 83, 570, [5.3, 20, 238])
    mlab.show()
