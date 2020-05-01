from enum import Enum

class Modality(Enum):
    """Enumeration to list Modalities according to SOPClass UID

    Arguments:
        Enum {[String]} -- [SOPClassUID]
    """

    PET = '1.2.840.10008.5.1.4.1.1.128'
    CT = '1.2.840.10008.5.1.4.1.1.2'
    RTSTRUCT = '1.2.840.10008.5.1.4.1.1.481.3'