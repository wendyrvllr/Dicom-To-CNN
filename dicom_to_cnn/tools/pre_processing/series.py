import os 
from dicom_to_cnn.enums.TagEnum import *
from dicom_to_cnn.enums.SopClassUID import *
from dicom_to_cnn.model.reader.Series import Series 
from dicom_to_cnn.model.reader.SeriesCT import SeriesCT
from dicom_to_cnn.model.reader.SeriesPT import SeriesPT 
from dicom_to_cnn.model.reader.Instance import Instance  

def get_series_object(path:str):
    """
    class method to generate a Series object

    Args:
        path (str): [path folder of series]

    Returns:
        [Series]: [return a Series object]
    """
    try:
        first_file_name = os.listdir(path)[0]
    except Exception as err:
        print(err)
        print(path)
    first_instance = Instance( os.path.join(path,first_file_name) )
    sop_class_uid = first_instance.get_sop_class_uid()
    if(sop_class_uid == ImageModalitiesSOPClass.PT.value or sop_class_uid == ImageModalitiesSOPClass.EnhancedPT.value):
        return SeriesPT(path)
    elif (sop_class_uid == ImageModalitiesSOPClass.CT.value or sop_class_uid == ImageModalitiesSOPClass.EnhancedCT.value):
        return SeriesCT(path)
    else : return Series(path)
