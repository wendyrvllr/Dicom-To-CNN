import os

def get_series_path(path):
    """Go through all the folder to find every series path

    Arguments:
        path {[string]} -- [Absolute path where the repertory is located]

    Returns:
        [list] -- [Path's list of every series]
    """

    seriesPath = []
    for (path, dirs, files) in os.walk(path): 
        if not (dirs) :
            seriesPath.append(path) 
    return seriesPath 