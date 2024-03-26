import os
import argparse
from PIL import Image, ImageChops, ImageEnhance, ImageFilter
import numpy as np

########
# Main #
########

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--compile", dest = "compile", help = "If we should compile instead of extract. Defaults to 'True'")
parser.add_argument("-i", "--input", dest = "input", help = "Directory to search for frames. Defaults to './in/'")
parser.add_argument("-o", "--output", dest = "output", help = "Directory to save the frames in. Defaults to './out/'")
parser.add_argument("-p", "--prefix", dest = "prefix", help = "(Optional) prefix for filenames. Defaults to ''.")
parser.add_argument("-t", "--threshold", dest = "threshold", help = "Luminosity threshold for extraction. 0 is very low threshold, 4 is high. Default is 2")
parser.add_argument("--ext", dest = "extension", help = "Input file extension. Defaults to 'gif'")
parser.add_argument("-a", "--animation", dest = "animation", help = "(Optional) Animation directory. Defaults to './src/animation/'")
parser.set_defaults(compile = "True")
parser.set_defaults(input = "./in/")
parser.set_defaults(output = "./out/")
parser.set_defaults(threshold = "2")
parser.set_defaults(extension = "gif")
parser.set_defaults(animation = "./src/animation/")
args = parser.parse_args()

# Get and check paths
if not os.path.exists(args.input):
    print(f"Error: Invalid --input argument. Input directory not found: '{args.input}'")
    quit()
if not os.path.exists(args.output):
    print(f"Error: Invalid --output argument. Output directory not found: '{args.output}'")
    quit()

print(f"Animation: {args.animation}")
animationDirectory = "./src/animation/"
if (args.animation != None):
    animationDirectory = f"{args.animation}"

if os.path.exists(f"{animationDirectory}0000.png"):
    print(f"Animations from '{animationDirectory}'")
elif (args.compile == "True"):
    print(f"Can't find valid animations: '{animationDirectory}0000.png'")
    quit()

prefixDirectory = ""
prefixDiffDirectory = ""
if (args.prefix != None):
    prefixDirectory = f"{args.prefix}/"
    prefixDiffDirectory = f"{args.prefix}/diff/"

    # If prefix is set, make a directory in the output
    directory = f"{args.output}{args.prefix}"
    if not os.path.exists(directory):
        os.mkdir(directory)
        print(f"Created directory '{prefixDirectory}'")
    else:
        print(f"Using directory '{prefixDirectory}'")

    # If compiling, make a /diff directory in the output as well
    if not os.path.exists(f"{directory}/diff"):
        os.mkdir(f"{directory}/diff")
        print(f"Created directory '{prefixDiffDirectory}'")
    else:
        print(f"Using /diff directory '{prefixDiffDirectory}'")

    # Check if input dir exists
    if not os.path.exists(f"{args.input}{args.prefix}"):
        print(f"Error: Can't find prefixed input directory '{args.input}{prefixDirectory}'")
        quit()
else:
    # If compiling, make a /diff directory in the output as well
    if not os.path.exists(f"{args.output}/diff"):
        os.mkdir(f"{args.output}/diff")
        print(f"Created directory '{args.output}/diff'")

compileActiveName = "0000"
compileCompleteName = "0024"

prefixDashed = ""
if (args.prefix != None):
    if os.path.exists(f"{args.input}{prefixDirectory}{args.prefix}_0000.{args.extension}"):
        prefixDashed = f"{args.prefix}_"
    elif os.path.exists(f"{args.input}{prefixDirectory}{args.prefix}_active.{args.extension}"):
        prefixDashed = f"{args.prefix}_"
        compileActiveName = "active"
        compileCompleteName = "complete"
    elif os.path.exists(f"{args.input}{prefixDirectory}active.{args.extension}"):
        compileActiveName = "active"
        compileCompleteName = "complete"
elif os.path.exists(f"{args.input}active.{args.extension}"):
    compileActiveName = "active"
    compileCompleteName = "complete"


# Preparation
imgFrame = Image.open("./src/frame_empty.png").convert("RGBA")
imgFrameInactive = Image.open("./src/frame_inactive.png").convert("RGBA")
out = Image.new("RGBA", imgFrame.size, (0, 0, 0, 1))
blk = Image.new("RGBA", imgFrame.size, (0, 0, 0, 1))

