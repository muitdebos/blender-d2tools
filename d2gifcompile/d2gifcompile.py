import os
import glob
import math
import argparse
import numpy as np
from PIL import Image, ImageOps, GifImagePlugin

# Override this function to prevent deduplication of consecutive frames that are exactly the same
# More info: https://github.com/python-pillow/Pillow/issues/8397
def _getbbox(base_im, im_frame):
    return None, (0, 0) + im_frame.size
GifImagePlugin._getbbox = _getbbox

########
# Defs #
########

## Brightness boost to ensure no content becomes transparent in D2
d2darkest = 5 # RGB: 4 / 256 is the darkest non-transparent black in d2 color palette
def boost_brightness(img: Image.Image):
    # Get a mask from alpha channel (anything with any transparency get's cut off)
    has_A = "A" in img.getbands()
    if (has_A):
        img_A = img.getchannel("A")
        mask = img_A.point(lambda i: i > 127 and 255)

    # Boost brightness fractionally to bump 0 to 4 (and 256 to 256)
    brighter = img.point(lambda i: round(((i + d2darkest) / (255 + d2darkest)) * 255))
    black = img.point(lambda i: 0)

    # Use the mask to only apply to the content
    if (has_A):
        black.paste(brighter, None, mask)
    
    return black

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
        print(f"Could not locate palette file from '{path}'")
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
def fade_images(src_img: Image.Image, overlay_img: Image.Image, mask_color):
    img = src_img.copy()

    # Create the mask image for this frame
    mask_img = Image.new('RGBA', src_img.size, mask_color)
    
    # Paste looped image on top of starting, using alpha
    img.paste(overlay_img, (0, 0), mask_img)

    return img

# Checks if an image has transparency  https://stackoverflow.com/a/58567453
def has_transparency(img):
    if img.info.get("transparency", None) is not None:
        return True
    if img.mode == "P":
        transparent = img.info.get("transparency", -1)
        for _, index in img.getcolors():
            if index == transparent:
                return True
    elif img.mode == "RGBA":
        extrema = img.getextrema()
        if extrema[3][0] < 255:
            return True

    return False
########
# Main #
########

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", dest = "input", help = "Glob string to search the files for. Defaults to './renders/*.png'")
parser.add_argument("-o", "--output", dest = "output", help = "Name of resulting animated .gif. Defaults to first image like so: @1TRLITNUHTH_0_0001.png becomes @1TRLITNUHTH.gif.")
parser.add_argument("-s", "--scale", dest = "scale", type = float, help = "Scale images by amount (default 1)")
parser.add_argument("-p", "--palette", dest = "palette", help = "Palette file to use. Default is './units_pylist.txt'. Needs to be a txt file where every line is one color value (e.g. RR\\nGG\\nBB\\nRR\\nGG\\BB\\..etc)")
parser.add_argument("--fade", dest = "fade", type = int, help="Amount of frames to fade in the loop. Reduces total frame count, but fades together this amount of frames to create a more seamless loop.")
parser.add_argument("-d", "--directions", dest = "directions", type = int, help="Amount of directions. Used for splitting the images into groups when looping.")
parser.add_argument("--verbose", dest = "verbose", action='store_true', help = "Verbose logging")
parser.add_argument("--boost", dest = "boost_brightness", action='store_true', help = "Boosts the brightness the tiniest amount to make full black not transparent in Diablo 2.")
parser.add_argument("--noboost", dest = "boost_brightness", action='store_false', help = "(Default if no alpha channel is found)")
parser.add_argument("--mask", dest = "mask", action='store_true', help = "If set, uses a grayscale version of the frame as alpha channel. (default False)")
parser.add_argument("--inverted-mask", dest = "inverted_mask", action='store_true', help = "Uses white as background for masking. (default False)")
parser.add_argument("--invert", dest = "invert", action='store_true', help = "Inverts the colors (before any other HSL operation). (default False)")
parser.add_argument("--hue", dest = "hsl_hue", type = int, help = "Amount to shift the hue by, from 0 to 255.")
parser.add_argument("--saturation", dest = "hsl_saturation", type = float, help = "Amount to multiply saturation by. 0 to 4")
parser.add_argument("--value", dest = "hsl_value", type = int, help = "Amount to add to brightness value. -255 to 255")
parser.add_argument("--contrast", dest = "hsl_contrast", type = float, help = "Amount to multiply brightness value by. 0 to 4")
parser.add_argument("-sf", "--save-frames", dest = "saveframes", action='store_true', help = "Save individual frames in .gif format as well.")
parser.set_defaults(input = "./renders/*.png")
parser.set_defaults(palette = "./units_pylist.txt")
parser.set_defaults(fade = 0)
parser.set_defaults(scale = 1)
parser.set_defaults(directions = 1)
parser.set_defaults(boost_brightness = False)
parser.set_defaults(saveframes = False)
parser.set_defaults(inverted_mask = False)
parser.set_defaults(mask = False)
parser.set_defaults(invert = False)
parser.set_defaults(hsl_hue = 0)
parser.set_defaults(hsl_saturation = 1)
parser.set_defaults(hsl_value = 0)
parser.set_defaults(hsl_contrast = 1)
args = parser.parse_args()

hsl_hue = args.hsl_hue
hsl_saturation = max(min(args.hsl_saturation, 4), 0)
hsl_value = max(min(args.hsl_value, 255), -255)
hsl_contrast = max(min(args.hsl_contrast, 4), 0)

can_boost_brightness = args.boost_brightness

image_paths = sorted(glob.glob(args.input))
if (len(image_paths) <= 0):
    print("Error: Did not find any images. Please check your --input arg. By default, it's \"./renders/*.png\".\nNote that you may need to escape special characters (e.g. ./$1TRLITNUHTH_*.png should become ./\$1TRLITNUHTH_*.png).")
    quit()


