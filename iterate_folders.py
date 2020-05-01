from library_dicom.dicom_processor.model.Series import Series
from library_dicom.dicom_processor.tools.folders import getSeriesPath

series_paths = getSeriesPath('/home/salim/12345 ANON ANON/')
print(series_paths)

for serie_path in series_paths:
    dicom1 = Series(serie_path)
    dicomsInfo = dicom1.get_series_details()