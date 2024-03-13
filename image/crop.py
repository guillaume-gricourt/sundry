#!/usr/bin/env python

import argparse
import glob
import json
import os
import shutil

from PIL import Image
import skimage
from skimage import io


def filter_img(data) -> bool:
    if data.shape[0] < 1025 or data.shape[1] < 1025:
        return True
    return False


def crop(data):
    x_middle = int(data.shape[0] / 2)
    y_middle = int(data.shape[1] / 2)

    tl = skimage.util.crop(data, ((0, x_middle), (0, y_middle), (0, 0)), copy=True)
    tr = skimage.util.crop(data, ((0, x_middle), (y_middle, 0), (0, 0)), copy=True)
    br = skimage.util.crop(data, ((x_middle, 0), (y_middle, 0), (0, 0)), copy=True)
    bl = skimage.util.crop(data, ((x_middle, 0), (0, y_middle), (0, 0)), copy=True)
    return [tl, tr, bl, br]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--indir", required=True, help="Indir")
    parser.add_argument("--outdir", required=True, help="Outdir")
    args = parser.parse_args()

    outdir = args.outdir
    os.makedirs(outdir, exist_ok=True)

    filenames = glob.glob(os.path.join(args.indir, "*.png"))

    files_to_compress = []
    for filename in sorted(filenames):
        basename = os.path.basename(filename).replace(".png", "")
        data = skimage.io.imread(filename)
        print("Deal with:", filename)
        datas = crop(data=data)
        for ij, data in enumerate(datas):
            outfile = os.path.join(outdir, basename + ".%s.png" % (ij,))
            skimage.io.imsave(outfile, data)
