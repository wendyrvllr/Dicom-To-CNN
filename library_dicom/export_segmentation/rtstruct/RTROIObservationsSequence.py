import pydicom 
import numpy as np
from library_dicom.export_segmentation.tools.rtss_writer_tools import *

class RTROIObservationsSequence :

    def __init__(self, results, number_of_roi):
        self.number_of_roi = number_of_roi 
        self.results = results


    def create_RTROIObservationsSequence(self):
        RTROIObservationsSequence = pydicom.sequence.Sequence()
        for number_roi in range(1, self.number_of_roi +1) : 
            dataset = pydicom.dataset.Dataset()
            dataset.ReferencedROINumber = number_roi
            dataset.ObservationNumber = number_roi 

            dataset.RTROIInterpretedType = self.results["segmentAttributes"][0][number_roi-1]['RTROIInterpretedType']
            dataset.ROIInterpreter = ''
            
            RTROIObservationsSequence.append(dataset)

        return RTROIObservationsSequence 