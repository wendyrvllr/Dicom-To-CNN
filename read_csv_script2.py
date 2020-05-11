from library_dicom.dicom_processor.model.csv_reader.CsvReader import CsvReader
from library_dicom.dicom_processor.model.csv_reader.RoiFactory import RoiFactory

csv_reader = CsvReader('/home/salim/Bureau/5986298233_jun 22_2011.csv')
csv_reader = CsvReader('/home/salim/Bureau/11009101406003_apr 14_2010.csv')


manual_rois = csv_reader.get_manual_rois()
automatic_rois = csv_reader.get_nifti_rois()

for manual_roi in manual_rois:
    roi_object = csv_reader.convert_manual_row_to_object(manual_roi)
    print(roi_object)
    roi_factory1 = RoiFactory(roi_object, (256,256,512), 1)
    roi1 = roi_factory1.read_roi()
    mask1 = roi1.calculateMaskPoint()
    print(mask1)
#roi_object = csv_reader.convert_nifti_row_to_list_point(manual_rois[0])



#CODE DE THOMAS 
# MIP creat_MIP_Projection : 
import scipy
a = scipy.ndimage.interpolation.rotate(img, angles = 0, axes=(0,1), reshape = bool)
#rotate en array in the plane defined by the 2 axis given
#axes = (1,0) and (0,1) is the same, which is x any y axes. The rotation plane is x-y plane.
#axes = (1,2) and (2,1) is the same, which is y any z axes. The rotation plane is y-z plane.
#axes = (2,0) and (0,2) is the same, which is x any z axes. The rotation plane is x-z plane

MIP = np.amax(a, axis = 1 ) #a = 2D, return max de chaque ligne 
# pour matrice 3D
# axe = 0 x
#axe = 1 y 
# axe = 2 z 


