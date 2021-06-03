import os
from library_dicom.dicom_processor.model.reader.Instance import Instance
from library_dicom.dicom_processor.tools.cleaning_dicom.folders import get_series_path

"""script to scan series and print True if Secondary_Capture, False instead
"""
series_paths = get_series_path('/home/salim/Test dicom MM/151949')
print(series_paths)

for serie_path in series_paths:
    firstFile = os.listdir(serie_path)[0]
    instance = Instance(os.path.join(serie_path,firstFile), load_image=False)
    print(serie_path)
    print(instance.is_secondary_capture())