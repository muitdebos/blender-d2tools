# d2gifcompile_py

Python script that takes renders from d2tools/blender-d2tools and compiles them into an animated .gif.

Features:
- No transparent pixels that should be black
- Converts everything to D2 units palette.
- Compiles into a single animated .gif

In Diablo 2, RGB(0, 0, 0) becomes transparent. To prevent this, this tool boosts the overall brightness slightly to ensure any pure blacks will become the closest thing to black in the D2 color palette that is not transparent, RGB(4, 4, 4). If you don't want this, run with `--noboost`.

![d2gifcompile.py example](https://github.com/iuitdebos/blender-d2tools/blob/main/images/d2gifcompile_verbose.png)

## How to use

1. You need to have [Python3 (site)](https://www.python.org/downloads/).
2. Additionally, install [Pillow (site)](https://pillow.readthedocs.io/en/stable/installation.html).
3. Download this folder (./d2gifcompile) and enter it with your terminal of choice.
4. Dump all your renders in the `./renders` folder
5. Run: `python3 ./d2gifcompile.py`
6. Output: `./<your-render>.gif`

![d2gifcompile.py options](https://github.com/iuitdebos/blender-d2tools/blob/main/images/d2gifcompile_options.png)