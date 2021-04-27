import os 
import pydicom
import numpy as np 
from library_dicom.dicom_processor.model.reader.Instance import Instance
from library_dicom.dicom_processor.model.reader.Instance_RTSS import Instance_RTSS



class Instance_RTDose(Instance): 

    def __init__(self, path_dose):
        super().__init__(path_dose, load_image=True)

    def get_image_nparray(self):
        return np.transpose(self.dicomData.pixel_array, axes = (1,2,0))


    def wrap_DHVSequence_in_dict(self): 
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
 
    def add_ROIName_from_RTSS_to_dict(self, dictionnary, rtss_file):
        instance_rtss_object = Instance_RTSS(rtss_file)
        keys = list(dictionnary.keys())
        for key in keys : 
            referenced_number = int(dictionnary[key]['ReferencedROINumber'])
            dictionnary[key]['ReferencedROIName'] = instance_rtss_object.get_ROIName_by_number(referenced_number)
        return dictionnary 


    

        


    #DHV Sequence 


    
