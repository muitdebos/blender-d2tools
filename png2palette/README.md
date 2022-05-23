# png2palette

These are two very simple scripts to convert between a text-based color palette to a 16x16 png image and vice-versa.

As an example, GIMP saves palette files like so:
```
...metadata...
  0  0  0
 23  0 46
etc
```

If we remove the metadata and keep just the color lines, we can feed it through palette2png.py and get an image output. We can then easily edit this image directly in preferred image editor.

When we have an image we're satisfied with we can run it through png2palette.py to get back a GIMP palette file.

In turn this can be used to generate a PL2 file using [gravestench/pl2](https://github.com/gravestench/pl2)

## Usage

For both scripts, see "example_palette" file types for the input and output data structure.

PNG to Palette (txt)
`python3 ./png2palette.py -i ./palette.png`

Palette (txt) to PNG
`python3 ./palette2png.tx -i ./palette.txt`

Optional parameters (on both):
`-o "newname"` to change the name of the output file.
`--verbose` to list per line or color what is parsed