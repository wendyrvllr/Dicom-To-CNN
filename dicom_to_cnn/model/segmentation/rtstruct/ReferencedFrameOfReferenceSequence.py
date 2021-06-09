import pydicom 

def create_ContourImageSequence(ReferencedSOPClassUID:str, list_all_SOPInstanceUID:list) -> pydicom.Sequence:
    """function to generate ContourImageSequence from ReferencedFrameOfReferenceSequence

    Args:
        ReferencedSOPClassUID (str): [Referenced SOPCLAss UID value from associated serie ]
        list_all_SOPInstanceUID (list): [list of every SOPINstanceUID of every slice in associated dicom serie]

    Returns:
        [pydicom.Sequence]: [return ContourImageSequence]
    """
    ContourImageSequence = pydicom.sequence.Sequence()
    for SOPInstanceUID in list_all_SOPInstanceUID : 

        dataset = pydicom.dataset.Dataset()
        dataset.ReferencedSOPClassUID = ReferencedSOPClassUID
        dataset.ReferencedSOPInstanceUID = SOPInstanceUID
        ContourImageSequence.append(dataset)
    return ContourImageSequence 

def create_RTReferencedSeriesSequence(ReferencedSOPClassUID:str, list_all_SOPInstanceUID:list, SeriesInstanceUID:str) -> pydicom.Sequence:
    """function to generate RTReferencedSeriesSequence from ReferencedFrameOfReferenceSequence

    Args:
        ReferencedSOPClassUID (str): [Referenced SOPCLAss UID value from associated value]
        list_all_SOPInstanceUID (list): [list of every SOPINstanceUID of every slice in associated dicom serie]
        SeriesInstanceUID (str): [SeriesInstanceUID value]

    Returns:
        [pydicom.Sequence]: [return RTReferencedSeriesSequence]
    """
    RTReferencedSeriesSequence = pydicom.sequence.Sequence()
         
    dataset = pydicom.dataset.Dataset()
    dataset.SeriesInstanceUID = SeriesInstanceUID
    dataset.ContourImageSequence = create_ContourImageSequence(ReferencedSOPClassUID, list_all_SOPInstanceUID)
    RTReferencedSeriesSequence.append(dataset)
    return RTReferencedSeriesSequence

def create_RTReferencedStudySequence(ReferencedSOPClassUID:str, list_all_SOPInstanceUID:list, SeriesInstanceUID:str, StudyInstanceUID:str) -> pydicom.Sequence:
    """function to generate RTReferencedStudySequence from ReferencedFrameOfReferenceSequence

    Args:
        ReferencedSOPClassUID (str): [Referenced SOPCLAss UID value from associated serie]
        list_all_SOPInstanceUID (list): [list of every SOPINstanceUID of every slice in associated dicom serie]
        SeriesInstanceUID (str): [SeriesInstanceUID value from associated serie]
        StudyInstanceUID (str): [StudyInstanceUID value from associated serie]

    Returns:
        [pydicom.Sequence]: [return RTReferencedStudySequence ]
    """
    RTReferencedStudySequence = pydicom.sequence.Sequence()
    dataset = pydicom.dataset.Dataset()
    dataset.ReferencedSOPInstanceUID = StudyInstanceUID
    dataset.ReferencedSOPClassUID = ReferencedSOPClassUID
    dataset.RTReferencedSeriesSequence = create_RTReferencedSeriesSequence(ReferencedSOPClassUID, list_all_SOPInstanceUID, SeriesInstanceUID)
    RTReferencedStudySequence.append(dataset)
    return RTReferencedStudySequence

def create_ReferencedFrameOfReferenceSequence(FrameOfReferenceUID:str, ReferencedSOPClassUID:str, list_all_SOPInstanceUID:list, SeriesInstanceUID:str, StudyInstanceUID:str) -> pydicom.Sequence: 
    """function to generate ReferencedFrameOfReferenceSequence

    Args:
        FrameOfReferenceUID (str): [FrameOfReferenceUID value from associated serie]
        ReferencedSOPClassUID (str): [Referenced SOPCLAss UID value from associated serie]
        list_all_SOPInstanceUID (list): [list of every SOPINstanceUID of every slice in associated dicom serie]
        SeriesInstanceUID (str): [SeriesInstanceUID value from associated serie]
        StudyInstanceUID (str): [StudyInstanceUID value from associated serie]


    Returns:
        [pydicom.Sequence]: [return ReferencedFrameOfReferenceSequence from RTSTRUCT file]
    """
    ReferencedFrameOfReferenceSequence = pydicom.sequence.Sequence()
    dataset = pydicom.dataset.Dataset()
    dataset.FrameOfReferenceUID = FrameOfReferenceUID 
    dataset.RTReferencedStudySequence = create_RTReferencedStudySequence(ReferencedSOPClassUID, list_all_SOPInstanceUID, SeriesInstanceUID, StudyInstanceUID)
    ReferencedFrameOfReferenceSequence.append(dataset)
    return ReferencedFrameOfReferenceSequence
