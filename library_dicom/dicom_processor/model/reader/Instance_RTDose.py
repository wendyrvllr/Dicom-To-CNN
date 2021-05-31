import os 
import pydicom
import numpy as np 
from library_dicom.dicom_processor.model.reader.Instance import Instance
from library_dicom.dicom_processor.model.reader.Instance_RTSS import Instance_RTSS



class Instance_RTDose(Instance): 
    """A class to represent a RTDose Dicom File

    Args:
        Instance ([type]): [description]
    """

    def __init__(self, path_dose :str ):
        """constructor

        Args:
            path_dose (str): [path of the rt dose file ]
        """
        super().__init__(path_dose, load_image=True)

    def get_image_nparray(self):
        """get 3d matrix of rt dose 

        Returns:
            [ndarray]: []
        """
        return np.transpose(self.dicomData.pixel_array, axes = (1,2,0))


    def wrap_DHVSequence_in_dict(self): 
        """wrap in dictionnary DVH Sequence of each ROI 

        Returns:
            [dict]: [return a dictionnary, with, for each ROI, DVHSequence in the RTDose file]
        """
        dictionnary = {}
        for i in range(len(self.dicomData.DVHSequence)) : 
            referenced_roi = int(self.dicomData.DVHSequence[i].DVHReferencedROISequence[0].ReferencedROINumber)
            dataset = {}
            dataset['ReferencedROINumber'] = referenced_roi
            dataset['DVHType'] = self.dicomData.DVHSequence[i].DVHType
            dataset['DoseUnits'] = self.dicomData.DVHSequence[i].DoseUnits  
            dataset['DVHDoseScaling'] = self.dicomData.DVHSequence[i].DVHDoseScaling 
            dataset['DVHVolumeUnits'] = self.dicomData.DVHSequence[i].DVHVolumeUnits 
            dataset['DVHNumberOfBins'] = self.dicomData.DVHSequence[i].DVHNumberOfBins 
            dataset['DVHMinimumDose'] = self.dicomData.DVHSequence[i].DVHMinimumDose
            dataset['DVHMaximumDose'] = self.dicomData.DVHSequence[i].DVHMaximumDose
            dataset['DVHMeanDose'] = self.dicomData.DVHSequence[i].DVHMeanDose
            dataset['DVHData'] = self.dicomData.DVHSequence[i].DVHData 
            dictionnary[referenced_roi] = dataset 

        return dictionnary
 
    def add_ROIName_from_RTSS_to_dict(self, dictionnary:dict, rtss_file:str):
        """From the RTSS file associated, add the roi's name in the dictionnary of DVH Sequence

        Args:
            dictionnary (dict): [dictionnary from  wrap_DHVSequence_in_dict function]
            rtss_file (str): [file path of the rtss file associated]

        Returns:
            [dict]: [description]
        """
        instance_rtss_object = Instance_RTSS(rtss_file)
        keys = list(dictionnary.keys())
        for key in keys : 
            referenced_number = int(dictionnary[key]['ReferencedROINumber'])
            dictionnary[key]['ReferencedROIName'] = instance_rtss_object.get_ROI_name(referenced_number)
        return dictionnary 