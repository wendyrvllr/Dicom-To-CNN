from Series import Series

class SeriesPT(Series, object):
    """[summary]

    Arguments:
        Series {[type]} -- [description]
    """

    def __init__(self, path, sul_value=False):
        super(SeriesPT, self).__init__(path)
        self.sul_value=sul_value
    
    def calculateSUVFactor(self):
        return 1
    
    def calculateSULFactor(self):
        return 1
    
    def get_numpy_array(self):
        numpy_array = Series.get_numpy_array(self)
        numpy_array = numpy_array * self.calculateSUVFactor()
        if(self.sul_value == False): return numpy_array
        else : return ( numpy_array * self.calculateSULFactor() )