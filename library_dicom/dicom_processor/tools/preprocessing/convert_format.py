import SimpleITK as sitk 


def convert_format_nifti_mask(nifti_path, destination):
    """Convert 8Bits UINT nifti mask to 32Bits UINT nifti mask

    Args:
        nifti_path ([str]): [path of the nifti file ]
        destination ([str]): [directory destination]
        filename ([str]): [destination filename ]
    """

    img = sitk.ReadImage(nifti_path)
    img = sitk.Cast(img, sitk.sitkUInt32)
    filename = nifti_path.split('/')[-1][0]
    sitk.WriteImage(img, os.path.join(destination,  filename))
    return None 
