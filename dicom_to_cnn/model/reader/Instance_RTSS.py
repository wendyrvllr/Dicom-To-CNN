from dicom_to_cnn.model.reader.Series import Series
from dicom_to_cnn.model.reader.Instance import Instance
import numpy as np 
import sys 



class Instance_RTSS(Instance):
    """A class to represent a RTSTRUCT Dicom file 
    """

    def __init__(self, path_rtss:str):
        """constructor 

        Args:
            path_rtss (str): [path of the rtss file]
        """
        super().__init__(path_rtss, load_image=True)


    def get_image_nparray(self):
        """Can't get image numpy array from a RTSTRUCT FILE 
        """
        sys.exit('Cannot get image numpy array from RTSTRUCT FILE')


    def get_list_all_SOP_Instance_UID_RTSS(self) -> list:
        """method to get all SOPInstanceUID referenced in RTSTRUCT File

        Returns:
            [list]: [list of all SOP Instance UID]
        """
        number_item = len(self.dicomData[0x30060010][0].RTReferencedStudySequence[0].RTReferencedSeriesSequence[0].ContourImageSequence)
        liste = []
        for i in range(number_item):
            liste.append(str(self.dicomData[0x30060010][0].RTReferencedStudySequence[0].RTReferencedSeriesSequence[0].ContourImageSequence[i].ReferencedSOPInstanceUID))
        return liste

    def get_number_of_roi(self) -> int:
        """method to count number of ROI in RTSTRUCT File

        Returns:
            [int]: [return the number of ROI in RTSS]
        """
        return len(self.dicomData.StructureSetROISequence)


    #info from ReferencedFrameOfReferenceSequence
    def get_number_of_referenced_series(self) -> int:
        """method to count the series referenced in ReferencedFrameOfReference Sequence

        Returns:
            [int]: [return the number of series referenced in ReferencedFrameOfReference Sequence]
        """
        return len(self.dicomData.ReferencedFrameOfReferenceSequence)


    def get_frame_of_reference_uid(self) -> list:
        """method to get FrameOfReferenceUID for each series referenced in ReferencedFrameOfReference Sequence.
            Usually, only one serie referenced.

        Returns:
            [list]: [list of FrameOfReferenceUID in ReferencedFrameOfReference Sequence]
        """
        number_serie = len(self.dicomData.ReferencedFrameOfReferenceSequence)
        liste = []
        for i in range(number_serie):
            liste.append(self.dicomData[0x30060010][i].FrameOfReferenceUID)
        return liste 


    def is_frame_of_reference_same(self, frame_of_ref_uid_serie:str) -> bool:
        """check if FrameOfReferenceUID in RTSS == FrameOfReferenceUID in associated serie 

        Args:
            frame_of_ref_uid_serie (str): [FrameOfReferenceUID in the associated serie]

        Returns:
            [bool]: [return True if UID in RTSS and UID in associated serie are equal, False instead. ]
        """
        frame_of_reference_UID = self.get_frame_of_reference_uid()
        for i in range(len(frame_of_reference_UID)):
            if frame_of_ref_uid_serie != frame_of_reference_UID[i] :
                return False 
        return True 


    def get_referenced_series_instance_uid(self) -> list:
        """method to get a list of SeriesInstanceUID for each series referenced in ReferencedFrameOfReference Sequence.
            Usually, only one serie referenced.
            Has to be the same SeriesInstanceUID in the associated serie. 

        Returns:
            [list]: [list of SeriesInstanceUID for each series referenced]
        """
        number_serie = len(self.dicomData.ReferencedFrameOfReferenceSequence)
        liste = []
        for i in range(number_serie):
            liste.append(self.dicomData[0x30060010][i].RTReferencedStudySequence[0].RTReferencedSeriesSequence[0].SeriesInstanceUID)
        return liste


    def get_referenced_study_SOP_instance_uid(self) -> list :
        """method to get a list of StudyInstanceUID for each series referenced in ReferencedFrameOfReference Sequence.
            Usually, only one serie referenced.
            Has to be the same StudyInstanceUID in the associated serie. 

        Returns:
            [list]: [list of StudyInstanceUID for each series referenced]
        """
        number_serie = len(self.dicomData.ReferencedFrameOfReferenceSequence)
        liste = []
        for i in range(number_serie):
            liste.append(self.dicomData[0x30060010][i].RTReferencedStudySequence[0].ReferencedSOPInstanceUID)
        return liste


    def get_referenced_SOP_class_UID(self) -> list :
        """method to get a list of SOPClassUID for each series referenced in ReferencedFrameOfReference Sequence.
            Usually, only one serie referenced.
            Has to be the same SOPCLassUID in the associated serie. 

        Returns:
            [list]: [list of SOPClassUID for each series referenced]
        """
        number_serie = len(self.dicomData.ReferencedFrameOfReferenceSequence)
        liste = []
        for i in range(number_serie):
            liste.append(self.dicomData[0x30060010][i].RTReferencedStudySequence[0].RTReferencedSeriesSequence[0].ContourImageSequence[0].ReferencedSOPClassUID)
        return liste 

 
    #info from StructureSetROISequence
    def get_ROI_name(self, number_roi:int) -> str:
        """method to get ROI name from StructureSetROI Sequence

        Args:
            number_roi (int): [ROI number; start at 1. ]

        Returns:
            [str]: [return ROI name]
        """
        return self.dicomData[0x30060020][number_roi - 1].ROIName 

    def get_ROI_volume(self, number_roi:int) -> str:
        """method to get ROI volume from StructureSetROI Sequence

        Args:
            number_roi (int): [ROI number; start at 1. ]

        Returns:
            [str]: [return ROI volume value]
        """
        return self.dicomData[0x30060020][number_roi - 1].ROIVolume 

    def get_ROI_generation_algorithm(self, number_roi:int) -> str :
        """method to get ROIGenerationAlgorithm value from StructureSetROI Sequence
        Args:
            number_roi (int): [ROI number; start at 1. ]

        Returns:
            [str]: [return ROIGenerationAlgorithme value]
        """
        return self.dicomData[0x30060020][number_roi - 1].ROIGenerationAlgorithm 


    #info from ROIContourSequence
    def get_roi_display_color(self, number_roi:int) -> str :
        """method to get ROI color representation from ROIContour Sequence

        Args:
            number_roi (int): [ROI number; start at 1. ]

        Returns:
            [str]: [return ROIDisplayColor value , format [r,g,b]]
        """
        return self.dicomData[0x30060039][number_roi - 1].ROIDisplayColor 


    def get_list_contour_SOP_Instance_UID(self, roi_number:int) -> list: 
        """method to get a list of every contour SOPINstanceUID  from ROIContour Sequence

        Args:
            number_roi (int): [ROI number; start at 1. ]

        Returns:
            [list]: [return list of every SOPInstanceUID where there is a contour]
        """
        number_item = len(self.dicomData[0x30060039][roi_number - 1].ContourSequence)
        liste = []
        for i in range(number_item):
            liste.append(str(self.dicomData[0x30060039][roi_number - 1].ContourSequence[i].ContourImageSequence[0].ReferencedSOPInstanceUID))
        return liste 

    
    def is_referenced_SOP_Instance_UID_in_all_SOP_Instance(self) -> bool :
        """check if every  SOPInstanceUID contour is referenced in the SOPINstanceUID of the associated serie

        Raises:
            Exception: [Exception if one of the SOPInstanceUID contour is not referenced in all SOPInstanceUID of the associated serie]

        Returns:
            [bool]: [True if everything referenced, raise Exception instead]
        """
        all_sop = str(self.get_list_all_SOP_Instance_UID_RTSS)
        referenced_sop = str(self.get_list_contour_SOP_Instance_UID)
        for uid in referenced_sop : 
            if uid not in all_sop : 
                raise Exception("SOP Instance UID not in the serie")
        return True 


    def get_number_of_contour_points(self, roi_number:int) -> list:
        """method to get a list of every NumberOfContourPoint in each contours  from ROIContour Sequence

        Args:
            number_roi (int): [ROI number; start at 1. ]

        Returns:
            [list]: [return list of number of contour points]
        """
        number_item = len(self.dicomData[0x30060039][roi_number - 1].ContourSequence)
        liste = []
        for i in range(number_item):
            liste.append(self.dicomData[0x30060039][roi_number - 1].ContourSequence[i].NumberOfContourPoints)
        return liste

    def get_list_contour_geometric_type(self, roi_number:int) -> list :
        """method to get a list of every ContourGeomtricType value of each contour  from ROIContour Sequence

        Args:
            number_roi (int): [ROI number; start at 1. ]

        Returns:
            [list]: [return a list with every ContourGeometricType value for each contour]
        """
        number_item = len(self.dicomData[0x30060039][roi_number - 1].ContourSequence)
        liste = []
        for i in range(number_item):
            liste.append(self.dicomData[0x30060039][roi_number - 1].ContourSequence[i].ContourGeometricType)
        return liste

    def is_closed_planar(self, roi_number:int) -> bool :
        """check if every contour is CLOSED_PLANAR  from ROIContour Sequence

        Args:
            roi_number (int): [ROI number, start a 1]

        Returns:
            [bool]: [return True if every value is CLOSED_PLANAR, False instead]
        """
        geometric_type = self.get_list_contour_geometric_type(roi_number)
        for type in geometric_type :
            if type != "CLOSED_PLANAR" : 
                return False
        return True 

    def get_contour_data(self, roi_number:int) -> list :
        """method to get contour data of contours  from ROIContour Sequence

        Args:
            number_roi (int): [ROI number; start at 1. ]

        Returns:
            [list]: [return list of contour data for each contour [[contour1 : x, y, z, x, y ,z, ...], [contour2 : ...], [...]] ]
        """
        number_item = len(self.dicomData[0x30060039][roi_number - 1].ContourSequence)
        liste = []
        for i in range(number_item):
            liste.append(self.dicomData[0x30060039][roi_number - 1].ContourSequence[i].ContourData)
        return liste 
