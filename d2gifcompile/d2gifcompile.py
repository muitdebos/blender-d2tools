import os
import glob
import math
import argparse
from PIL import Image

########
# Defs #
########

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

# Load images into Pillow Image
def load_images(paths):
    images = []
    for path in paths:
        img = Image.open(path)
        images.append(img)
    
    return images

# Creates a palette img for use in Pillow
def load_palette(path: str):
    # Load palette data
    if (not os.path.isfile(path)):
        print(f"Could not locate pallete file from '{path}'")
        quit()

    pal_data = []
    with open(path, 'r') as file:
        pal_data = list(map(int, file.read().split('\n')))

    # Create a palette image to quantize to
    pal_img = Image.new('P', (1, 1), 0)
    pal_img.putpalette(pal_data + [0] * (768 - len(pal_data))) # Make sure pal_data is 768 entries long

    if (args.verbose):
        print(f"Palette file: '{path}'")

    return pal_img


# Places 'img_overlay' over 'img_src' with 'alpha' transparency
def fade_images(src_img, overlay_img, alpha):
    img = src_img.copy()
    # Create the mask image for this frame
    mask_img = Image.new('RGBA', src_img.size, (0, 0, 0, alpha))
    
    # Paste looped image on top of starting, using alpha
    img.paste(overlay_img, (0, 0), mask_img)

    return img


########
# Main #
########

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", dest = "input", help = "Glob string to search the files for. Defaults to './renders/*.png'")
parser.add_argument("-o", "--output", dest = "output", help = "Name of resulting animated .gif. Defaults to first image like so: @1TRLITNUHTH_0_0001.png becomes @1TRLITNUHTH.gif.")
parser.add_argument("--fade", dest = "fade", type = int, help="Amount of frames to fade in the loop. Reduces total frame count, but fades together this amount of frames to create a more seamless loop.")
parser.add_argument("-d", "--directions", dest = "directions", type = int, help="Amount of directions. Used for splitting the images into groups when looping.")
parser.add_argument("--verbose", dest = "verbose", action='store_true', help = "Verbose logging")
parser.add_argument("--boost", dest = "boost_brightness", action='store_true', help = "Boosts the brightness the tiniest amount to make full black not transparent in Diablo 2. Transparent base images are never boosted.")
parser.add_argument("--noboost", dest = "boost_brightness", action='store_false', help = "(Default)")
parser.set_defaults(input = "./renders/*.png")
parser.set_defaults(fade = 0)
parser.set_defaults(directions = 1)
parser.set_defaults(boost_brightness = False)
args = parser.parse_args()

can_boost_brightness = args.boost_brightness

image_paths = sorted(glob.glob(args.input))
rootname = args.output if args.output else os.path.basename(image_paths[0]).split('_')[0]

if (len(image_paths) <= 0):
    print("Error: Did not find any images. Please check your -input arg.\nNote that you may need to escape special characters (e.g. ./$1TRLITNUHTH_*.png should become ./\$1TRLITNUHTH_*.png).")
    quit()

# Separate by direction
if (args.directions <= 0):
    args.directions = 1
if (args.directions > len(image_paths)):
    print("Error: You are asking for more directions than there are images.")
    quit()

amount_per_dir = len(image_paths) // args.directions
imagepaths_by_dir = []
processed_images = [] # List of final images

# Separate by direction
loop_amount = args.fade
loop_max = math.floor(amount_per_dir / 2)
if (loop_amount > loop_max):
    loop_amount = loop_max
    print(f"Warning: Maximum amount of looping frames is half the total amount of frames. Clamped to {loop_max}")

if ((len(image_paths) / args.directions) % 1 != 0):
    print("Error: Directions do not have an equal amount of frames. All directions must have the same amount of frames.")
    quit()

if (args.verbose):
    print("| Settings |")
    print(f"Boost image brightness: {args.boost_brightness}")
    print(f"Fade-in loop frames: {loop_amount}")
    print(f"Directions: {args.directions}")
    print(f"Frames / direction: {amount_per_dir}")
    print(f"Total images found: {len(image_paths)}")

d2pal = load_palette('./units_pylist.txt')

## Per direction, loop images if necessary, then process them and add them to the global processed_images list
for d in range(args.directions):
    if (args.verbose):
        print(f"\n| Direction: {d} |")

    dir_imagepaths = image_paths[(d*amount_per_dir):((d+1)*amount_per_dir)]
    imagepaths_by_dir.append(dir_imagepaths)

    images_in_dir = load_images(dir_imagepaths)

    # Loop additional images, keeping in mind the directions
    if (loop_amount > 0 and len(images_in_dir) > loop_amount):
        loop_start = len(images_in_dir) - loop_amount
        for i in range(loop_amount):
            # Fade in frames 0, 1, 2 .. on top of last frames
            target_frame = loop_start + i
            loop_frame = i
            src_img = images_in_dir[target_frame]
            loop_img = images_in_dir[loop_frame]

            # We skip 0 and 255 alpha's
            alpha = round((i + 1) * 255 / (loop_amount + 1)) 
            res_img = fade_images(src_img, loop_img, alpha)
            res_img.filename = src_img.filename

            if (args.verbose):
                print(f"Fading {alpha}/255: ({src_img.filename}) into ({loop_img.filename})")

            # Overwrite first frames that have loop overlayed
            images_in_dir[loop_frame].close()
            images_in_dir[loop_frame] = res_img

    # Close and delete looped images
    for i in range(loop_amount):
        im = images_in_dir.pop()
        im.close()

    # Process images
    for img in images_in_dir:
        if (args.verbose):
            print(f"{img.filename}: [Processing] ...", end = " ")

        # Check to ensure we can and should boost blacks
        if (img.mode == "RGB" and can_boost_brightness):
            print(f"\nWarning: {img.filename} does not have an alpha channel. Cannot boost blacks.")
            can_boost_brightness = False
        
        # If we can, boost blacks to the darkest non-transparent black in d2 color palette
        if (can_boost_brightness):
            if (args.verbose):
                print(f"[Boosting brightness] ...", end = " ")
            img = boost_brightness(img)
        
        
        # Convert to RGB and apply D2 palette
        if (args.verbose):
            print(f"[Converting to D2 palette] ...", end = " ")
        img = img.convert("RGB")
        img = img.quantize(palette=d2pal)
        
        processed_images.append(img)

        if (args.verbose):
            print(f"[Done]")


# Done processing
if (args.verbose):
    print(f"\nAll images processed, saving as '{rootname}.gif'")

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

for image in processed_images:
    image.close()

if (args.verbose):
    print(f"DONE")
else:
    print(f"Saved as '{rootname}.gif'")
