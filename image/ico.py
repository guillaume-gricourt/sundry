#!/usr/bin/env python

import argparse
import os

from PIL import Image


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Input img")
    parser.add_argument("--output", required=True, help="Output img")
    parser.add_argument("--size", type=int, default=48, help="Size")
    args = parser.parse_args()

    size = args.size
    data = Image.open(args.input)
    data.save(args.output, "ICO", sizes=[(size, size)])
