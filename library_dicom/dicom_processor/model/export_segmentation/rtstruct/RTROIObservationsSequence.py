import pydicom 

class RTROIObservationsSequence :
    """a class to represent RTROIObservationsSequence
    """

    def __init__(self, results:dict, number_of_roi:int):
        """constructor

        Args:
            results (dict): [dict generated by 'generate_dict.py' ]
            number_of_roi (int): [total number of ROI]
        """
        self.number_of_roi = number_of_roi 
        self.results = results


    def create_RTROIObservationsSequence(self):
        """method to generate RTROIObservationsSequence

        Returns:
            [pydicom.Sequence]: [return RTTOIObservationsSequence ]
        """
        RTROIObservationsSequence = pydicom.sequence.Sequence()
        for number_roi in range(1, self.number_of_roi +1) : 
            dataset = pydicom.dataset.Dataset()
            dataset.ReferencedROINumber = number_roi
            dataset.ObservationNumber = number_roi 

            dataset.RTROIInterpretedType = self.results["segmentAttributes"][0][number_roi-1]['RTROIInterpretedType']
            dataset.ROIInterpreter = ''
            
            RTROIObservationsSequence.append(dataset)

        return RTROIObservationsSequence 