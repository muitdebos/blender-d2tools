# d2gifcompile_py

Python script that takes renders from d2tools/blender-d2tools and compiles them into an animated .gif.

In Diablo 2, RGB(0, 0, 0) becomes transparent. To prevent this, this tool boosts the overall brightness slightly to ensure any pure blacks will become the closest thing to black in the D2 color palette that is not transparent, RGB(4, 4, 4).

## How to use

1. You need to have Python3.
2. Additionally, install Pillow
3. Download this folder (./d2gifcompile) and enter it with your terminal of choice.
4. Dump all your renders in a folder like `'./renders/'`
5. Run: `./d2gifcompile.py -i "./renders/*.png"`
6. Output: `./<your-render>.gif`
