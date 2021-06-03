import numpy as np 
from library_dicom.dicom_processor.tools.visualization.create_mip import * 

class MIP_Builder : 
    """a class to  generate 2D MIP from a np.ndarray"""

    def __init__(self, numpy_array:np.ndarray):
        """constructor

        Args:
            numpy_array (np.ndarray): [3D np.ndarray of shape (z,y,x)]
        """
        self.numpy_array = numpy_array

    def save_mip(self, angle:int, study_uid:str, directory:str):
        """method to generate and save 2D MIP as png image

        Args:
            angle (int): [choose rotation angle]
            study_uid (str): [study uid of the patient]
            directory (str): [directory's path where to save the MIP png]

        Returns:
            (str): [return complete filename of the MIP png saved]
        """
        filename = mip_projection(numpy_array=self.numpy_array, angle=angle, study_uid=study_uid, type='ct', cmap='gray', vmin=None, vmax=None, directory_path=directory)
        return filename



    
