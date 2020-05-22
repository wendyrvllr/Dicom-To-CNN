
def find_non_intersting_series(data):
    paths = []
    series_description = data["series"]["SeriesDescription"].encode('utf-8')
    if("CT COUPES FINES" in series_description): 
        paths.append( data["path"])
    if("_wb_nac" in series_description) : 
        paths.append( data["path"])
