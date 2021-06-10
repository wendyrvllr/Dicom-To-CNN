import SimpleITK as sitk 
import abc 

class Abstract_Writer(abc.ABCMeta) : 
    """abstract class to write segmentation
    """

    def __init__(self, mask_img:sitk.Image):
        self.mask_img = mask_img

    @abc.abstractmethod
    def save_file(self, filename:str, directory_path:str) -> None :
        pass 

