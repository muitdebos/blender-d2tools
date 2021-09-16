# blender-d2tools

Blender plugin for Diablo 2 modelling and rendering

In the future I might add some examples. But for now, see [docs/blender-to-d2-process.md](https://github.com/iuitdebos/blender-d2tools/blob/main/docs/blender-to-d2-process.md) for documentation on how to take your renders into Diablo 2.

## Table of Contents
- [blender-d2tools](#blender-d2tools)
  - [Table of Contents](#table-of-contents)
  - [How to install](#how-to-install)
  - [How to use](#how-to-use)
  - [Importing renders into the game](#importing-renders-into-the-game)

![D2Tools Panel preview](https://github.com/iuitdebos/blender-d2tools/blob/main/images/d2tools_panel.png)


## How to install

1. Download the d2tools.py script and put it in your .blend file directory.
2. Open Blender (2.93.1+, probably 2.8+ but haven't checked).
3. Go to the "Scripts" window, and open the d2tools.py file there.
4. If you want it to always run when you open this .blend file (recommended),  in the Script editor navigation bar go to Text > Register and check it.
5. To run the script, press the Play button.
6. In any View3D panel, press N to open up the tools panel. There should now be a new tab "Diablo 2".


## How to use

1. Go to the Diablo 2 tab in View3D tools panel.
2. Choose if you want a World setup or Item setup. World is anything isometric-- monsters, characters, environments. Items are anything face-on, primarily inventory graphics.
3. If this is the first time, check out the Generate tab. Most likely you want all selected and hit "Generate".

  - `Rotatebox` is an empty object created at the Scene root. It will contain the camera and lighting. For "World", these settings are based off semi-official settings used by Blizzard. "Item" inventory graphics don't have standardized render settings.

  - `Scale example` generates a very blocky example of approximately the size of a human, once rendered, in the game, or for the "Item" template it generates a 2x4 inventory tile size collection of cubes.  
![Scale example](https://github.com/iuitdebos/blender-d2tools/blob/main/images/size_example.png)

  - `Scene setup` prepares your .blend file by changing the settings a bit.

4. Whenever you want to render out the frames, go to the Render Properties tab. I highly suggest filling in the animation frame naming convention Blizzard used, e.g. CRTRLITNUHTH for Corrupt Rogue idle animation.
5. Choose the settings you want, then head to the Render tab.
6. If you are rendering an opaque graphic, I recommend checking "Transparent". If you want a glowy overlay like an aura or certain monster glow effects, uncheck "Transparent" as the game uses blend modes to do the effects.
7. Once you're satisfied, SAVE FIRST, then hit "Render Directions". There is no UI feedback, but Blender is now rendering out all the frames according to the Render Properties.
8. Blender has a tendency to crash. If it crashed somewhere halfway, you can use the "Skip Directions" to jump ahead to where it crashed.


## Importing renders into the game

I've made a separate documentation for the entire process. See [/docs/blender-to-d2-process.md](https://github.com/iuitdebos/blender-d2tools/blob/main/docs/blender-to-d2-process.md). This has an almost step-by-step plan to follow in order to get the renders into the game.