def do_extract():
    # Quest icon
    imgActive = Image.open(f"{args.input}{prefixDirectory}{prefixDashed}0000.{args.extension}").convert("RGBA")
    imgComplete = Image.open(f"{args.input}{prefixDirectory}{prefixDashed}0024.{args.extension}").convert("RGBA")
    imgInactive = Image.open(f"{args.input}{prefixDirectory}{prefixDashed}0026.{args.extension}").convert("RGBA")

    # Generate "Inactive" state 1px higher for differencing
    imgInactiveCorrected = Image.new("RGBA", imgFrame.size, (0, 0, 0))
    imgInactiveCorrected.paste(imgInactive, [0, -1])
    imgInactiveCorrected.paste(imgFrame, [0, 0], imgFrame)

    # To extract a specific color, change this
    # nR = oR + oG + oB + oExtra
    # nG = oR + oG + oB + oExtra
    # nB = oR + oG + oB + oExtra
    MaskColorScale = ( 1,  0,  0,  0, 
                    1,  0,  0,  0, 
                    1,  0,  0,  0) 

    # Threshold levels
    thresholdLevels = [
        # 1-2   3-4  5-12 13-16 17-25
        [ 20,   12,   25,   20,   25], # 0
        [ 30,   40,   35,   40,   30], # 1
        [ 45,   60,   50,   55,   40], # 2
        [ 55,   70,   60,   65,   50], # 3
        [ 65,   80,   70,   75,   60], # 4
    ]
    thresholdLevel = int(args.threshold)

    # Extraction script
    def extract_frame(index: int, fromImage: Image.Image, threshold: int):
        # Open frame
        imgIndex = Image.open(f"{args.input}{prefixDirectory}{prefixDashed}{index:04}.{args.extension}").convert("RGBA")
        print(f'Extract image: {index:04}')

        # If we have a /diff directory in input, use that frame instead for diffing.
        if (os.path.exists(f"{args.input}{prefixDiffDirectory}{prefixDashed}0000.{args.extension}")):
            imgDiffIndex = Image.open(f"{args.input}{prefixDiffDirectory}{prefixDashed}{index:04}.{args.extension}").convert("RGBA")
            print(f'...using /diff/ image')
            imgInactiveCorrected.paste(imgDiffIndex, None, imgDiffIndex)
            imgDiffIndex.close()
        # /diff output from compilation results in .png's by default. Check this regardless of extension input
        elif (os.path.exists(f"{args.input}{prefixDiffDirectory}{prefixDashed}0000.png")):
            imgDiffIndex = Image.open(f"{args.input}{prefixDiffDirectory}{prefixDashed}{index:04}.png").convert("RGBA")
            print(f'...using /diff/ image')
            imgInactiveCorrected.paste(imgDiffIndex, None, imgDiffIndex)
            imgDiffIndex.close()

        # Clean output
        out.paste(blk)

        # Store difference
        bufferActive = np.asarray(fromImage.convert("RGB")).astype(np.int32)
        bufferFrame = np.asarray(imgIndex.convert("RGB")).astype(np.int32)
        bufferSub = np.abs(bufferFrame - bufferActive)
        imgDiff = Image.fromarray(np.uint8(bufferSub))
        imgDiff.save(f"{args.output}{prefixDiffDirectory}{prefixDashed}{index:04}.png")

        # Select brightness > 70
        mask = imgDiff.point(lambda i: i > threshold and 255)
        mask = mask.filter(ImageFilter.GaussianBlur(1))
        mask = mask.convert("L", MaskColorScale)

        # Save output
        out.paste(imgIndex, None, mask)
        out.save(f"{args.output}{prefixDirectory}{prefixDashed}{index:04}.png")

        imgIndex.close()

    # Loop through frames and get differences
    for fi in range(0, 3):
        extract_frame(fi, imgActive, thresholdLevels[thresholdLevel][0])

    for fi in range(3, 9):
        extract_frame(fi, imgInactiveCorrected, thresholdLevels[thresholdLevel][1])

    for fi in range(9, 13):
        extract_frame(fi, imgInactiveCorrected, thresholdLevels[thresholdLevel][2])

    for fi in range(13, 17):
        extract_frame(fi, imgComplete, thresholdLevels[thresholdLevel][3])

    for fi in range(17, 25):
        extract_frame(fi, imgComplete, thresholdLevels[thresholdLevel][4])

    imgActive.close()
    imgComplete.close()
    imgInactive.close()
    imgInactiveCorrected.close()

    print('Extraction complete')
    # do_extract end

