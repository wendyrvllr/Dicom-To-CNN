from library_dicom.rtss_processor.model.RTSS import RTSS 
import os
import random

class NewRTSS : 

    def __init__(self, origin, directory_path , serie_path):
        self.directory = directory_path
        self.origin = origin 
        self.serie_path = serie_path 


    def generates_empty_RTSTRUCT(self, path_new_directory, filename=None, serie_path):
        
        # generates folders
        if not os.path.exists(path_new_directory):
            os.makedirs(path_new_directory)
        
        if filename is None:
            filename = path_new_directory+'/'+random.randint(0,1e8)+'.dcm'
        else:
            filename = path_new_directory+'/'+filename
            
        new_rtss = RTSS(self.origin, filename, serie_path)
        new_rtss.save_as(filename)
        return None
        
