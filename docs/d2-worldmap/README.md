## Diablo 2 Worldmap

Diablo 2 has a worldmap where the levels are positioned in. This is act-based, so every act takes place on the same XY grid. The level has an 2D offset and a 2D size, which together create the area that level occupies.

How the game uses these position is perhaps somewhat unintuitive at first, because at some point it stops being a valid position and the game crashes. That can be a seemingly arbitrary point. Here I will describe how it works and why it works like this.

When positioning levels outside of the allocated range, the first thing that will cause crashes is the automap functionality. I haven't yet further explored how to extend the worldmap but I assume that would require significant further code editing. However since the automap creates the initial crash I'll explain how to avoid this.


### Playable area

To get right into it, the shape of the world map where levels can sit in is a pentagon. See the image below to get a quick view. The pentagon starts from 0,0 and extends to a maximum total sum of 8191, and where abs(x-y) < 4096 and (x+y) < 8191.

![World Map](https://github.com/iuitdebos/blender-d2tools/blob/main/docs/d2-worldmap/worldmap.png)

The reason is that the game maps a level's tiles' 2D position with some math onto a single integer (up to 0xFFFF or 8191). One could use the first two bytes as the X and the second to as Y, which would give you a square 0xFF / 4096 per axis. However, the Blizzard North developers were smart and could squeeze out those extra triangles you see in the image above past 4096.

Also note that Diablo 2 has quite some random map generation including connected outdoor areas. Any area below 1000 on either axis is reserved for these random maps.


### The math

(based on version 1.13c)

The game stores the location data of tiles, which make up the level, on an XY grid. They've allocated a WORD for this, so 0xFFFF. Below is the smart part where they subtract Y from X for the first two bytes, and add Y to X for the latter two. This gives the extra triangles on top of the otherwise square area.

```
1.13c: D2Common.dll+0x4DAC0
void (int *nX, int *nY) {
  nX = *pX;
  nY = *pY;
  *pX = (nX - nY) * 0x50;
  *pY = (nY + nX) * 0x50 >> 1;
  return;
}
```

This is called from D2Client, where it will get the world position for the automap. After getting the results, it will divide them by 10.

```
  D2Common.dll+0x4DAC0(&nX, &nY);
  nX = nX / 10;
  nY = nY / 10;
```

Since the math function multiplies the X and Y by 0x50 and the result gets divided by 0xA, you could imagine these to simply multiplying by 0x8 with the Y being bitshifted. Interestingly and most likely on purpose, "rooms" in Diablo are 8x8 tiles so it makes sense they use steps of 8.

After this calculation it does a couple of checks in the following form:

```
if ((nX < -0x8000) || (0x7fff < nX)) {
  ...
}
```

So it directly checks for either output nX or nY to be within that valid range. 0x8000 is 32768 which is much more than 4096, but don't forget that 0x8000 was the actual position multiplied by 8, so the actual usable area is only 0x1000, which _is_ 4096.

Neither nX nor nY after the math can exceed either of these, but because of this transformation in the first code section this boils down to the following usage.


### How to use

When talking about any values here I assume any valid point in the square that makes up the level (form offset to offset + size). Keep in mind that the levels are squares and the playable area has diagonals in it.

Without any issues it's possible to go to 4096x4096. From there it gets more tricky. If you want to go higher you have to decrease the other axis.

These are the rules that must be followed. Assuming X is the highest number (but works both ways, just swap X and Y if Y is the highest).

- x-y must be < 4096
- y-x must be > -4096
- x+y must be < 8191

With an example in code, X: 5000, y: 1000.

- 5000 - 1000 = 4000
- 1000 - 5000 = -4000
- 5000 + 1000 = 6000

However interestingly, 5000x500 is not valid as 5000 - 500 = 4500 which is too large on `x-y``. 1500x5000 would be valid however; 5000 - 1500 = 3500, 1500 - 5000 = -3500 and 5000 + 1500 = 6500.

The number combination with highest possible single value is 6143x2047. However that would mean the level would have to be 0 in size, so not very practical. More realistically however, something like 6000x2000 seems the useful upper limit for highest single value where a smallish level can fit.