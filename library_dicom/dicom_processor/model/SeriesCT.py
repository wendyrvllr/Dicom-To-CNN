from Series import Series

class SeriesCT(Series):
    """[summary]

    Arguments:
        Series {[type]} -- [description]
    """
    def __init__(self, path, sul_value=False):
        super(SeriesCT, self).__init__(path)
        self.sul_value=sul_value

#A mettre le z spacing ? 