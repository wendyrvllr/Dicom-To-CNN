import os

from library_dicom.dicom_processor.model.Series import Series
from library_dicom.dicom_processor.model.Instance import Instance
from library_dicom.dicom_processor.tools.folders import get_series_path
from library_dicom.dicom_processor.tools.series import get_series_object

series_paths = get_series_path('/home/salim/Test dicom MM/151949')
print(series_paths)

for serie_path in series_paths:
    firstFile = os.listdir(serie_path)[0]
    instance = Instance(os.path.join(serie_path,firstFile), load_image=False)
    print(serie_path)
    print(instance.is_secondary_capture())