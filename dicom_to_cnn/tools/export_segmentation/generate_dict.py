from numpy import random 
import os 
from dicom_to_cnn.tools.cleaning_dicom.folders import *


def generate_dict(number_of_roi:int, mode:str) -> dict:
    """a function to generate a dict with informations to generate DICOM SEG or DICOM RTSTRUCT file
    ! no more than 16 characters for each informations ! 

    Args:
        number_of_roi ([int]): [Total number of ROI in dicom file ]
        mode ([str]): ['rtstruct' or 'dicomseg']

    Returns:
        [dict]: [return dict with informations about ROI in it ]
    """

    results = {}
    results["ContentCreatorName"] = "dicom_to_cnn"
    random_number = random.randint(0,1e3)
    
    name = str(input('Enter filename for json file (filename or nothing):'))
    if not name : results["ClinicalTrialSeriesID"] = "json_serie"+str(random_number)
    else : 
        if len(name) > 16 : results["ClinicalTrialSeriesID"] = name[0:16]
        else : results["ClinicalTrialSeriesID"] = name #name of json

    results["ClinicalTrialTimePointID"] = "1"

    description = str(input('Enter serie description (serie description or nothing):'))
    if not description : results["SeriesDescription"] =''
    else : 
        if len(description) > 16 : results["SeriesDescription"] = description[0:16]
        else : results["SeriesDescription"] = description
    
    results["SeriesNumber"] = str(random_number)
    results["InstanceNumber"] = str(number_of_roi)

    body_part = str(input('Enter body part examined (body part or nothing) : '))
    if not body_part : results["BodyPartExamined"] = "all body"
    else : 
        if len(body_part) > 16 : results["BodyPartExamined"] = body_part[0:16]
        else : results["BodyPartExamined"] = body_part

    results["segmentAttributes"] = []
    subliste = []
    for i in range(number_of_roi):
        subdict = {}
        subdict["labelID"]= i+1
        segment_description = str(input('Enter ROI n°{} description/name (segment description or nothing) : '.format(i+1)))
        if not segment_description : subdict["SegmentDescription"] = str("ROI {}".format(i+1))
        else : 
            if len(segment_description) > 16 : 
                subdict["SegmentDescription"] = segment_description[0:16]
            else : subdict["SegmentDescription"] = segment_description

        subdict["SegmentAlgorithmType"] = "SEMIAUTOMATIC"
        subdict["SegmentAlgorithmName"] =  "DeepOncology"
        if mode == 'rtstruct' : 
            RTROIInterpretedType = str(input("Enter RTROIInterpredType for ROI n°{} (predefined type or nothing) : ".format(i+1)))
            if not RTROIInterpretedType : subdict['RTROIInterpretedType'] = ''
            else : subdict['RTROIInterpretedType'] = RTROIInterpretedType
        


        #subdict["SegmentedPropertyCategoryCodeSequence"] 
        subsubdict = {}
        subsubdict["CodeValue"] = "49755003"
        subsubdict["CodingSchemeDesignator"] = "SCT"
        subsubdict["CodeMeaning"] = "Morphologically Altered Structure"
        subdict["SegmentedPropertyCategoryCodeSequence"] = subsubdict

        #subdict["SegmentedPropertyTypeCodeSequence"] = {}
        subsubdict = {}
        subsubdict["CodeValue"] = "108369006"
        subsubdict["CodingSchemeDesignator"] = "SCT"
        subsubdict["CodeMeaning"] = "Neoplasm"
        subdict["SegmentedPropertyTypeCodeSequence"] = subsubdict
        subliste.append(subdict)

    results["segmentAttributes"].append(subliste)

    results["ContentLabel"] =  "SEGMENTATION"
    results["ContentDescription"] = "Image segmentation"
    results["ClinicalTrialCoordinatingCenterName"] = "dicom_to_cnn"

    return results

def save_dict_as_json(results:dict, directory:str) -> str :
    """a function to save the dict generated by 'generate_dict' function above

    Args:
        results ([dict]): [Dictionnary generated by 'generate_dict' function ]
        directory ([str]): [Name of directory to save the dict as json file ]

    Returns:
        [str]: [return the path name of the json file]
    """
    filename = results["ClinicalTrialSeriesID"]
    write_json_file(directory, filename, results)
    return os.path.join(directory, filename+'.json')
