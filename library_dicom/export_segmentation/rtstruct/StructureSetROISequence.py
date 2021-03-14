import pydicom 
import numpy as np
from library_dicom.export_segmentation.tools.rtss_writer_tools import *

class StructureSetROISequence : 

    def __init__(self, mask, results):
        self.mask = mask
        self.number_of_roi = get_number_of_roi(self.mask)
        self.results = results


    def create_StructureSetROISequence(self, pixel_spacing, ReferencedFrameOfReferenceUID) :
        StructureSetROISequence = pydicom.sequence.Sequence()

        for number_roi in range(1 , self.number_of_roi +1):
            dataset = pydicom.dataset.Dataset()
            dataset.ROINumber = number_roi
            dataset.ReferencedFrameOfReferenceUID = ReferencedFrameOfReferenceUID 
            if self.results['segmentAttributes'][0][number_roi-1]["SegmentDescription"] != "None": 
                dataset.ROIName = self.results['segmentAttributes'][0][number_roi-1]["SegmentDescription"]

            else : dataset.ROIName = str(number_roi)

            dataset.ROIVolume = self.get_roi_volume(number_roi, pixel_spacing)
                
             
            #if self.dict_roi_data[number_roi]['ROIGenerationAlgorithm'] != '' :
            #    dataset.ROIGenerationAlgorithm = self.dict_roi_data[number_roi]['ROIGenerationAlgorithm']
            #else : dataset.ROIGenerationAlgorithm = 'UNDEFINED'
            dataset.ROIInterpretedType = self.results['segmentAttributes'][0][number_roi-1]["SegmentAlgorithmType"]
            StructureSetROISequence.append(dataset)
        return StructureSetROISequence 
        
     
    def get_roi_volume(self, number_roi, pixel_spacing):
        number_pixel = 0

        if len(self.mask.shape) == 3 :
             x = np.where(self.mask == number_roi)[0]
        elif len(self.mask.shape) == 4 : 
            x = np.where(self.mask[:,:,:,number_roi-1] != 0)[0]
        number_pixel = len(x) #same as len(y) or len(z)
        volume_pixel = pixel_spacing[0] * pixel_spacing[1] * abs(pixel_spacing[2])
        volume_pixel = volume_pixel * 10**(-3) #mm3 to ml 
        roi_volume = number_pixel * volume_pixel 

        return np.round(roi_volume , 5)

