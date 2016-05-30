def get_geotiff_wkt(dataset):
    '''Get WKT projection information from geotiff'''
    from osgeo import osr

    proj = dataset.GetProjection()

    proj_wkt = osr.SpatialReference()
    proj_wkt.ImportFromWkt(proj)

    return proj_wkt


def get_cartopy_proj(proj_wkt):
    '''Extract EPSG code from WKT and get cartopy projection

       NOTE: code must be projected coordinate system, not geodetic coordinate
       system'''
    import cartopy.crs

    #projcs = proj_wkt.GetAuthorityCode('PROJCS')
    projcs = int(proj_wkt.GetAttrValue('Authority',1))

    #TODO make handle other geodetic projections
    if projcs==4326:
        projection = cartopy.crs.PlateCarree()
    else:
        projection = cartopy.crs.epsg(projcs)
    return projection


def plot_geotiff(file_path):
    '''Plot geotiff with cartopy

       https://ocefpaf.github.io/python4oceanographers/blog/2015/03/02/geotiff/
    '''
    from osgeo import gdal, osr
    import matplotlib.pyplot as plt

    # Read file, data, and geotransform
    gdal.UseExceptions()
    dataset = gdal.Open(file_path)

    data = dataset.ReadAsArray()
    geotransform = dataset.GetGeoTransform()

    ## http://geoinformaticstutorial.blogspot.no/2012/09/reading-raster-data-with-python-and-gdal.html
    ## Dataset parameters
    #cols = dataset.RasterXSize
    #rows = dataset.RasterYSize
    #bands = dataset.RasterCount
    #driver = dataset.GetDriver().LongName

    ## Geotransform parameters
    #origin_x     = geotransform[0] # top left x
    #pixel_width  = geotransform[1] # w-e pixwl resolution
    #x_rot        = geotransform[2] # rotation, 0 = "north up"
    #origin_y     = geotransform[3] # top left y
    #y_rot        = geotransform[4] # rotation, 0 = "north up"
    #pixel_height = geotransform[5] # n-s pixel resolution

    # Get projection for plotting
    proj_wkt = get_geotiff_wkt(dataset)
    projection = get_cartopy_proj(proj_wkt)

    # Create plot
    subplot_kw = dict(projection=projection)
    fig, ax = plt.subplots(figsize=(9, 9), subplot_kw=subplot_kw)

    extent = (geotransform[0],
              geotransform[0] + dataset.RasterXSize * geotransform[1],
              geotransform[3] + dataset.RasterYSize * geotransform[5],
              geotransform[3])

    # Reshape data from (y, x, t) to (t, y, x)
    plot_data = data[:3, :, :].transpose((1, 2, 0))

    img = ax.imshow(plot_data, extent=extent, origin='upper')
    ax.coastlines('50m')

    plt.show()

    return None


if __name__ == '__main__':

    file_path = './mareano_kjemi-HCB.tif'

    plot_geotiff(file_path)
