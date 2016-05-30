def create_linestring(name, description, lons, lats, width, color):
    '''Create a simplekml linestring object

    E.g. Save the KML
    kml.save(file_name)
    '''
    import simplekml

    coords = zip(lons, lats)

    # Create an instance of Kml
    kml = simplekml.Kml()

    ls = kml.newlinestring(name=name, description=description,
                                  coords=coords)

    ls.style.linestyle.color = simplekml.Color.red  # Red
    ls.style.linestyle.width = 10  # 10 pixels

    return kml


if __name__ == '__main__':

    print('yes')#TODO implement simple test
