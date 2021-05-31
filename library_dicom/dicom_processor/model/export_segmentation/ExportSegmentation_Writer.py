import SimpleITK as sitk 
from library_dicom.export_segmentation.rtstruct.RTSS_Writer import RTSS_Writer
from library_dicom.export_segmentation.dicom_seg.DICOMSEG_Writer import DICOMSEG_Writer

class ExportSegmentation_Writer : 
    """a class to export segmentation sitk img in RTSTRUCT or DICOMSEG format
    """

    def __init__(self, segmentation:sitk.Image, serie_path:str, mode:str):
        """[summary]

        Args:
            segmentation ([sitk.Image]): [sitk image of 3D segmentation]
            serie_path ([str]): [directory's pathy of a dicom serie associated to the segmentation]
            mode ([str]): ['rtstruct' or 'dicomseg']
        """
        self.segmentation = segmentation
        self.serie_path = serie_path 
        self.mode = mode 
        mode_available = ['rtstruct', 'dicomseg']
        if self.mode not in mode_available : 
            raise Exception ('Format not available')
        self.is_segmentation_in_good_modality()


    def is_segmentation_in_good_modality(self):
        """check if segmentation mask is a sitk.Image for both modality

        Raises:
            Exception: [raise Exception if not]
        """
        if self.mode == 'rtstruct' : 
            if  str(type(self.segmentation)) != "<class 'SimpleITK.SimpleITK.Image'>" : 
                raise Exception ('For RTSTRUCT format, segmentation has to be a SITK image')

        if self.mode == 'dicomseg' : 
            if str(type(self.segmentation)) != "<class 'SimpleITK.SimpleITK.Image'>" : 
                raise Exception ('For DICOM-SEG format, segmentation has to be a SITK Image')

    def generate_dicom(self, filename:str, directory_path:str):
        """method to generate and save a new DICOM file in RTSTRUCT or DICOMSEG format

        Args:
            filename (str): [name of the new dicom file]
            directory_path (str): [directory's path where to save the new dicom file]
        """
        if self.mode == 'rtstruct' : 
            writer = RTSS_Writer(self.segmentation, self.serie_path)
            writer.save_file(filename, directory_path) 
        elif self.mode == 'dicomseg' : 
            writer = DICOMSEG_Writer(self.segmentation, self.serie_path)
            writer.save_file(filename, directory_path)
