# Import the database driver and shapefile library
import pg8000
import shapefile

def shphand(url):
    # Set up the datbase connection
    connection = pg8000.connect(database="kursova", user="kursovauser", 
                                password="root")

    # Get the database cursor to execute queries
    cursor = connection.cursor()

    # Set up a shapefile reader for our shapefile
    r = shapefile.Reader(url)

    # Build a query to create our "cities" table
    # with an id and geometry column.
    table_query = """CREATE TABLE cities (
                     id SERIAL,
                     PRIMARY KEY (id),
                     geom GEOMETRY(Point, 4326),
                     """

    # Get the shapefile fields but skip the first
    # one which is a deletion flag used internally
    # by dbf software
    fields = r.fields[1:]

    # We are going to keep track of the fields as a
    # string. We'll use this query fragment for our
    # insert query later.
    field_string = ""

    # Loop throug the fields and build our table
    # creation query.
    for i in range(len(fields)):
        # get the field information
        f = fields[i]
        # get the field name and lowercase it for consistency
        f_name = f[0].lower()
        # add the name to the query and our string list of fields
        table_query += f_name
        field_string += f_name
        # Get the proper type for each field. Note this check
        # is not comprehensive but it convers the types in
        # our sample shapefile.
        if f[1] == "F":
            table_query += " DOUBLE PRECISION"
        elif f[1] == "N":
            table_query += " INTEGER"
        else:
            table_query += " VARCHAR"
        # If this field isn' the last, we'll add a comma
        # and some formatting.
        if i != len(fields)- 1:
            table_query += ","
            table_query += "\n"
            table_query += "                 "
            field_string += ","
        # Close the query on the field.
        else:
            table_query += ")"
            field_string += ",geom"

    # Execute the table query
    cursor.execute(table_query)

    # Commit the change to the database or it won't stick. 
    # PostgreSQL is transactional which is good so nothing 
    # is stored until you're sure it works.
    connection.commit()

    # Create a python generator for the 
    # shapefiles shapes and records
    shape_records = (shp_rec for shp_rec in r.iterShapeRecords())

    # Loop through the shapefile data and add it to our new table.
    for sr in shape_records:
        # Get our point data.
        shape = sr.shape
        x, y = shape.points[0]
        # Get the attribute data and set it up as
        # a query fragment.
        attributes = ""
        for r in sr.record:
            if type(r) == type("string"):
                r = r.replace("'", "''")
            attributes += "'{}'".format(r)
            attributes += ","        
        # Build our insert query template for this shape record.
        # Notice we are going to use a PostGIS function
        # which can turn a WKT geometry into a PostGIS
        # geometry.
        point_query = """INSERT INTO cities 
                         ({})
                         VALUES ({}
                         ST_GEOMFROMTEXT('POINT({} {})',4326))"""    
        # Populate our query template with actual data.
        format_point_query = point_query.format(field_string, 
                                                attributes, x, y)
        # Insert the point data
        cursor.execute(format_point_query)

    # Everything went ok so let's update the database.
    connection.commit()
    return 0