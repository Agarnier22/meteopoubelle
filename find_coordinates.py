def find_by_center(df, long, lat, r):
    return Math.sqrt(Math.pow(df['LIEU_COORD_GPS_X'] - long, 2) + Math.pow(df['LIEU_COORD_GPS_Y'] - lat, 2)) < r