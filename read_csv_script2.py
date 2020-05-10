from library_dicom.dicom_processor.model.csv_reader.CsvReader import CsvReader
from library_dicom.dicom_processor.model.csv_reader.RoiFactory import RoiFactory

csv_reader = CsvReader('/home/salim/Bureau/5986298233_jun 22_2011.csv')

manual_rois = csv_reader.get_nifti_rois()

#roi_object = csv_reader.convert_manual_row_to_object(manual_rois[3])
roi_object = csv_reader.convert_nifti_row_to_list_point(manual_rois[0])

print(manual_rois)
print(roi_object)
roi_factory1 = RoiFactory(roi_object, (256,256,512), 1)
roi1 = roi_factory1.read_roi()
mask1 = roi1.calculateMaskPoint()
