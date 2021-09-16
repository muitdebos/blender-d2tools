import os
import glob
import argparse
from PIL import Image

# Initialize parser
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", dest = "input", help = "Glob string to search the files for. Defaults to './*.png'")
parser.set_defaults(input = "./renders/*.png")
parser.add_argument("-o", "--output", dest = "output", help = "Name of resulting animated .gif. Defaults to first image like so: @1TRLITNUHTH_0_0001.png becomes @1TRLITNUHTH.gif.")
parser.add_argument("-v", "--verbose", dest = "verbose", action='store_true', help = "Verbose logging")
parser.add_argument("--boost", dest = "boost_brightness", action='store_true', help = "Boosts the brightness the tiniest amount to make full black not transparent in Diablo 2. Transparent base images are never boosted. (Default)")
parser.add_argument("--noboost", dest = "boost_brightness", action='store_false')
parser.set_defaults(boost_brightness = True)
args = parser.parse_args()

can_boost_brightness = args.boost_brightness

if (args.verbose):
    print("Not boosting image brightness.")

## Brightness boost to ensure no content becomes transparent in D2
d2darkest = 4 # RGB: 4 / 256 is the darkest non-transparent black in d2 color palette
def boost_brightness(img: Image.Image):
    # Get a mask from alpha channel (anything with any transparency get's cut off)
    img_A = img.getchannel("A")
    mask = img_A.point(lambda i: i > 254 and 255)

    # Boost brightness fractionally to bump 0 to 4 (and 256 to 256)
    brighter = img.point(lambda i: round(((i + d2darkest) / (255 + d2darkest)) * 255))
    # Use the mask to only apply to the content
    img.paste(brighter, None, mask)
    
    return img


def load_palette(path: str):
    # Load palette data
    if (not os.path.isfile(path)):
        print(f"Could not locate pallete file from '{path}'")
        quit()

    paldata = []
    with open(path, 'r') as file:
        paldata = list(map(int, file.read().split('\n')))

    # Create a palette image to quantize to
    palimg = Image.new('P', (1, 1), 0)
    palimg.putpalette(paldata + [0] * (768 - len(paldata))) # Make sure paldata is 768 entries long

    if (args.verbose):
        print(f"Loaded palette from: '{path}'")

    return palimg


## main
images = sorted(glob.glob(args.input))
d2pal = load_palette('./units_pylist.txt')
rootname = args.output if args.output else os.path.basename(images[0]).split('_')[0]
processed_images = []

if (len(images) <= 0):
    print("Did not find any images. Please check your -input arg.\nNote that you may need to escape special characters (e.g. ./$1TRLITNUHTH_*.png should become ./\$1TRLITNUHTH_*.png).")
    quit()

for image in images:
    with open(image, 'rb') as file:
        # Load image with Pillow
        img = Image.open(file)

        # Check to ensure we can and should boost blacks
        if (img.mode == "RGB" and can_boost_brightness):
            print("Input files are without alpha channel. Cannot boost blacks.")
            can_boost_brightness = False
        
        # If we can, boost blacks to the darkest non-transparent black in d2 color palette
        if (can_boost_brightness):
            img = boost_brightness(img)
            if (args.verbose):
                print(f"Loading: '{image}' and boosting brightness")
        elif (args.verbose):
                print(f"Loading: '{image}'")
        
        # Convert to RGB and apply D2 palette
        img = img.convert("RGB")
        img = img.quantize(palette=d2pal)
        
        processed_images.append(img)

if (args.verbose):
    print(f"All images processed, saving as '{rootname}.gif'")

# Compile into a single animated gif
processed_images[0].save(rootname+'.gif',
    append_images = processed_images[1:],
    background = 0,
    transparency = 255,
    disposal = 2, # No need to dispose because every image has black background
    save_all = True, 
    optimize = False,
    palette = d2pal,
    loop = 0,
    duration = 0)


print(f"Saved: '{rootname}.gif'")
