import glob
import argparse
from PIL import Image

########
# Main #
########

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", dest = "input", help = "Name of input file. Defaults to './palette.txt'")
parser.add_argument("-o", "--output", dest = "output", help = "Name of output text file. Defaults to './palette.png'")
parser.add_argument("--verbose", dest = "verbose", action='store_true', help = "Verbose logging")
parser.set_defaults(input = "./palette.txt")
parser.set_defaults(output = "palette")
args = parser.parse_args()

input_paths = glob.glob(args.input)
if (len(input_paths) <= 0):
    print("Error: Did not find any input. Please check your --input arg.")
    quit()

colors = []
with open(input_paths[0]) as f:
    colors = f.readlines()

img = Image.new("RGB", (16,16))
imgdata = []

count = 0
for c in colors:
    cvalues = c.split()
    count += 1
    if (args.verbose):
        print(f"line {count}: {cvalues[0]}, {cvalues[1]}, {cvalues[2]}")

    imgdata.append((int(cvalues[0]), int(cvalues[1]), int(cvalues[2])))
    img.putdata(imgdata)

img.save(args.output + ".png")

print(f"DONE")