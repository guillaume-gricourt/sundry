#!/usr/bin/env python

import argparse
import glob
import json
import os
import shutil

from PIL import Image


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser_input = parser.add_mutually_exclusive_group(required=True)
    parser_input.add_argument("--indir", help="Indir")
    parser_input.add_argument("--input", help="Input")
    parser.add_argument("--outdir", required=True, help="Outdir")
    parser.add_argument("--quality", type=int, default=0, help="Quality")
    parser.add_argument("--size", type=int, default=200, help="Height and Width")
    parser.add_argument("--fmt", default="WebP", choices=["WebP", "PNG"], help="Format")
    args = parser.parse_args()

    outdir = args.outdir
    os.makedirs(outdir, exist_ok=True)

    filenames = []
    if args.input:
        filenames.append(args.input)
    elif args.indir:
        filenames = glob.glob(os.path.join(args.indir, "*"))

    for filename in sorted(filenames):
        basename = os.path.basename(filename)
        basename = ".".join([x for x in basename.split(".")[:-1]])
        data = Image.open(filename)

        # resize
        data = data.resize((args.size, args.size))

        # save
        data.save(
            os.path.join(args.outdir, basename + "." + args.fmt.lower()),
            args.fmt,
            quality=args.quality,
        )
