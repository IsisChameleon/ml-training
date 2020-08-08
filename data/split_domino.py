
import logging
import sys, os
from argparse import ArgumentParser
from pathlib import Path
from PIL import Image, JpegImagePlugin
from fastai.data_block import get_files


def load_images(path, size=(256,512)):
	src_list, tar_list = list(), list()
	# enumerate filenames in directory, assume all are images
	for filename in listdir(path):
		# load and resize the image
		pixels = load_img(path + filename, target_size=size)
		# convert to numpy array
		pixels = img_to_array(pixels)
		# split into satellite and map
		sat_img, map_img = pixels[:, :256], pixels[:, 256:]
		src_list.append(sat_img)
		tar_list.append(map_img)
	return [asarray(src_list), asarray(tar_list)]

def split_image(imgPath: Path):
    try:
        im = Image.open(imgPath)
        w, h = im.size
        im1 = im.crop((0, 0, w/2, h))
        im2 = im.crop((w/2, 0, w, h))
        return (im, im1, im2)

    except BaseException as e:
        print(f"Exception {e} occured")
        logger.error(f"Exception {e} occured")

def save_image(img: Image, original_img: Image, fp: Path):
    # How to save an image with same quality as original? https://stackoverflow.com/questions/4354543/determining-jpg-quality-in-python-pil#4355281
    # https://jdhao.github.io/2019/07/20/pil_jpeg_image_quality/
    # https://pillow.readthedocs.io/en/stable/reference/JpegPresets.html
    # http://code.nabla.net/doc/PIL/api/PIL/PIL.JpegImagePlugin.html
    frmt = original_img.format

    if frmt == 'JPEG':
        quantization = getattr(original_img, 'quantization', None)
        subsampling = JpegImagePlugin.get_sampling(original_img)
        img.save(fp, format=frmt, subsampling=subsampling, qtables=quantization)
    else:
        img.save(fp, format=frmt)
    pass

def split_domino(domino_loc:str, list_subfolders=['train', 'val']):

    logging.info(f'Starting split_domino to split images in ${domino_loc} for folders ${list_subfolders}')

    for sf in list_subfolders:
        current_path=Path(domino_loc)/sf

        Path(domino_loc,'Xs',sf).mkdir(parents=True, exist_ok=True)
        Path(domino_loc,'Ys',sf).mkdir(parents=True, exist_ok=True)

        for file in get_files(path=current_path, extensions=['.jpg'], recurse=False ):
            (original_img, img1, img2) = split_image(imgPath=file)
            save_image(img=img1, original_img=original_img, fp=Path(domino_loc,'Xs',sf)/file.name)
            save_image(img=img2, original_img=original_img, fp=Path(domino_loc,'Ys',sf)/file.name)




if __name__ == '__main__':
    # Script parameters
    parser = ArgumentParser(description='Arguments to split the domino jpeg Xs and Ys images')
    parser.add_argument("-l", "--domino_location", dest="domino_loc",
                        help="domino image folder containing the train, val and test folder e.g. ./data/maps")
    args = parser.parse_args()

    logger = logging.getLogger("split_domino")
    logger.setLevel(logging.DEBUG)

    split_domino(args.domino_loc)


        