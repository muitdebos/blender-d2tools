# blender-d2tools

Tools to assist the render pipeline from Blender to Diablo 2. At the moment this is mostly the one script, d2tools.py. The script is human-readable so any concerns, questions or specific info is there to see.

In the future I might add some examples.


## How to install

1. Download the d2tools.py script and put it in your .blend file directory.
2. Open Blender (2.93.1+, probably 2.8+ but haven't checked).
3. Go to the "Scripts" window, and open the d2tools.py file there.
4. If you want it to always run when you open this .blend file (recommended),  in the Script editor navigation bar go to Text > Register and check it.
5. To run the script, press the Play button.
6. In any View3D panel, press N to open up the tools panel. There should now be a new tab "Diablo 2".


## How to use

1. Go to the Diablo 2 tab in View3D tools panel.
2. If this is the first time, check out the Generate tab. Most likely you want all selected and hit "Generate".
  - `Rotatebox` is an empty object created at the Scene root. It will contain the camera and lighting. These settings are based off semi-official settings used by Blizzard.
  - `Scale example` generates a very blocky example of approximately the size of a human, once rendered, in the game.
  - `Scene setup` prepares your .blend file by changing the settings a bit.
3. Whenever you want to render out the frames, go to the Render Properties tab. I highly suggest filling in the animation frame naming convention Blizzard used, e.g. CRTRLITNUHTH for Corrupt Rogue idle animation.
4. Choose the settings you want, then head to the Render tab.
5. If you are rendering an opaque graphic, I recommend checking "Transparent". If you want a glowy overlay like an aura or certain monster glow effects, uncheck "Transparent" as the game uses blend modes to do the effects.
6. Once you're satisfied, SAVE FIRST, then hit "Render Directions". There is no UI feedback, but Blender is now rendering out all the frames according to the Render Properties.
7. Blender has a tendency to crash. If it crashed somewhere halfway, you can use the "Skip Directions" to jump ahead to where it crashed.


## Importing renders into the game

This is quite a large topic that I will get back to, but for now you can check out [https://d2mods.info/resources/infinitum/tut_files/dcc_tutorial/](Animation Conversion Tutorial) by Joel Falcou, Alkalund and Nefarius. Or you can check out the Phrozen Keep forums or discord for more info.