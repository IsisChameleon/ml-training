import logging

import fastai
from fastai.vision import *
from fastai.callbacks import *
from fastai.utils.mem import *

from torchvision.models import vgg16_bn

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# set the constants for the content types
JSON_CONTENT_TYPE = 'application/json'
JPEG_CONTENT_TYPE = 'image/jpeg'

if __name__ == '__main__':
    # Script parameters
    parser = ArgumentParser(description='Arguments for the training job')
    parser.add_argument("-u", "--training_data_url", dest="url",
                        help="dataset url e.g. https://s3.amazonaws.com/fast-ai-imageclas/oxford-iiit-pet")
    parser.add_argument("-m", "--model", dest="model",
                        help="location of model"
                        )
    parser.add_argument('--workers', type=int, default=2, metavar='W',
                        help='number of data loading workers (default: 2)')
    parser.add_argument('--epochs', type=int, default=2, metavar='E',
                        help='number of total epochs to run (default: 2)')
    parser.add_argument('--batch_size', type=int, default=64, metavar='BS',
                        help='batch size (default: 4)')
    parser.add_argument('--lr', type=float, default=0.001, metavar='LR',
                        help='initial learning rate (default: 0.001)')
    # fast.ai specific parameters
    parser.add_argument('--image-size', type=int, default=224, metavar='IS',
                        help='image size (default: 224)')
    parser.add_argument('--model-arch', type=str, default='resnet34', metavar='MA',
                        help='model arch (default: resnet34)')

    # This is where the training happens!
    _train(parser.parse_args())


def _train(args):
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    logger.info("Starting _train(). Training device Type: {}".format(device))

    # Loading / locating / creating datasets
    # ---------------------------------------
    logger.info("Loading dataset: {}".format(args.training_data_url))
        
    #Existing datasets already available in Paperspace
    imagenette2_path=Path('/datasets/fastai/imagenette2')
    oxford_iiit_path=Path('/datasets/fastai/oxford-iiit-pet')
    path_pets=oxford_iiit_path
    path_pets_storage=Path('/storage/fastai/oxford-iiit-pet')
    path_hr = imagenette2_path/'train'

    # newly created images to save on persistent storage (/storage on Paperspace, ../SageMaker on AWS )
    root_storage=Path('/storage')
    dataset_storage_path=Path(root_storage/'fastai/imagenette2')
    path_lr = dataset_storage_path/'small-64/train'
    path_mr = dataset_storage_path/'small-256/train'

    logger.info("Original resolution dataset for target images: {}".format(path_hr))
    logger.info("Medium resolution training dataset: {}".format(path_mr))
    logger.info("Low resolution training dataset: {}".format(path_lr))

    # Creating databunch
    il=fastai.vision.ImageList

    path=imagenette2_path
    
    assert path.exists(), f"Imagenet dataset doesn't exist here @ {path}"
    
    sets = [(path_lr, 64), (path_mr, 256)]
    for p,size in sets:
        if not p.exists(): 
            print(f"..resizing images to {size} into {p}")
            parallel(partial(resize_one, path=p, size=size), il.items)




def resize_one(filename, resized_path, hr_path, size):
    dest = resized_path/fn.relative_to(hr_path)
    dest.parent.mkdir(parents=True, exist_ok=True)
    img = PIL.Image.open(filename)
    target_size = resize_to(img, size, use_min=True)
    img = img.resize(target_size, resample=PIL.Image.BILINEAR).convert('RGB')
    img.save(dest, quality=60)