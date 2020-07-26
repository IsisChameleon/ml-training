
import logging
import sys, os
from argparse import ArgumentParser
from pathlib import Path
from PIL import Image
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


def split_domino(domino_loc:str, list_subfolders=['train', 'val']):

    logger.info(f'Starting split_domino to split images in ${domino_loc} for folders ${list_subfolders}')

    for sf in list_subfolders:
        current_path=Path(domino_loc)/sf
        # os.mkdir(str(current_path/'Xs'))
        # os.mkdir(str(current_path/'Ys'))
        print(f"Directory to create {current_path/'Xs'}")
        print(f"Directory to create {current_path/'Ys'}")
        for file in get_files(path=current_path, extensions=['.jpg'], recurse=False ):
            print(f"File to split ${file}")







if __name__ == '__main__':
    # Script parameters
    parser = ArgumentParser(description='Arguments to split the domino jpeg Xs and Ys images')
    parser.add_argument("-l", "--domino_location", dest="domino_loc",
                        help="domino image folder containing the train, val and test folder e.g. ./data/maps")
    args = parser.parse_args()

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    split_domino(args.domino_loc)


        