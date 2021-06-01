import numpy as np 
import SimpleITK as sitk 

def label_stat_results(labelled_img:sitk.Image, pet_img:sitk.Image) :
    """a function to gather stats about each ROI

    Args:
        labelled_img (sitk.Image): []
        pet_img (sitk.Image): [description]

    Returns:
        [type]: [description]
    """
    results = {} 
    stats = sitk.LabelIntensityStatisticsImageFilter()
    stats.Execute(labelled_img, pet_img)
    pet_spacing = pet_img.GetSpacing()
    number_of_label = stats.GetNumberOfLabels()
    results['number_of_label'] =  number_of_label
    volume = 0
    for i in range(1, number_of_label + 1) :
        subresult = {}
        subresult['max'] = stats.GetMaximum(i)
        subresult['mean'] = stats.GetMean(i)
        subresult['median'] = stats.GetMedian(i)
        subresult['variance'] = stats.GetVariance(i)
        subresult['sd'] = stats.GetStandardDeviation(i)
        subresult['number_of_pixel'] = stats.GetNumberOfPixels(i)
        volume_voxel = pet_spacing[0] * pet_spacing[1] * pet_spacing[2] * 10**(-3) #ml
        subresult['volume'] = stats.GetNumberOfPixels(i) * volume_voxel
        subresult['centroid'] = stats.GetCentroid(i)
        volume += stats.GetNumberOfPixels(i) * volume_voxel
        results[i] = subresult
    results['total_vol'] = volume
    return results


def read_img(img_path):
    img = sitk.ReadImage(img_path)
    array = sitk.GetArrayFromImage(img).transpose()
    return array , img.GetSpacing()


def normalize_pet(array):
    x,y,z = np.where(array != 0)
    suv = []
    for j in range(len(x)):
        suv.append(array[x[j], y[j], z[j]])

    suv_max = np.max(suv)

    for i in range(len(x)):
        array[x[i], y[i], z[i]] = (array[x[i], y[i], z[i]] * 255) / suv_max

    return array 

def read_inference(inference_path):
    return sitk.GetArrayFromImage(sitk.ReadImage(inference_path)).transpose()

    
def binarize_mask(mask_array) : 
    size = mask_array.shape 
    binarize = np.zeros(size)
    x,y,z = np.where(mask_array >= 0.5)
    binarize[x,y,z] = 1
    return binarize