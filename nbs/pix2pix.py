# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from IPython import get_ipython

# %%
import fastai
from fastai.vision import *

# %% [markdown]
# # Dataset Download
# %% [markdown]
# 

# %%
#!cd /storage && mkdir pix2pix && cd pix2pix && mkdir data

get_ipython().system('cd .. && mkdir storage && cd storage && mkdir pix2pix && cd pix2pix && mkdir data')


# %%



# %%
get_ipython().system('pip install wget')


# %%
# https://pypi.org/project/wget/
# https://docs.python.org/2/library/tarfile.html
import tarfile
import wget

downloaded_tars=list()
def get_tar(url: str, dest: str):
    filename = wget.download(url, dest)
    downloaded_tars.append({'path':dest, 'filename':filename})
    return filename

def _opentar(fname: str):
    tar=None
    if (fname.find('.tar') and fname.endswith('.gz')):
        tar = tarfile.open(fname, "r:gz")
    elif (fname.endswith(".tar")):
        tar = tarfile.open(fname, "r:")
    return tar

def untar(fname: str, dest:str='.'):
    tar = _opentar(fname)
    tar.list()
    tar.extractall(path=dest)
    tar.close()

def viewtar(fname: str):
    tar = _opentar(fname)
    tar = tarfile.open(fname, "r:gz")
    tar.list()
    tar.close()

def getuntarsize(fname: str):
    tar = _opentar(fname)
    tar = tarfile.open(fname, "r:gz")
    # to do
    tar.close()


# %%
wget.download('http://efrosgans.eecs.berkeley.edu/pix2pix/datasets/maps.tar.gzhttp://efrosgans.eecs.berkeley.edu/pix2pix/datasets/maps.tar.gz', 'storage/pix2pix/data''storage/pix2pix/data')


# %%
url_dataset='http://efrosgans.eecs.berkeley.edu/pix2pix/datasets/maps.tar.gz'
# on gradient : dest='/storage/pix2pix/data'
dest='storage/pix2pix/data'


# %%
## ONLY EXECUTE FIRST TIME to download the dataset tar and extract it all
print(url_dataset)
print(dest)
filename=get_tar(url_dataset, dest)
print(filename)
print(dest)
untar(filename, dest)


# %%
print(dest)
os.listdir(dest)
#!rm /storage/pix2pix/data/maps.tar (1).gz


# %%
for t in downloaded_tars:
    print(t.filename)
    print(t.path)


# %%
# Setting up dataset path for fastai
path=Path(dest + '/maps')
path

# %% [markdown]
# # PREPARING DATA FOR TRAINING
# %% [markdown]
# Each image will be loaded, rescaled, and split into the satellite and Google map elements. The result will be 1,097 color image pairs with the width and height of 256×256 pixels.

# %%
get_ipython().system('ls ../storage/pix2pix/data/maps')


# %%
# Set those variables if running independently from the data set download
dest='../storage/pix2pix/data'
path=Path(dest,'maps')
pathXs=path/'Xs'
pathYs=path/'Ys'


# %%
pathXs.is_dir()


# %%
il = ImageList.from_folder(pathXs, presort=True).split_by_folder(train='train', valid='val')
type(il)



# %%
ImageImageList


# %%
iil = ImageImageList.from_folder(pathXs, presort=True).split_by_folder(train='train', valid='valid')


# %%



# %%
iil.valid


# %%
iil.train


# %%
iil.items[10]


# %%
iil.valid.items[10]


# %%
On writing your won item list : https://docs.fast.ai/data_block.html#ItemList


# %%
iil.lists[0]


# %%
iil.lists[1]


# %%
iil.lists[1][10]


# %%
index=iil.train.items[0].parts.index('Xs')
new_path = Path(*iil.train.items[0].parts[:index]).joinpath(Path('Ys',*iil.train.items[0].parts[index+1:]))
print(new_path)
type(iil.train.items[0])

def getYsfromXs(x:Path, xFolder:str='Xs', yFolder:str='Ys'):
    index=x.parts.index(xFolder)
    newPath=Path(*x.parts[:index]).joinpath(Path(yFolder,*x.parts[index+1:]))
    return newPath

myPath=getYsfromXs(iil.train.items[1])
print(myPath)


# %%
def get_data(iil:ImageImageList, bs:int,size:int):
    ''' Takes an ImageImageList in iil and return a databunch with images of size=size and training batch size= bs '''
    data = (iil.label_from_func(getYsfromXs)
           .transform(get_transforms(max_zoom=2.), size=size, tfm_y=True)
           .databunch(bs=bs).normalize(imagenet_stats, do_y=True))

    data.c = 3
    return data


# %%
bs = 16
size = 100


# %%
data = get_data(iil=iil, bs=16,size=100)


# %%
from PIL import Image

def _plot(i,j,ax): 
    images = [ data.train_ds[0][0], data.train_ds[0][1] ]
    widths, heights = zip(*(i.size for i in images))

    total_width = sum(widths)
    max_height = max(heights)
    new_im = Image.new('RGB', (total_width, max_height))

    x_offset = 0
    for im in images:
        new_im.paste(im, (x_offset,0))
        x_offset += im.size[0]

    new_im.show(ax)

plot_multi(_plot, 3, 3, figsize=(8,8))





# %%
import sys
sys.path.append(r'/home/isischameleon/Dropbox/Coding/gitrepos/ml-training')
import functools

from model.networks import NLayerDiscriminator

model = NLayerDiscriminator().model

# %%

learn = Learner(data, model, loss_func = nn.CrossEntropyLoss(), metrics=accuracy)




# %%

learn.summary()



# %%
