import numpy as np 
from dicom_to_cnn.model.reader.Instance import Instance
from dicom_to_cnn.model.reader.Instance_RTSS import Instance_RTSS



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

    def get_image_nparray(self) -> np.ndarray:
        """get 3d matrix of rt dose 

        Returns:
            [np.ndarray]: [return the 3D array from a RTDose file, shape (z,y,x) ]
        """
        return self.dicomData.pixel_array


    def wrap_DHVSequence_in_dict(self, rtss_file:str) -> dict: 
        """wrap in dictionnary DVH Sequence of each ROI 
        dict = { (roi) 1 : {'ReferencedROINumber' : value
                                'DVHType' : value
                                'DoseUnits' : value
                                'DVHDoseScaling' : value
                                'DVHVolumeUnits':  value
                                'DVHNumberOfBins' : value
                                'DVHMinimumDose' : value
                                'DVHMaximumDose' : value
                                'DVHMeanDose' : value
                                'DVHData' : value},
                (roi) 2 : {'ReferencedROINumber' : value
                                'DVHType' : value
                                'DoseUnits' : value
                                'DVHDoseScaling' : value
                                'DVHVolumeUnits':  value
                                'DVHNumberOfBins' : value
                                'DVHMinimumDose' : value
                                'DVHMaximumDose' : value
                                'DVHMeanDose' : value
                                'DVHData' : value}, ...}

        Returns:
            [dict]: [return a dictionnary, with, for each ROI, DVHSequence in the RTDose file]
        """

        instance_rtss_object = Instance_RTSS(rtss_file)
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
            dataset['ReferencedROIName'] = instance_rtss_object.get_ROI_name(referenced_roi)
            dictionnary[referenced_roi] = dataset 

        return dictionnary
