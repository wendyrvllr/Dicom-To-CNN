from library_dicom.dicom_processor.model.Series import Series
from math import exp, log, pow
from datetime import datetime, timedelta

class SeriesPT(Series):
    """[summary]

    Arguments:
        Series {[class]} -- [description]
    """

    def __init__(self, path, sul_value=False):
        super().__init__(path)
        self.sul_value=sul_value


    def get_series_details(self):
        """Add Pharmaceuticals data to common series details

        Returns:
            [dict] -- [Return the details of a SeriePT from the first Dicom]
        """
        details = super().get_series_details()
        dicomInstance = self.get_first_instance_metadata()
        self.radiopharmaceutical_details = {}
        self.radiopharmaceutical_details = dicomInstance.get_radiopharmaceuticals_tags()
        details['radiopharmaceutical'] = self.radiopharmaceutical_details
        self.pet_correction_details = {}
        self.pet_correction_details = dicomInstance.get_pet_correction_tags()
        details['pet_correction'] = self.pet_correction_details
        self.philips_tag = {}
        self.philips_tag = dicomInstance.get_philips_private_tags()
        details['philips_tags'] = self.philips_tag

        return details

    def __calculateSUVFactor(self):
        """Calcul of  SUV factor

        Returns:
            [float] -- [return SUV factor or "Calcul SUV impossible" if there is "Undefined" value in tags]
        """
        series_details = self.get_series_details()
        units = series_details['series']['Units']
        if units == 'GML' : return 1
        
        patient_weight = series_details['study']['PatientWeight']
        patient_weight = patient_weight * 1000
        series_time = series_details['series']['SeriesTime']
        series_date = series_details['series']['SeriesDate']
        series_datetime = series_date + series_time #str 

        if '.' in series_datetime : 
            series_datetime = series_datetime[0 : series_datetime.index('.')]

        
        series_datetime = datetime.strptime(series_datetime, "%Y%m%d%H%M%S") #datetime.datetime
        

        acquisition_time = series_details['series']['AcquisitionTime']
        acquisition_date = series_details['series']['AcquisitionDate']
        acquisition_datetime = acquisition_date + acquisition_time #str

        if '.' in acquisition_datetime : 
            acquisition_datetime = acquisition_datetime[0 : acquisition_datetime.index('.')]
        
        acquisition_datetime = datetime.strptime(acquisition_datetime, "%Y%m%d%H%M%S") #datetime.datetime
        
        #modality = series_details['series']['Modality']
        manufacturer = series_details['series']['Manufacturer']
        decay_correction = series_details['series']['DecayCorrection']
        radionuclide_half_life = series_details['radiopharmaceutical']['RadionuclideHalfLife']
        total_dose = series_details['radiopharmaceutical']['TotalDose']

        #ICI SK Probleme de vieux tag a explorer

        radiopharmaceutical_start_date_time = series_details['radiopharmaceutical']['RadiopharmaceuticalStartDateTime']
        if radiopharmaceutical_start_date_time == 'Undefined':
            radiopharmaceutical_start_time = series_details['radiopharmaceutical']['RadiopharmaceuticalStartTime']
            radiopharmaceutical_start_date_time = acquisition_date + radiopharmaceutical_start_time 
            
        if '.' in radiopharmaceutical_start_date_time : 
            radiopharmaceutical_start_date_time = radiopharmaceutical_start_date_time[0 : radiopharmaceutical_start_date_time.index('.')]

        radiopharmaceutical_start_date_time = datetime.strptime(radiopharmaceutical_start_date_time, "%Y%m%d%H%M%S")
    

        if manufacturer == 'Philips' :
            #philips_suv_factor = series_details['series']['PhilipsSUVFactor']
            philips_suv_bqml = series_details['philips_tags']['PhilipsBqMlFactor']
            if (philips_suv_bqml == 'Undefined') : raise Exception('Missing Philips BqMl Factor')
        
        if (total_dose == 'Undefined' or acquisition_time== 'Undefined' 
            or patient_weight == 'Undefined' or radionuclide_half_life == 'Undefined' ) :
            raise Exception('Missing Radiopharmaceutical data or patient weight')
        
        #Determine Time reference of image acqusition 
        acquisition_hour = series_datetime
        if (acquisition_date != 'Undefined' and acquisition_time != 'Undefined'
             and (acquisition_datetime - series_datetime).total_seconds() < 0 and units == 'BQML') : 
            acquisition_hour = acquisition_datetime
        
        #Calculate decay correction
        if decay_correction == 'START' : 
            delta = (acquisition_hour - radiopharmaceutical_start_date_time)
            delta = delta.total_seconds()
            if (delta < 0) : raise("Acqusition time before injection time")
            decay_factor = exp(-delta * log(2) / radionuclide_half_life)

        #If decay corrected from administration time no decay correction to apply
        elif decay_correction == 'ADMIN' : 
            decay_factor = 1

        else : raise Exception('Unknown Decay Correction methode')
        
        suv_conversion_factor = (1/((total_dose * decay_factor) / patient_weight))

        if manufacturer =='Philips' : return philips_suv_bqml * suv_conversion_factor
        else : return suv_conversion_factor
    

    def calculateSULFactor(self):
        """Calcul SUL Factor

        Returns:
            [float] -- [Return SUL Factor or "Calcul SUL impossible" if there is "Undefined" value in tags]
        """
        series_details = self.get_series_details()
        patient_sex = series_details['patient']['PatientSex']
        patient_weight = series_details['study']['PatientWeight']
        patient_height = series_details['study']['PatientHeight']
        if (patient_sex == 'Undefined' or patient_height == 'Undefined' or patient_weight == 'Undefined' or patient_height == 0.0) : 
            raise Exception('Missing Height or Weight to calculate SUL')
        bmi =  patient_weight / pow(patient_height, 2)
        if patient_sex == 'F' : 
            return 9270 / (8780 + 244 * bmi)
        return 9270 / (6680 + 216 * bmi)
    

    def is_corrected_attenuation(self):
        series_details = self.get_series_details()
        corrected_image = series_details['pet_correction']
        if 'ATTN' in corrected_image : return True
        else : return False


    
    def get_numpy_array(self):
        """[summary]

        Returns:
            [array] -- [return array of the SeriesPT with SUV and SUL factor in 32bis npArray ]
        """
        numpy_array = super().get_numpy_array()
        try:
            if (self.sul_value == False) :
                return numpy_array * self.__calculateSUVFactor()
            else :
                return numpy_array * self.__calculateSUVFactor() * self.calculateSULFactor()
        except Exception as err:
            print("Error generating result array", err)