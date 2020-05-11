from library_dicom.dicom_processor.model.Series import Series
from library_dicom.dicom_processor.tools.folders import get_series_path
from library_dicom.dicom_processor.tools.series import get_series_object

series_paths = get_series_path('/home/salim/Test dicom MM/151949')
print(series_paths)

for serie_path in series_paths:
    dicom_serie = get_series_object(serie_path)
    dicomsInfo = dicom_serie.get_series_details()
    dicom_serie.export_nifti('/home/salim/testNiftiExport/test.nii')