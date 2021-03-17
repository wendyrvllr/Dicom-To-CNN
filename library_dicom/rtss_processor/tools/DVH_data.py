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

def generate_plot(dictionnary, mode = 'cumulative', dose_mode = 'Gray', volume_mode = '%'):
    """[summary]

    Args:
        dictionnary ([type]): [description]
        mode (str, optional): ['cumulative' or 'differentiel' only]. Defaults to 'cumulative'.
        dose_mode (str, optional): ['%' or 'Gray' only ]. Defaults to 'Gray'.
        volume_mode (str, optional): ['%' or 'cc' only ]. Defaults to '%'.

    Returns:
        [type]: [description]
    """
    keys = list(dictionnary.keys())
    dataframe  = []
    for key in keys : 
        data_str = dictionnary[key]['DVHData']
        name = dictionnary[key]['ReferencedROIName']
        data_float = convert_str_list_to_float_list(data_str)
        x,y = generate_x_y_cumul(data_float)


        if mode == 'cumulative' : 

            #volume
            if volume_mode == '%' : 
                new_y = []
                maxi = np.max(y)
                for vol in y : 
                    new_y.append(vol / maxi * 100)
            elif volume_mode == 'cc' : 
                new_y = y 
            else : print('Mode not available')


            #dose 
            if dose_mode == 'Gray' : 
                new_x = x 
            elif dose_mode == '%' : 
                new_x = []
                maxi = np.max(x)
                for rayon in x : 
                    new_x.append(rayon/maxi * 100 )
            else : print('Mode not available')


            for i in range(len(new_x)):
                subliste = []
                subliste.append(name)
                subliste.append(new_x[i])
                subliste.append(new_y[i])
                dataframe.append(subliste)

        if mode == 'differentiel' : 
            #conversion volume to differentiel 
            differentiel = []
            y.reverse()
            differentiel.append(y[0])
            for i in range(1, len(y)):
                differentiel.append(abs(y[i] - y[i-1]))

            #volume 
            if volume_mode == '%' : 
                new_y = []
                maxi = np.max(differentiel)
                for vol in differentiel : 
                    new_y.append(vol / maxi * 100)
            elif volume_mode == 'cc' : 
                new_y = differentiel
            else : print('Mode not available')

            new_y.reverse()

            #dose 
            if dose_mode == 'Gray' : 
                new_x = x 
            elif dose_mode == '%' : 
                new_x = []
                maxi = np.max(x)
                for rayon in x : 
                    new_x.append(rayon/maxi * 100 )
            else : print('Mode not available')

            for i in range(len(new_x)):
                subliste = []
                subliste.append(name)
                subliste.append(new_x[i])
                subliste.append(new_y[i])
                dataframe.append(subliste)


    df = pd.DataFrame(dataframe, columns=['ROIName', "dose_{}".format(dose_mode), "volume_{}".format(volume_mode)])
    fig = px.line(df, x="dose_{}".format(dose_mode), y="volume_{}".format(volume_mode), color='ROIName', title=mode, width = 750, height = 550)
    fig.show()

    return None 

    

