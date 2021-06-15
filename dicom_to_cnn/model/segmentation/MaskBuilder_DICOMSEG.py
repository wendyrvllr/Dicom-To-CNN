import pydicom_seg
import pydicom 
import numpy as np 
import SimpleITK as sitk 

class MaskBuilder_DICOMSEG: 
    """a class to read a DICOMSEG file format and generate np.ndarray mask 
    """

    def __init__(self, path_dicomseg_file:str):
        """constructor

        Args:
            path_dicomseg_file (str): [abs path to the dicom_seg file]
        """

        self.path_dicomseg_file = path_dicomseg_file
        self.reader = self.__reader()

    def __reader(self):
        dcm = pydicom.dcmread(self.path_dicomseg_file)
        reader = pydicom_seg.MultiClassReader()
        result = reader.read(dcm)
        return result

    def get_numpy_array(self) -> np.ndarray:
        """return the np.ndarray of the segmentation 

        Returns:
            [np.ndarray]: [return the segmentation mask np.ndarray of shape [z,y,x]]
        """
        return self.reader.data 

    def get_sitk_image(self) -> sitk.Image:
        """return the sitk.Image of the segmentation 

        Returns:
            [np.ndarray]: [return the segmentation mask sitk.Image of shape [x,y,z]]
        """
        return self.reader.image 