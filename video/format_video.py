#!/usr/bin/env python3

import glob
import os
import re
import subprocess
import sys

indir = os.getcwd()
if len(sys.argv) > 1:
    indir = sys.argv[1]


# List files
finputs = glob.glob(os.path.join(indir, "*.mkv"))
finputs += glob.glob(os.path.join(indir, "*.avi"))
finputs = sorted(finputs)

for finput in finputs:
    basename = os.path.basename(finput)
    m = re.search(r"S\d{2}E(\d{2})", basename)
    if m is None:
        labels = basename.split(".")[:-1]
    else:
        # Format Series
        label = ""
        short = basename[: m.span()[0]]
        shorts = re.split(r"[\.]", short)
        for text in shorts:
            if text == "":
                continue
            text = text.lower()
            text = text[0].upper() + text[1:]
            label += text

        labels = [label]
        labels.append(m.group(0))

    labels.append("mp4")
    label = ".".join(labels)

    args = ["ffmpeg", "-i", finput, label]
    print("Run:", " ".join(args))
    ret = subprocess.run(args, stderr=sys.stderr, stdout=sys.stdout)
    if ret.returncode < 1:
        print("Clean up", finput)
        os.remove(finput)
