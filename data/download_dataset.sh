#!/bin/bash
FILE=$1
DEST=$2

if [[ $FILE != "cityscapes" &&  $FILE != "night2day" &&  $FILE != "edges2handbags" && $FILE != "edges2shoes" && $FILE != "facades" && $FILE != "maps" ]]; then
  echo "Available datasets are cityscapes, night2day, edges2handbags, edges2shoes, facades, maps"
  exit 1
fi

echo "Specified [$FILE]"
echo "Destination [$DEST]"

URL=http://efrosgans.eecs.berkeley.edu/pix2pix/datasets/$FILE.tar.gz
TAR_FILE=$DEST/$FILE.tar.gz
TARGET_DIR=$DEST/$FILE/
echo "Downloading ${TAR_FILE} into dest folder ${TARGET_DIR}..."
wget -v --show-progress -N $URL -O $TAR_FILE
mkdir -p $TARGET_DIR
tar -zxvf $TAR_FILE -C $DEST/
rm $TAR_FILE