def do_compile():
    # Load initial image
    imgActive = Image.open(f"{args.input}{prefixDirectory}{prefixDashed}{compileActiveName}.{args.extension}").convert("RGBA")

    # Load 'complete' frame, if it exists. Otherwise, generate it from the initial image
    imgComplete = None
    if os.path.exists(f"{args.input}{prefixDirectory}{prefixDashed}{compileCompleteName}.{args.extension}"):
        imgComplete = Image.open(f"{args.input}{prefixDirectory}{prefixDashed}{compileCompleteName}.{args.extension}").convert("RGBA")
    else:
        imgComplete = ImageEnhance.Color(imgActive).enhance(0)
        imgComplete = ImageEnhance.Contrast(imgComplete).enhance(0.9)
        imgComplete = ImageEnhance.Brightness(imgComplete).enhance(1.6)
        imgComplete.paste(imgFrame, None, imgFrame)

    # Darkens or overexposes the images in certain frames
    # Frame num:      0    1    2    3    4    5    6    7    8    9    10   11   12   13   14   15   16   17   18   19   20   21    22   23    24   25   26
    contrastLevels = [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.4, 0.6, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.15, 1.1, 1.05, 1.0, 1.0, 1.2]
    brightnsLevels = [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.4, 0.6, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.15, 1.1, 1.05, 1.0, 1.0, 1.1]

    def compile_frame(index: int, fromImage: Image.Image, contrast: int, brightness: int):
        # Open animation frame
        imgAnim = Image.open(f"{args.animation}{index:04}.png").convert("RGBA")
        print(f'Image: {index:04}')

        # Clean output
        out.paste(blk)
        out.paste(fromImage)

        # Contrast
        outC = ImageEnhance.Contrast(out).enhance(contrast)
        outC = ImageEnhance.Brightness(outC).enhance(brightness)

        # Save output
        outC.paste(imgFrame, None, imgFrame)
        outC.save(f"{args.output}{prefixDiffDirectory}{prefixDashed}{index:04}.png")

        # Clone and sharpen anim frame
        out.paste(blk)
        out.paste(imgAnim, None, imgAnim)
        imgAnimSharpen = ImageEnhance.Sharpness(out).enhance(1.3)

        # Save output
        outC = ImageChops.lighter(outC, imgAnimSharpen)
        outC.save(f"{args.output}{prefixDirectory}{prefixDashed}{index:04}.png")

        imgAnim.close()
        imgAnimSharpen.close()
        outC.close()

    # Darken and overlay animation
    for fi in range(0, 12):
        compile_frame(fi, imgActive, contrastLevels[fi], brightnsLevels[fi])

    for fi in range(12, 25):
        compile_frame(fi, imgComplete, contrastLevels[fi], brightnsLevels[fi])

    # Finally, add frame 25 (active, pressed down)
    out.paste(blk)
    out.paste(imgActive, [-1, 1])
    out.paste(imgFrame, None, imgFrame)
    out.save(f"{args.output}{prefixDirectory}{prefixDashed}0025.png")

    # ... and 26 (inactive)
    out.paste(blk)
    out.paste(imgActive, [0, 1])
    outC = ImageEnhance.Color(out).enhance(0)
    outC = ImageEnhance.Contrast(outC).enhance(contrastLevels[26])
    outC = ImageEnhance.Brightness(outC).enhance(brightnsLevels[26])
    outC.paste(imgFrameInactive, None, imgFrameInactive)
    outC.save(f"{args.output}{prefixDirectory}{prefixDashed}0026.png")

    imgActive.close()
    imgComplete.close()
    outC.close()

    print('Compilation complete')
    # do_compile end


if (args.compile == "True"):
    do_compile()
else:
    do_extract()

imgFrameInactive.close()
imgFrame.close()
out.close()
blk.close()

quit()
