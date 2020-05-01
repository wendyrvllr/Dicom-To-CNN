from enum import Enum

class CapturesSOPClass(Enum):

    SecondaryCaptureImageStorage = '1.2.840.10008.5.1.4.1.1.7'
    MultiframeSingleBitSecondaryCaptureImageStorage = '1.2.840.10008.5.1.4.1.1.7.1'
    MultiframeGrayscaleByteSecondaryCaptureImageStorage	= '1.2.840.10008.5.1.4.1.1.7.2'
    MultiframeGrayscaleWordSecondaryCaptureImageStorage = '1.2.840.10008.5.1.4.1.1.7.3'	
    MultiframeTrueColorSecondaryCaptureImageStorage = '1.2.840.10008.5.1.4.1.1.7.4'

class ImageModalitiesSOPClass(Enum):

    CT = '1.2.840.10008.5.1.4.1.1.2'
    PT = '1.2.840.10008.5.1.4.1.1.128'

class RTModalitiesSOPClass(Enum):

    RTSS = '1.2.840.10008.5.1.4.1.1.481.3'