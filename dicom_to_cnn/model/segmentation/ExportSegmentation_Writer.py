import SimpleITK as sitk 
from dicom_to_cnn.model.segmentation.rtstruct.RTSS_Writer import RTSS_Writer
from dicom_to_cnn.model.segmentation.dicom_seg.DICOMSEG_Writer import DICOMSEG_Writer
from dicom_to_cnn.model.segmentation.nifti.Nifti_Writer import Nifti_Writer

class Format(Enum):
    nifti = 1
    dicomseg = 2
    rtstruct = 3

    
class ExportSegmentation_Writer : 
    """a class to export segmentation sitk img in RTSTRUCT or DICOMSEG format
    """

    def __init__(self, segmentation:sitk.Image,  mode:str, serie_path:str=None):
        """[summary]

        Args:
            segmentation (sitk.Image): [3D sitkImage of shape (z,y,x)]
            mode (str): ['rtstruct', 'dicomseg', 'nifti']
            serie_path (str, optional): [set a path for the associated serie. Optionnal for nifti format only]. Defaults to None.

         

        Raises:
            Exception: [description]
        """
        self.segmentation = segmentation
        self.serie_path = serie_path 
        self.mode = mode 
        mode_available = ['rtstruct', 'dicomseg', 'nifti']
        if self.mode not in mode_available : 
            raise Exception ('Format not available')


    def save_file(self, filename:str, directory_path:str) -> None:
        """method to generate and save a new DICOM file in RTSTRUCT or DICOMSEG format

        Args:
            filename (str): [name of the new dicom file]
            directory_path (str): [directory's path where to save the new dicom file]
        """
        if self.mode == 'rtstruct' : 
            writer = RTSS_Writer(self.segmentation, self.serie_path)
        elif self.mode == 'dicomseg' : 
            writer = DICOMSEG_Writer(self.segmentation, self.serie_path)
        elif self.mode == 'nifti':
            writer = Nifti_Writer(self.segmentation)
        writer.save_file(filename, directory_path)
    

