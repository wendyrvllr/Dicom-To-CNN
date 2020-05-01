from enum import Enum

class TagsPatient(Enum):
    """Patient related dicom tags

    Arguments:
        Enum {hex} -- [Tag address]
    """

    PatientName = 0x00100010
    PatientID = 0x00100020
    PatientBirthDate = 0x00100030
    PatientSex = 0x00100040

class TagsStudy(Enum):
    """Study related tags

    Arguments:
        Enum {hex} -- [Tag address]
    """

    AccessionNumber = 0x00080050
    InstitutionName = 0x0080080
    StudyDate = 0x00080020
    StudyTime = 0x00080030
    StudyDescription = 0x00081030
    StudyID = 0x00200010
    StudyInstanceUID = 0x0020000D
    PatientWeight = 0x00101030
    PatientHeight = 0x00101020

class TagsSeries(Enum):
    """Series related dicom tags

    Arguments:
        Enum {hex} -- [Tag address]
    """

    ImageOrientationPatient = 0x00200020
    Manufacturer = 0x0080070
    Modality = 0x0080060
    SeriesDate = 0x00080021
    SeriesTime = 0x00080032
    SeriesDescription = 0x0008103E
    SeriesInstanceUID = 0x0020000E
    SeriesNumber = 0x00200011
    AcquisitionDate = 0x00080022
    AcquisitionTime = 0x0080032
    NumberOfSlices = 0x00540081

class TagsInstance(Enum):
    """Instance related tags

    Arguments:
        Enum {hex} -- [tag address]
    """

    ImagePosition = 0x00200032
    ImageOrientation = 0x00200037
    RescaleSlope = 0x00281053
    RescaleIntercept = 0x00281052
    PixelSpacing = 0x00280030
    SliceLocation = 0x00201041