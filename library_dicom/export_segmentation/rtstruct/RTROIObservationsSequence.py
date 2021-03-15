import pydicom 
import numpy as np
from library_dicom.export_segmentation.tools.rtss_writer_tools import *

class RTROIObservationsSequence :

    def __init__(self, mask, results):
        self.mask = mask
        self.number_of_roi = get_number_of_roi(self.mask)
        self.results = results


    def create_RTROIObservationsSequence(self):
        RTROIObservationsSequence = pydicom.sequence.Sequence()
        for number_roi in range(1, self.number_of_roi +1) : 
            dataset = pydicom.dataset.Dataset()
            dataset.ReferencedROINumber = number_roi
            if self.results['segmentAttributes'][0][number_roi-1]["SegmentDescription"] != "None" : 
                dataset.ROIObservationLabel = self.results['segmentAttributes'][0][number_roi-1]["SegmentDescription"]

            else : dataset.ROIName = str(number_roi)

            #if 'ROIInterpretedType' in self.dict_roi_data[number_roi] : 
            dataset.RTROIInterpretedType = '' #self.results['segmentAttributes'][0][number_roi-1]["SegmentAlgorithmType"]

            RTROIObservationsSequence.append(dataset)

        return RTROIObservationsSequence 