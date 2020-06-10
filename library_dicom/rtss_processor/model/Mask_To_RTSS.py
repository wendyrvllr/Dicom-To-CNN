import cv2 
import numpy as np 


class Mask_To_RTSS:
    """build a DicomRT from a Mask 
    """
    def __init__(self, mask): 
        self.mask = mask #3D numpy array
        self.x = mask.shape[0]
        self.y = mask.shape[1]
        self.z = mask.shape[2]
        self.number_of_roi = mask.shape[3]



    def get_contour_ROI(self, number_roi):

        results = {}
        slice = []

        binary_mask = np.array(self.mask[:,:,:,number_roi - 1], dtype=np.uint8)

        for s in range(self.z):
            contours, _ = cv2.findContours(binary_mask[:,:, s], cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE) 
            if (contours != []) : 
                results[s] = contours
                slice.append(s)

        return results, slice 


    def pixel_to_spatial(self, number_roi, dicom_origin, dicom_spacing, list_all_SOPInstanceUID):

        
        list_contours = []
        list_SOPInstanceUID = []
        x0,y0,z0 = dicom_origin
        dx,dy,dz = dicom_spacing
        dict_contours, list_slice = self.get_contour_ROI(number_roi)

        number_contour = len(dict_contours)

        for i in range(number_contour): #plusieurs contours dans une même slice 
            number_of_contour_in_slice = len(dict_contours[list_slice[i]])
            for j in range(number_of_contour_in_slice)  : 
                number_point_contour = len(dict_contours[list_slice[i]][j])

                liste = []

                for point in range(number_point_contour): #[x,y]
                    x = dict_contours[list_slice[i]][j][point][0][0]
                    liste.append(x0 + x*dx + dx/2 )
                    y = dict_contours[list_slice[i]][j][point][0][1]
                    liste.append( y0 + y*dy + dy/2)
                    z = list_slice[i] 
                    liste.append(z0 + z*dz )

                list_SOPInstanceUID.append(list_all_SOPInstanceUID[z])
                list_contours.append(liste)

        return list_contours, list_SOPInstanceUID






                



        
            


            







        
    


#1) convert mask to roi rtss
#2) create RTStruct from a mask => fichier .dcm 
 
#code de thomas 
#voir comment on réorganise 


