import os 
import pydicom
from library_dicom.dicom_processor.model.reader.Instance import Instance



class Instance_RTDose(Instance): 

    def __init__(self, path_dose):
        super().__init__(path_dose, load_image=True)

    def get_image_nparray(self):
        return np.transpose(self.dicomData.pixel_array, axes = (1,2,0))


    def wrap_DHVSequence_in_dict(self): 
        dictionnary = {}
        for i in range(len(self.dicomData.DVHSequence)) : 
            referenced_roi = int(self.dicomData.DHVSequence[i].DVHReferencedROISequence[0].ReferencedROINumber)
            #dataset = {}


    #DHV Sequence 


    
