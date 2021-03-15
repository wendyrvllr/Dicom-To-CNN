from library_dicom.export_segmentation.rtstruct.RTSS_Writer import RTSS_Writer
from library_dicom.export_segmentation.dicom_seg.DICOMSEG_Writer import DICOMSEG_Writer


class ExportSegmentation_Writer : 

    def __init__(self, segmentation, serie_path, mode):
        """[summary]

        Args:
            segmentation ([array or sitk img]): [if mode = rtstruct : array, if mode = dicomseg : sitk img]
            serie_path ([str]): [Path to an imaging serie related to the segmentation ]
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
        if self.mode == 'rtstruct' : 
            if str(type(self.segmentation)) != "<class 'numpy.ndarray'>" : 
                raise Exception ('For RTSTRUCT format, segmentation has to be an array')
        if self.mode == 'dicomseg' : 
            if str(type(self.segmentation)) != "<class 'SimpleITK.SimpleITK.Image'>" : 
                raise Exception ('For DICOM-SEG format, segmentation has to be a SITK Image')

    def generate_dicom(self, filename, directory_path):
        if self.mode == 'rtstruct' : 
            writer = RTSS_Writer(self.segmentation, self.serie_path)
            writer.save_file(filename, directory_path) 
        elif self.mode == 'dicomseg' : 
            writer = DICOMSEG_Writer(self.segmentation, self.serie_path)
            writer.save_file(filename, directory_path)
