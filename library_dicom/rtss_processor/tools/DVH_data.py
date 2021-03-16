from library_dicom.dicom_processor.model.reader.Instance_RTDose import Instance_RTDose
import matplotlib.pyplot as plt 
import plotly_express as px 
import pandas as pd 
import numpy as np 


def convert_str_list_to_float_list(str_liste):
    empty_list = []
    for i in range(len(str_liste)):
        empty_list.append(float(str_liste[i]))
    return empty_list 


def generate_x_y_cumul(liste):
    x = []
    y = []
    somme = 0
    for i in range(len(liste)) : 
        if i%2 == 1 : 
            y.append(liste[i])
        else : 
            somme += liste[i]
            x.append(somme)
    return x,y 

def generate_plot(dictionnary):
    keys = list(dictionnary.keys())
    s = []
    for key in keys : 
        data_str = dictionnary[key]['DVHData']
        name = dictionnary[key]['ReferencedROIName']
        data_float = convert_str_list_to_float_list(data_str)
        x,y = generate_x_y_cumul(data_float)

        #normalize 
        normalize_vol = []
        maxi = np.max(y)
        for vol in y : 
            normalize_vol.append(vol / maxi * 100)


        #subliste = []
        for i in range(len(x)):
            subliste = []
            subliste.append(name)
            subliste.append(x[i])
            subliste.append(normalize_vol[i])
            #print(subliste)
            s.append(subliste)

    df = pd.DataFrame(s, columns=['ROIname', 'dose', 'volume'])
    fig = px.line(df, x="dose", y="volume", color='ROIname')
    fig.show()

    return None 

    

