from library_dicom.rtss_processor.model.RTSS import RTSS
import os 
import random 

class New_Empty_RTSS : 
    """from a serie CT, generate a dicom RT file 
    """

    def __init__(self, origin, filename, serie_path, path_new_directory):

    
        self.origin = origin
        self.filename = filename
        self.generate_empty_RTSTRUCT(origin, filename, serie_path, path_new_directory)
        


    def generate_empty_RTSTRUCT(self, origin, filename, serie_path, path_new_directory):
        """create a new empty RTSTRUCT file

        """
    
        # generates folders
        if not os.path.exists(path_new_directory):
            os.makedirs(path_new_directory)

        if filename is None:
            filename = path_new_directory+'/'+random.randint(0,1e8)+'.dcm'
        else:
            filename = path_new_directory+'/'+filename



        new_RTSTRUCT = RTSS(origin, filename, serie_path)
        new_RTSTRUCT.save_as(filename)

        return None 
