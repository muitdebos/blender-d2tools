from PIL import Image


import os
import glob
import math
import argparse

########
# Main #
########

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", dest = "input", help = "Name of input file. Defaults to './palette.png'")
parser.add_argument("-o", "--output", dest = "output", help = "Name of output text file. Defaults to './palette.txt'")
parser.add_argument("--verbose", dest = "verbose", action='store_true', help = "Verbose logging")
parser.set_defaults(input = "./palette.png")
parser.set_defaults(output = "palette.txt")
args = parser.parse_args()

image_paths = glob.glob(args.input)
if (len(image_paths) <= 0):
    print("Error: Did not find any images. Please check your --input arg. By default, it's \"./renders/*.png\".\nNote that you may need to escape special characters (e.g. ./$1TRLITNUHTH_*.png should become ./\$1TRLITNUHTH_*.png).")
    quit()

with Image.open(image_paths[0]) as img:
    output = []
    img = img.convert("RGB")

    imgdata = list(img.getdata())

    for c in imgdata:
        r = str(c[0]).rjust(3, " ")
        g = str(c[1]).rjust(3, " ")
        b = str(c[2]).rjust(3, " ")
        output.append(f"{r} {g} {b}")

    if (args.verbose):
        print("\n".join(output))

    filename = args.output + ".txt"
    with open(filename, 'w') as f:
        f.write('\n'.join(output))

print(f"DONE")