rootname = args.output
if (args.output == None):
    split_path = os.path.basename(image_paths[0]).split('_')
    if (len(split_path) > 0):
        rootname = split_path[0]
        rootsplit = rootname.split('.')
        if (len(rootsplit) > 1):
            rootname = rootsplit[0]
    else:
        rootname = "results"

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
    print(f"Mask using lightness: {args.mask}")
    print(f"...using white background instead: {args.inverted_mask}")
    print(f"Total images found: {len(image_paths)}")
    print(f"Save individual converted frames: {args.saveframes}")

d2pal = load_palette(args.palette)

total_frames = 0

frames_directory = rootname+'_frames'
if (args.saveframes):
    if not os.path.exists(frames_directory):
        os.mkdir(frames_directory)

## Per direction, loop images if necessary, then process them and add them to the global processed_images list
for d in range(args.directions):
    if (args.verbose):
        print(f"\n| Direction: {d} |")

    dir_imagepaths = image_paths[(d*amount_per_dir):((d+1)*amount_per_dir)]
    imagepaths_by_dir.append(dir_imagepaths)

    images_in_dir = load_images(dir_imagepaths)

    # Apply self-mask
    if (args.mask):
        print("Masking out the images using lightness as masking value")
        base_hue = hsl_hue

        img: Image.Image
        for index, img in enumerate(images_in_dir):
            img_rgb = img.convert('RGB')
            img_mask = img.convert('L')

            # Use white as transparent instead
            if (args.inverted_mask):
                img_rgb = ImageOps.invert(img_rgb)
                # By default, change hue back to original hue before inversion
                hsl_hue = base_hue + 127

            # Re-apply greyscale alpha mask
            img_rgba = img_rgb.convert('RGBA')
            img_rgba.putalpha(img_mask)

            img_rgba.filename = img.filename
            images_in_dir[index] = img_rgba

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
            mask_color = (0, 0, 0, alpha)

            res_img = fade_images(src_img, loop_img, mask_color)
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
    img: Image.Image
    for img in images_in_dir:
        fullpath = img.filename
        filetext = fullpath.split('/')[-1].split('.')
        filename = filetext[0]
        fileext = filetext[-1]

        if (args.verbose):
            print(f"{filename}.{fileext}: [Processing] ...", end = " ")
        else:
            print(f"{filename}.{fileext}")

        if (img.mode == "P"):
            if (has_transparency(img)):
                img = img.convert("RGBA")
            else:
                img = img.convert("RGB")

        # Check to ensure we can and should boost blacks
        if (img.mode == "RGB" and can_boost_brightness):
            print(f"\nWarning: {fullpath} does not have an alpha channel. Boosting blacks might not work as expected.")
        
        # If we can, boost blacks to the darkest non-transparent black in d2 color palette
        if (can_boost_brightness):
            if (args.verbose):
                print(f"[Boosting brightness] ...", end = " ")
            img = boost_brightness(img)
        
        # If we want a white background, paste image on top of white
        if (args.inverted_mask or args.invert):
            if (args.verbose):
                print(f"[Applying inversion] ...", end = " ")
            white_img = Image.new('RGBA', img.size, (255, 255, 255, 1))
            img_A = img.getchannel("A")

            if (args.invert):
                img_inverted = ImageOps.invert(img.convert("RGB"))
                white_img.paste(img_inverted, (0, 0), img)
            else:
                white_img.paste(img, (0, 0), img)
            
            mask = img_A.point(lambda i: i < 2 and 255)
            white_img.paste((0, 0, 0, 1), (0, 0), mask)
            img = white_img

        # Apply hue / saturation changes (don't do masked, that happened earlier in the masking step)
        if (hsl_hue != 0 or hsl_saturation != 1 or hsl_value != 0 or hsl_contrast != 1):
            if (args.verbose):
                print(f"[Applying HSL changes] ...", end = " ")
            img = img.convert("HSV")
            img_split = img.split()
            if (hsl_hue != 0):
                new_hues = img_split[0].point(lambda i: (i + hsl_hue) % 255)
                img_split[0].paste(new_hues)
            if (hsl_saturation != 1):
                new_sats = img_split[1].point(lambda i: i * hsl_saturation)
                img_split[1].paste(new_sats)
            if (hsl_value != 0 or hsl_contrast != 1):
                new_sats = img_split[2].point(lambda i: ((i + hsl_value) * hsl_contrast))
                img_split[2].paste(new_sats)
            img = Image.merge(img.mode, img_split)

        if (args.scale != 1):
            if (args.verbose):
                print(f"[Applying scaling] ...", end = " ")
            width, height = img.size
            width = int(width * args.scale)
            height = int(height * args.scale)
            img = img.resize((width, height), Image.Resampling.NEAREST)
            
        # Convert to RGB and apply D2 palette
        if (args.verbose):
            print(f"[Converting to D2 palette] ...", end = " ")
        img = img.convert("RGB")
        img = img.quantize(palette=d2pal,dither=Image.NONE)

        if (args.saveframes):
            img.save(f"{frames_directory}/{rootname}_{filename}.gif",
                background = 0,
                transparency = 255,
                disposal = 2, # No need to dispose because every image has black background
                save_all = True, 
                optimize = False,
                palette = d2pal,
                loop = 0,
                duration = 0)

        processed_images.append(img)
        total_frames += 1

        if (args.verbose):
            print(f"[Done]")


# Done processing
if (args.verbose):
    print(f"\nAll images processed, saving as '{rootname}.gif'. Frames: {total_frames}")

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
    print(f"Saved as '{rootname}.gif'. Frames: {total_frames}")
