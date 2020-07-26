# https://docs.fast.ai/tutorial.itemlist.html
# ItemBase : https://github.com/fastai/fastai/blob/54a9e3cf4fd0fa11fc2453a5389cc9263f6f0d77/fastai/core.py#L179

import sys



from fastai.core.torch_core import *
from fastai.core. import *
from .transform import *
from ..data_block import *
from ..basic_data import *
from ..layers import *
from .learner import *
from torchvision import transforms as tvt

class ImageTupleFromOne(ItemBase):
    def __init__(self, img):
        self.img1, self.img2 = self._split(img, split='LR')
        # Here the object is the tuple of images and the data their underlying tensors normalized between -1 and 1.
        self.obj,self.data = (img1,img2),[-1+2*img1.data,-1+2*img2.data]

    def _split(self, img, split:str='LR'):
        #cut the image in 2 
        img1, img2 = img, img
        if split=='LR':
            #to do
            img1, img2 = img, img
        return img1, img2

    def apply_tfms(self, tfms, **kwargs):
        self.img1 = self.img1.apply_tfms(tfms, **kwargs)
        self.img2 = self.img2.apply_tfms(tfms, **kwargs)
        self.data = [-1+2*self.img1.data,-1+2*self.img2.data]
        return self

    def to_one(self): return Image(0.5+torch.cat(self.data,2)/2)


    if __name__ == "__main__":
        print(sys.path)


