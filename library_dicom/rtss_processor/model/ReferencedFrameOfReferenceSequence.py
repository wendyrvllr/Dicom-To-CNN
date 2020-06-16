import pydicom 
import numpy as np
import cv2 

class ReferencedFrameOfReferenceSequence :

    def __init__(self): 
        pass


    def create_ContourImageSequence(self, ReferencedSOPClassUID, list_all_SOPInstanceUID):
        ContourImageSequence = pydicom.sequence.Sequence()
        for SOPInstanceUID in list_all_SOPInstanceUID : 

            dataset = pydicom.dataset.Dataset()
            dataset.ReferencedSOPClassUID = ReferencedSOPClassUID
            dataset.ReferencedSOPInstanceUID = SOPInstanceUID
            ContourImageSequence.append(dataset)
        return ContourImageSequence 

    def create_RTReferencedSeriesSequence(self, ReferencedSOPClassUID, list_all_SOPInstanceUID, SeriesInstanceUID):
        RTReferencedSeriesSequence = pydicom.sequence.Sequence()
         
        dataset = pydicom.dataset.Dataset()
        dataset.SeriesInstanceUID = SeriesInstanceUID
        dataset.ContourImageSequence = self.create_ContourImageSequence(ReferencedSOPClassUID, list_all_SOPInstanceUID)
        RTReferencedSeriesSequence.append(dataset)
        return RTReferencedSeriesSequence

    def create_RTReferencedStudySequence(self, ReferencedSOPClassUID, list_all_SOPInstanceUID, SeriesInstanceUID, StudyInstanceUID):
        RTReferencedStudySequence = pydicom.sequence.Sequence()
        dataset = pydicom.dataset.Dataset()
        dataset.ReferencedSOPInstanceUID = StudyInstanceUID
        dataset.RTReferencedSeriesSequence = self.create_RTReferencedSeriesSequence(ReferencedSOPClassUID, list_all_SOPInstanceUID, SeriesInstanceUID)
        RTReferencedStudySequence.append(dataset)
        return RTReferencedStudySequence

    def create_ReferencedFrameOfReferenceSequence(self, FrameOfReferenceUID, ReferencedSOPClassUID, list_all_SOPInstanceUID, SeriesInstanceUID, StudyInstanceUID): 
        ReferencedFrameOfReferenceSequence = pydicom.sequence.Sequence()
        dataset = pydicom.dataset.Dataset()
        dataset.FrameOfReferenceUID = FrameOfReferenceUID 
        dataset.RTReferencedStudySequence = self.create_RTReferencedStudySequence(ReferencedSOPClassUID, list_all_SOPInstanceUID, SeriesInstanceUID, StudyInstanceUID)
        ReferencedFrameOfReferenceSequence.append(dataset)
        return ReferencedFrameOfReferenceSequence
