import os
import json

def get_series_path(path:str) -> list :
    """Go through all the folder to find every series path

    Arguments:
        path {[string]} -- [Absolute path where the repertory is located]

    Returns:
        [list] -- [Path's list of every series]
    """

    seriesPath = []
    for (path, dirs, files) in os.walk(path): 
        if not (dirs) :
            seriesPath.append(path)
    return seriesPath


def write_json_file(path:str, file_name:str, content:list, extension:str = 'json'):
    """write and save a json file

    Args:
        path (str): [directory's path where to save json file]
        file_name (str): [name of the json file]
        content (list): [what to write in the json file]
        extension (str, optional): [description]. Defaults to 'json'.
    """
    wrinting_file = open(os.path.join(path, file_name+'.'+extension), 'w')
    wrinting_file.write(json.dumps(content))
    wrinting_file.close()

def remove_bi_file(path:str):
    """remove bi file of a dicom serie

    Args:
        path (str): [directory's path of the serie]
    """
    file_names = os.listdir(path)
    if('graphic.brownFat.gr2' in file_names):
        os.remove( os.path.join(path,"graphic.brownFat.gr2") )

def remove_index_ini(path:str):
    """remove index ini of a dicom serie

    Args:
        path (str): [directory's path of the serie]
    """
    file_names = os.listdir(path)
    if ('index.ini' in file_names):
        os.remove(os.path.join(path, 'index.ini'))

def remove_empty_folders(path:str):
    """remove serie with no dicom file in it 

    Args:
        path (str): [directory's path of a dicom serie]

    """
    list_instances = os.listdir(path)
    if len(list_instances) == 0 : 
        os.remove(path)
