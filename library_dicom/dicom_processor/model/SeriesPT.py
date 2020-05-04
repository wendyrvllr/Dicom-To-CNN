from Series import Series
from math import exp, log, pow
from datetime import datetime

class SeriesPT(Series, object):
    """[summary]

    Arguments:
        Series {[type]} -- [description]
    """

    def __init__(self, path, sul_value=False):
        super(SeriesPT, self).__init__(path)
        self.sul_value=sul_value


    def calculateSUVFactor(self):
        """Calcul of  SUV factor

        Returns:
            [float] -- [return SUV factor or "Calcul SUV impossible" if there is "Undefined" value in tags]
        """
        series_details = Series.get_series_details()
        patient_heigt = series_details['patient']['PatientHeight']
        patient_weight = series_details['patient']['PatientWeight']
        series_time = series_details['series']['SeriesTime']
        series_date = series_details['series']['SeriesDate']
        series_datetime = series_date + series_time #str 
        series_datetime = datetime.strptime(series_datetime, "%Y%m%d%H%M%S") #datetime.datetime


        acquisition_time = series_details['series']['AcquisitionTime']
        acquisition_date = series_details['series']['AcquisitionDate']
        acquisition_datetime = acquisition_date + acquisition_time #str
        acquisition_datetime = datetime.strptime(acquisition_datetime, "%Y%m%d%H%M%S") #datetime.datetime


        modality = series_details['series']['Modality']
        manufacturer = series_details['series']['Manufacturer']
        units = series_details['series']['Units']
        decay_correction = series_details['series']['DecayCorrection']
        radionuclide_half_life = series_details['radiopharmaceutical']['RadionuclideHalfLife']
        total_dose = series_details['radiopharmaceutical']['TotalDose']
        radiopharmaceutical_start_date_time = series_details['radiopharmaceutical']['RadiopharmaceuticalStartDateTime']
        radiopharmaceutical_start_date_time = datetime.strptime(radiopharmaceutical_start_date_time, "%Y%m%d%H%M%S")


        #condition à checker
        if manufacturer == 'Philips' :
            philips_suv_factor = series_details['series']['PhilipsSUVFactor']
            philips_suv_bqml = series_details['series']['PhilipsBqMlFactor']
            if (philips_suv_bqml == 'Undefined') : return ('Calcul SUV impossible')
        
        if units != 'GML' :
            if (total_dose == 'Undefined' or acquisition_time== 'Undefined' 
                or patient_weight == 'Undefined' or radionuclide_half_life == 'Undefined' ) :
                return ('Calcul SUV impossible')

        #heure d'acquisition 
        acquisition_hour = series_datetime
        if (acquisition_date != 'Undefined' and acquisition_time != 'Undefined'
             and acquisition_datetime - series_datetime < 0 and units == 'BQML') : 
            acquisition_hour = acquisition_datetime

        #algo
        #1)
        if units == 'GML' : return 1
        #2)
        if manufacturer =='Philips' : return philips_suv_bqml
        #3)
        if decay_correction != 'ADMIN' : 

            #calcul du facteur de décroissance
            delta = (acquisition_hour - radiopharmaceutical_start_date_time).seconds 
            if delta < 0 : return ("Calcul SUV impossible")

            decay_factor = exp(-delta * log(2) / radionuclide_half_life)

        elif decay_correction == 'ADMIN' : 
            decay_factor = 1
        
        return (1/((total_dose * decay_factor) / patient_weight)) #facteur de conversion SUV
    



    def calculateSULFactor(self):
        """Calcul SUL Factor

        Returns:
            [float] -- [Return SUL Factor or "Calcul SUL impossible" if there is "Undefined" value in tags]
        """
        series_details = Series.get_series_details()
        patient_sex = series_details['patient']['PatientSex']
        patient_weight = series_details['patient']['PatientWeight']
        patient_heigt = series_details['patient']['PatientHeight']
        if (patient_heigt == 'Undefined' or patient_weight == 'Undefined') : 
            return ("Calcul SUL impossible ")
        bmi =  patient_weight / pow(patient_heigt, 2)
        if patient_sex == 'F' : 
            return 9270 / (8780 + 244 * bmi)
        return 9270 / (6680 + 216 * bmi)
    
    def get_numpy_array(self):
        """[summary]

        Returns:
            [array] -- [return array of the SeriesPT with SUV and SUL factor ]
        """
        if self.calculateSUVFactor == 'Calcul SUV impossible' : 
            return ("No conversion")
        numpy_array = Series.get_numpy_array(self)
        numpy_array = numpy_array * self.calculateSUVFactor()
        if(self.sul_value == False): return numpy_array
        else : return ( numpy_array * self.calculateSULFactor() )