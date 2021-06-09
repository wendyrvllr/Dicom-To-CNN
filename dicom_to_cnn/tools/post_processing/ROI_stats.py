import numpy as np 
import SimpleITK as sitk 

def label_stat_results(labelled_img:sitk.Image, pet_img:sitk.Image) -> dict :
    """a function to gather stats about each ROI

    Args:
        labelled_img (sitk.Image): [3D segmentation sitk.Image with label]
        pet_img (sitk.Image): [3D pet sitk.Image]

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

