# Blender to D2 Isometric

Some documentation on the process of getting things from Blender into Diablo 2. Many thanks to the old Blizzard North and the Phrozen Keep community for the help.

Special thanks to
- Phil Shenk (ex-Blizzard North Lead Character Artist) for sharing info on the rendering process for D2
- Paul Siramy for his many tools and wisdom
- Billian Belchev for the Cv5 .dcc plugin
- afj666 for the AFJ sheet edit
- Jetaman and Hz for Coffee COF Editor
- Joel Falcou, Alkalund and Nefarius for the highly recommended [Animation Conversion Extended Tutorial](https://d2mods.info/resources/infinitum/tut_files/dcc_tutorial/index.html)
-  reiyo_oki
- Sloan Roy and Necrolis for Dr. Tester
- Ladislav Zezula for Ladik's MPQ Editor


## Chapters 0: Set-up

### Required tools
- Blender (/ similar)
- AFJ Sheet Edit (/ similar .txt file editor)
- Graphics editor capable of handling indexed color maps and compiling animated gifs (I use Photoshop CS 6)
- AnimData Edit
- CofEditor
- Cv5.2
- MPQEditor
- Units.act (palette file)

### Concepts helpful to understand
- 3D section
  - Modelling (or sculpting + retopology)
  - Rigging
  - UV mapping
  - Texturing
  - Animating
- Color palettes and graphics editing
  - What is a color palette
  - Graphics file types
  - Retouching if desired
- D2 basic rendering
  - Tile-based (floors + walls)
  - Layered graphics (separate body parts and effects)
  - .COF / .DCC Files, how they work conceptually
- D2 text editing
  - -direct -txt files
  - AnimData.d2

### Guides / Tutorials / Further reading
- 3D tutorials
  - [Modelling (Beginners)](https://www.youtube.com/watch?v=9xAumJRKV6A)
  - [Rigging](https://www.youtube.com/watch?v=1yHF1PcreIY)
  - [UV Unwrapping](https://www.youtube.com/watch?v=ZyRtd8iYBOg)
- Diablo 2
  - !Highly recommended! [Animation Conversion Extended Tutorial](https://d2mods.info/resources/infinitum/tut_files/dcc_tutorial/index.html)
  - [New token from existing DCC animations](https://d2mods.info/resources/infinitum/tut_files/token-tutorial.html)
  - [Creating new tokens for animations](https://d2mods.info/forum/kb/viewarticle?a=168)


## Chapter 1: 3D Section

3D is a very large topic, an entire industry even, so I will only go through the concepts. It all depends on how deep you want to go down the rabbit hole, but feel free to look up tutorials for any parts you don't quite understand. It's too much to cover everything here.

We'll be going through the steps for a neutral animation (NU) of a monster.

Inventory graphics have slightly more customized setups, but going through this document will give a good idea of the process. Important note, is that a lot of D2's inventory graphics are actually painted, not 3d-rendered.

Note, Blender is known to crash every now and then, please save frequently.

### Scene Setup

First we need to make sure our scene is set up properly. For this I created a [Blender python script](https://github.com/iuitdebos/blender-d2tools) that automates all of this. But for reference, here are the steps.
- Clear the scene of anything currently there
- Create an empty object called RotateBox
- Create a Sun (/ directional) light.
  - Position: (8.05, -11.788, 24)
  - Rotation: (0, 30.7, -55.7)
  - Light settings: Default (1 Strength, full white light)
- Create a Camera
  - Position: (0, -30, 20)
  - Rotation: (60, 0, 0)
  - Set to "Ortographic" projection, ortho scale of 7.0
- Parent both Sun and Camera to RotateBox so that if you rotate the box by 45 degrees in Z axis, you get Diablo 2's "0" direction (facing bottom left).
- Any art you want to render should be unparented and face the Y direction.
- Render Properties
  - I prefer using Cycles render engine
  - Film > Pixel Filter, select "Gaussian" and set Width to 0.02 px. This removes anti-aliasing (which we want, as D2 doesn't support half-transparent pixels)
  - Film > Transparent (if you want monsters. If you want glowy effects, make sure it's NOT transparent)
- Output Properties
  - Resolution of maximally 256 x 256 (for dcc files). If you want something bigger, you need to layer them into different body parts.
  - Frame rate of 25 (helps preview, no effect on end-result since we're exporting an image sequence)
- World Properties
  - Background color to full black for opaque renders
  - Background color to Hue 0, Saturation 0, Value 0.0212 for transparent renders. Blender uses gamma-correction. If you're environment doesn't use gamma-correction, use Value 40/256.

Feel free to save this as a template project, copy it and here we can start our development.

### Character creation

Again, this is too much to cover in this document. But here are the steps:
- Model your character in a neutral pose (relaxed T-pose for humanoids).
- Rig your character
- UV unwrapping
- Texturing
- Apply shader if necessary
- Animate using keyframes. Use DrTester to see examples for desired amount of keyframes.
- If it's an attack or cast frame, make sure to have a one clear keyframe where the hit occurs. In D2, the engine applies the "hit" effect on one single frame. You might want to exaggerate the movement to this frame for impact.

### Rendering

There are a lot of steps here, which I also automated with my [Blender python script](https://github.com/iuitdebos/blender-d2tools). I highly recommend automating this process. Here are the steps:
- Check output settings (naming / resolution etc)
- Transparent or opaque rendering 
  - If you want something glowing or translucent like FingerMages or Mephisto's clouds you need a full-black background. In that case, World > Background full black, and disable Transparent in Render options.
- Max image size for DCC files is 256 x 256 (doesn't need to be square)
  - If you need more than that, see multi-part monsters in the tutorial mentioned in chapter 0. However, once you understand single-part, multi-part is not that much more complicated, just more work.
- Try out a single image render (Render > Render Image), check if looks how you want it to be.
- Note that direction 0 should be facing bottom left.
- Render out the animation (Render > Render Animation) to an image sequence (.PNG's is fine, we need to process them anyway)
- Move those renders to a directory, naming it with _0 for direction.
- Rotate the RotateBox to the next direction. Monsters usually have 8 directions, player characters 16, missiles 32.
  |Directions | Z-rotations|  |       |       |       |       |       |       |
  |-----------|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|
  | 0 .. 7  	| 45 	  | 135 	| 225 	| 315   | 0 	  | 90 	  | 180 	| 270 	|
  | 8 .. 15 	| 22.5 	| 67.5 	| 112.5	| 157.5 | 202.5 | 247.5 | 292.5 | 337.5 |
  | 16 .. 23 	| 11.25 | 33.75 | 56.25	| 78.75 | 101.25| 123.75| 146.25| 168.75|
  | 24 .. 31 	| 191.25| 213.75| 236.25| 258.75| 281.25| 303.75| 326.25| 348.75|
- Render out animation for each direction, moving them to different folders _0, _1, _2 etc.
- Make sure all images within each direction folder must all have the same amount of frames. E.g. 16 image for each direction. You may have different amounts per animation however (neutral or attack etc).

At the end of this chapter you should have rendered images in png format, of all directions. There should be an equal number of frames for all directions.

## Chapter 2: Graphic editing

This example uses Photoshop CS 6, but the steps are not too complicated so if you don't have PS or this specific version, follow that tool's version of these instructions.

### GIF Preparation
- Add all images from each direction to your document, in order of direction as listed above, in separate layers.
  - Photoshop CS6 has a useful function for this, File > Scripts > Load Files into Stack. This allows you to select files and it will load them into separate layers for you.
- Open the Timeline / animations panel (Window > Timeline)
- In top right of panel, click on the extra options and select "Make Frames from Layers"
- Most likely the frames will be in reverse order (last frame is first), check that and if necessary you can click "Reverse Frames" in the same menu.
- Select all frames, right click on a frame and and instead of Automatic choose "Dispose". This is necessary because when Photoshop wants to render a .gif, normally it would be optimized saving only the changes between frames rather than the full image every single frame. We don't want this as Diablo does not handle this well and we neat the full image every frame.
- Final check, you can run the animation in Photoshop. Make sure it has all directions, in the correct order, and that no frames are missing.

### GIF Exporting
- In Photoshop CS 6, you need to go File > Save for Web. In general however, just "Save as file type (animated) GIF".
- GIF File type
- Set colors to 256. Dither pattern as Diffusion is fine.
- Set "Matte" to full black
- Set "Metadata and Copyright info" to None
- Check / uncheck transparency depending on your needs.
- In the Color Table section, top right menu "Load Color Table". Select units.act to load in the .dcc color palette.
- Save as \<token>TRLIT\<animation>HTH_anim.gif, e.g. CRTRLITNUHTH_anim.gif

Now you should have an animated .gif that you can play, that in the correct order animates through all directions.

Troubleshooting:
- If you get random white dots, your "matte" is not set.
- If later on in the process random pixels are missing, double check to remove any optimization in the .gif.
- If your first frame has some seemingly random scratches on it, that means that your program has added some data at the start of the gif. Add an empty 1st frame (or duplicate it) to the .gif export. Then, in the next step when saving as .DCC, select from Frame 1 rather than Frame 0. 


## Chapter 3: DCC and COF

Roughly speaking, a .dcc is a filetype similar to .gif but that comes prepared with some extra information for Diablo 2. This includes where the floor would be in relation to the animation, separates it into directions and some other stuff probably.

The .cof file combines multiple .dcc's into a single "token". This can have multiple layers (think Mephisto, which has a solid body and the white glowy misty thing around him), and multiple body parts (character helmets, armors, weapons etc).

### Convert to DCC

Start up Cv5 and navigate to where your _anim.gif is stored, and load it. It should show all the frames. Press "View" to see if it renders the frames as you expect (see troubleshooting in the step above if it doesn't); you should see a grey background with your model on top. If what you're working on needs to be a glowy effect, it should have a black background.

- Click on "Save" in the bottom half on the right.
- Select ".dcc" as Filetype to save as (important)
- Name it \<token>TRLIT\<animation>HTH.dcc
- A modal should pop up for setting up the DCC settings.
- Select your amount of directions (e.g. "8 directions") with your amount of frames. If this is greyed out, or the amount doesn't match with your rendered images, the frame count is wrong somehow. Double-check that all your directions have an equal amount of frames.
- White text boxes open up for each direction. These determine the point that Diablo will use as the "center" of the image; e.g. the root on which it bases where the monster or missile is.
- Fill in numbers (try negative numbers), using the preview to see where the crosshair gets placed. This should be horizontally centered, vertically where the floor should be in relation to the animation.
- Save the .dcc and move / copy it to /data/global/monsters/\<token>/tr/\<filename>.dcc

### COF Editing

COF editing is quite complicated to start completely blank with, so unless you've done this before I recommend copying an existing monster's .COF file initially. To limit how much we need to customize, choose a monster that's somewhat similar in terms of what kinds of animations it has and how many layers (single-part or multi-part, glowing translucent parts or no).

- As an example, we have a solid body with a glowing overlay like the FingerMage's you encounter in act 4. We copy all FingerMage .cof files to /data/global/monsters/\<token>/cof/\<filename>.cof
- Open this .cof with CofEditor (drag the .cof on top of the .exe).
- This should show the Fingermage animation in the editor.
- If you select the neutral animation, it should show your animation!
  - .cof files loads the .dcc files from the relative subdirectory, so directory setup is important. (e.g. \<token>/cof/\<filename>.cof and \<token>/tr/\<filename>.dcc)
  - Solid bodies / single bodyparts are usually Torso (/tr/.dcc). If you have glowy effects, they are often as overlay as Special 1 (/s1/.dcc).
- There are a couple of things to change.
- Make sure to set the Frame/dir to your correct number.
- Normal animation speed is 256. Set TNSpeed to 256, or unless you want something specific do that but keep that in mind for the next step.
- If it's an attack animation, make sure to set "Trigger" to 1 (or whatever your original .cof has) on the frame that is supposed to "hit" or cast. Any other frames should be 0.
- Other animations like NU (neutral), DT (death) etc don't have any trigger, all should be 0.
- Don't forget to hit "Save".

Now you should have a .COF file that is using your animations.


## Chapter 4: Text editing

### AnimData.D2
- From the .mpq, get data/global/AnimData.d2
- Unpack AnimData.D2 using AnimData_Edit by Paul Siramy into an editable AnimData.txt
- Copy the rows from your .cof-copied token (FingerMage) to the bottom of the sheet, and replace the token in the filename with your own.
- Set the frame count to your animation's framecount
- Set the frame speed to your TNSpeed in the .cof
- If it's an attack animation, go to the column for the frame where you marked the trigger and mark it with the same value (1). All other columns should be 0. Any animation that doesn't have a hit (like neutral, death etc) will only have 0's.
- Save and re-pack the AnimData.txt back into a .D2. Note that this will override any existing AnimData.d2, so backup if you need to.

### MonStats / .txt files
- Open monstats.txt
- Create a new row, feel free to copy-paste a FingerMage row.
- Update the hcidx to next last index
- Set the Token to your new token we've been using throughout.
- Now this monster should use your animation!
- Note, that certain AI needs certain animation types to not crash the game. E.g. spellcasting AI might need a SC / S1 animation. Almost all monsters should have at least A1, A2, DD, DT, GH, NU and WL. So repeat this process for all those :)


## Chapter 5: Design tips

- Check out the Phrozen Keep discord.
- Proportions should be slighly exaggerated, especially details, as small details will not render on small scale. Think of a small 3d-printed boardgame miniature.
- Animations should be similarly clear. Think of Andariel's back spider legs and follow the huge arcs they make.
- Keep it simple with colors. Especially monsters you will have many of on the screen. Most monsters are largely 1 color with details in a secondary color. Bosses can have slightly more colors because there will be fewer of on the screen.
- Similarly, don't go crazy with asymmetry. Details can be asymmetrical and so can animations. The common monster models in D2 are usually fairly symmetric however.
- For attacks, have a clear frame where they hit should occur, rather than a flowing motion where it would be unclear, as D2 does the "effect" of the attack on one specific frame.


## Chapter 6: Reference


### Isometric 3D Setup
- Sun (/ directional) light.
  - Position: (8.05, -11.788, 24)
  - Rotation: (0, 30.7, -55.7)
  - Light settings: Default (1 Strength, full white light)
- Camera settings
  - Position: (0, -30, 20)
  - Rotation: (60, 0, 0)
  - Set to "Ortographic" projection, ortho scale of 7.0
- Ambient light of 40 / 256 rgb (0.0212 / 1 gamma-corrected)

### Directions
Rotate the rotatebox in the Z-axis

|Directions | Z-rotations|  |       |       |       |       |       |       |
  |-----------|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|
  | 0 .. 7  	| 45 	  | 135 	| 225 	| 315   | 0 	  | 90 	  | 180 	| 270 	|
  | 8 .. 15 	| 22.5 	| 67.5 	| 112.5	| 157.5 | 202.5 | 247.5 | 292.5 | 337.5 |
  | 16 .. 23 	| 11.25 | 33.75 | 56.25	| 78.75 | 101.25| 123.75| 146.25| 168.75|
  | 24 .. 31 	| 191.25| 213.75| 236.25| 258.75| 281.25| 303.75| 326.25| 348.75|

### Animation Modes

- A1 – Attack 1
- A2 – Attack 2
- TH – Throw (Most monsters don’t have this)
- KK – Kick (Most monsters don’t have this)
- SQ – Special sequence (like the amazon’s dodge sequence, or the paladin’s smite)
- SC – Cast
- S1 – Special 1
- S2 – Special 2
- S3 – Special 3
- S4 – Special 4
- GH – Get Hit
- KB – Knockback (Most monsters don’t have this)
- BL – Block (Most monsters don’t have this)
- DD – Corpse
- DT – Death
- NU – Neutral
- WL – Walk
- RN – Run (Most monsters don’t have this)
- TN – Town Neutral (Only for player animations)
- TW – Town Walk (Only for player animations)

### Hit-Class Codes

These are for organizing different weapons used by the same creature, most monsters only have HTH mode, but some have others.
- HTH - Hand to Hand
- 1HS - 1-handed Strike
- 2HS - 2-handed Strike
- 1HT - 1-handed Thrust
- 2HT - 2-handed Thrust
- STF - (? Staff?)
- 1JS - 1-handed jab-strike
- 1JT - 1-handed jab-thrust
- 1SS - (?)
- 1ST - (?)
- BOW - Bow
- XBW - Crossbow
 

### Armor-Class Codes

You will only need the first three codes (LIT,MED,HVY) for monsters, the rest are player codes, or used for complex monsters.

All armors:
- HVY
- LIT
- MED

Head:
- BHM
- CAP
- CRN
- FHL
- GHM
- HLM
- MSK
- SKP

Left hand:
- HXB
- LBB
- LBW
- LXB
- SBB
- SBW

Right hand:
- AXE
- BRN
- BSD
- BST
- BTX
- BWN
- CLB
- CLM
- CRS
- CST
- DGR
- DIR
- FLA
- FLC
- GIX
- GLV
- GPL
- GPS
- GSD
- HAL
- HAX
- HXB
- JAV
- LAX
- LSD
- LST
- LXB
- MAC
- MAU
- OPL
- OPS
- PAX
- PIK
- PIL
- SCM
- SCY
- SPR
- SSD
- SST
- TRI
- WHM
- WND
- YWN
