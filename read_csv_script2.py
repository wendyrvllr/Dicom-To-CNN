from library_dicom.dicom_processor.model.csv_reader.CsvReader import CsvReader
from library_dicom.dicom_processor.model.csv_reader.RoiFactory import RoiFactory

csv_reader = CsvReader('/home/salim/Bureau/11009101406003_apr 14_2010.csv')

manual_rois = csv_reader.get_manual_rois()

roi_object = csv_reader.convert_manual_row_to_object(manual_rois[3])

print(manual_rois)
print(roi_object)
roi_factory1 = RoiFactory(roi_object, (256,256,512), 1)
roi1 = roi_factory1.read_roi()
mask1 = roi1.calculateMaskPoint()
