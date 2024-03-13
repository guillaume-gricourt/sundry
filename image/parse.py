#!/usr/bin/env python

import argparse
import glob
import json
import os
import shutil
import tempfile

import pandas as pd
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
    return dict(tl=tl, tr=tr, bl=bl, br=br)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Input file csv")
    parser.add_argument("--outdir", required=True, help="Outdir")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite")
    args = parser.parse_args()

    outdir = args.outdir
    is_overwrite = False
    if args.overwrite:
        is_overwrite = True
    os.makedirs(outdir, exist_ok=True)

    input_file = args.input
    if not os.path.isfile(input_file):
        print("File does not exist", input_file)
        parser.exit(1)

    df = pd.read_csv(input_file, sep=";")
    dirname = os.path.dirname(input_file)
    ftemp = tempfile.NamedTemporaryFile(suffix=".png").name

    for ix in df.index:
        name = df.loc[ix, "name"]
        foutput = os.path.join(args.outdir, df.loc[ix, "section"], name + ".webp")
        print("Deal with:", name)
        if os.path.isfile(foutput) and not is_overwrite:
            print("\tAlready exists -> skip !")
            continue
        # Filename
        filename = df.loc[ix, "filename"]
        if not filename.endswith("png"):
            filename += ".png"
        print(dirname, filename)
        paths = glob.glob(os.path.join(dirname, "**", filename), recursive=True)
        assert len(paths) == 1
        path = paths[0]
        # Crop
        data = skimage.io.imread(path)
        datas = crop(data=data)
        data = datas[df.loc[ix, "crop"]]
        skimage.io.imsave(ftemp, data)
        # Resize
        data = Image.open(ftemp)
        data = data.resize((df.loc[ix, "size"], df.loc[ix, "size"]))
        os.makedirs(os.path.dirname(foutput), exist_ok=True)
        data.save(foutput, "WebP", quality=df.loc[ix, "quality"])
