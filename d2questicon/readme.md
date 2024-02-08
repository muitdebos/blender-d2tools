## D2 Quest Icon tools

This is a python script that handles quest icon frame generation. In Diablo 2, quest icons have a couple different states (inactive, active, pressed, complete), and an animation that goes from active to complete.

This script will, given a single quest icon image in the 'active' state, generate all the other required frames.

![d2questicon.py input example](https://github.com/muitdebos/blender-d2tools/blob/main/d2questicon/examples/input.png)
![d2questicon.py output example](https://github.com/muitdebos/blender-d2tools/blob/main/d2questicon/examples/output.gif)

### Usage

- You need to have Python3 (site) and use PIP or similar package manager.
- Additionally, install Pillow (site).
- Download this folder (./d2questicon) and enter it with your terminal of choice.
- Put your 'active' quest icon frame image in `./d2questicon/in/`, and name it `active.gif` or `0000.gif`
- Optionally, you can also add the 'completed' state frame and name it `completed.gif` or `0024.gif`. If not provided, it will be generated.
- Run: `python3 ./d2questicon.py`
- Output is in `./d2questicon/out/0000.png` through `./d2questicon/out/0026.png`.
- If you want an animated gif of the output in units palette, you can copy-paste these renders and use it with the [../d2gifcompile/](D2gifcompile) script.



### Options

```

-i / --input: Directory to search for input images. Defaults to './in/'
-o / --output: Directory to save output images. Defaults to './out/'
-p / --prefix: (Optional) Name prefix for images. Default is empty.
--ext: Input file extension. Defaults to "gif", can also be "png" for instance
```

Example: `python3 ./d2questicon.py -p a1q1 --ext png`

Takes input images: `./in/a1q1_active.png` and `./in/a1q1_active.png`, or alternatively `./in/a1q1/active.png` and `./in/a1q1/active.png`

And generates: `./out/a1q1_0000.png` through `./out/a1q1_0026.png`, or alternatively `./out/a1q1/0000.png` through `./out/a1q1/0026.png`,


### Extraction

Note: **This is not needed if you just want to generate your quest icon frames**. This is only in case you want more specific results, or a look into how I got the animation.

The script can also extract the animation from existing quest icons. That's how `./src/animation/` was created. For best results you need to play around with the script a bit.

Optionally you can have a `./in/diff/` directory with frames to compare to. If those are not defined, the script will take frame `0000` and `0024` as diff starters, but that won't be as accurate. For best results see the example below.

```
-c / --compile: [True|False] = If we should compile instead of extract. Defaults to 'True'. Set this to False to extract.
-t / --threshold: [int] = Luminosity threshold for extraction. 0 is very low threshold, 4 is high. Default is 2.
```

Example: `python3 ./d2questicon.py -p a1q1 -c False -t 1`

Takes input images: `./in/a1q1/0000.gif` through `./in/a1q1/0026.gif`

And generates `./out/a1q1/0000.png` through `./out/a1q1/0024.png`, as well as `./out/a1q1/diff/0000.png` through  `./out/a1q1/diff/0024.png`. Note that `0025` and `0026` are not generated, since they are not part of the animation.

#### Usage

Here are the steps I took to generate `./src/animation/`, using an example prefix `a1q6`:

1. Put your frames to extract from in `./in/a1q6/...`, such as `./in/a1q6/0000.gif` and onwards.
2. Run `python3 ./d2questicon.py -p a1q6 -c False -t 2`
3. Copy the generated `./out/a1q6/diff/` directory and put it in `./in/a1q6/` to make `./in/a1q6/diff/`
4. This will now use these generated images to separate out the animation
5. Run `python3 ./d2questicon.py -p a1q6 -c False -t 0` (more strict)
6. Now you can use `./out/a1q6/*.png` as final animation images.
7. I did some very minor manual clean-up to make the animation slightly more consistent.
8. If you want to use these for the compilation part of this script, copy them to `./src/animation/` and follow the existing name convention. Make sure this directory has (an empty) `0000.png`, `0025.png`, and `0026.png` as is currently the case. Then you can run the compile part of the script and it will use your newly extracted animation.
9. If you want to instead use the animation manually, use a `lighten` blend mode to blend it with base images.