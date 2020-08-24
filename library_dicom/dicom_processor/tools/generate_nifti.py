import SimpleITK as sitk 
import numpy as np

def generate_nifti(numpy_array, origin, direction, spacing, filename):
    img = sitk.GetImageFromArray(numpy_array.astype(np.uint8))
    img.SetDirection(direction)
    img.SetOrigin(origin)
    img.SetSpacing(spacing)
    sitk.WriteImage(img, filename)
