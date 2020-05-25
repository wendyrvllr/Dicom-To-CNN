import json
import os
import shutil
import pprint
from collections import defaultdict, Counter

def generate_merged_file(json_path):
    filenames = os.listdir(json_path)
    content_map = defaultdict(dict)

    for filename in filenames:
        with open(os.path.join(json_path, filename)) as json_file:
            data = json.load(json_file)
            patientID = str(data['patient']['PatientID'])
            studyUID = str(data['study']['StudyInstanceUID'])
            studyDetails = data['study']
            seriesDetails = data['series']
            seriesInstanceUID = data['series']['SeriesInstanceUID']

            if(studyUID not in content_map[patientID]) :
                content_map[patientID][studyUID]=studyDetails
            
            if('Series' not in content_map[patientID][studyUID] ):
                content_map[patientID][studyUID]['Series']={}
            content_map[patientID][studyUID]['Series'][seriesInstanceUID]=seriesDetails
            content_map[patientID][studyUID]['Series'][seriesInstanceUID]['path'] = data['path']
            content_map[patientID][studyUID]['Series'][seriesInstanceUID]['files'] = data['files']

    return content_map

def find_non_intersting_series(json_file_path):
    paths = []
    data = json.load(open(json_file_path))
    series_description = data["series"]["SeriesDescription"]
    if("CT COUPES FINES" in series_description): 
        paths.append( data["path"])
    if("_wb_nac" in series_description): 
        paths.append( data["path"])
    if("POUMON" in series_description):
        paths.append( data["path"])
    if("PARENCHYME" in series_description):
        paths.append( data["path"])
    if("CT ORL" in series_description):
        paths.append( data["path"])

def find_studies_over_two_series(json_merged_file_path):
    data = json.load(open(json_merged_file_path))
    number = 0
    series_to_check=[]
    series_list = []
    for patientID in data:
        for studyUID in data[patientID]:
            if( len(data[patientID][studyUID]['Series']) >2 ):
                number +=1
                for seriesUID in data[patientID][studyUID]['Series']:
                    series_list.append(data[patientID][studyUID]['Series'][seriesUID]['SeriesDescription'])
                    series_to_check.append(data[patientID][studyUID]['Series'])
    print(series_list)
    return series_to_check

def find_studies_with_two_series(json_merged_file_path):
    data = json.load(open(json_merged_file_path))
    matching_series = defaultdict(dict)
    for patientID in data:
        for studyUID in data[patientID]:
            if( len(data[patientID][studyUID]['Series']) == 2 ):
                for seriesUID in data[patientID][studyUID]['Series']:
                    matching_series[seriesUID]['seriesDetails'] = data[patientID][studyUID]['Series'][seriesUID]
                    matching_series[seriesUID]['path'] = data[patientID][studyUID]['Series'][seriesUID]['path']
                    matching_series[seriesUID]['parentStudyUID'] = studyUID
                    matching_series[seriesUID]['parentPatientID'] = patientID
    #pp = pprint.PrettyPrinter(depth=6)
    #pp.pprint(matching_series)
    return matching_series

def remove_path_from_disk(path):
    try:
        shutil.rmtree(path)
    except Exception as err:
        print(err)