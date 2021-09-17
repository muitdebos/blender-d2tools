bl_info = {
    "name": "Diablo 2 Tools",
    "author": "Aerlynn",
    "version": (1, 0),
    "blender": (2, 93, 1),
    "location": "View3D > Toolbar > Diablo 2",
    "description": "Generate Diablo 2 ready scene and automate the rendering process.",
    "warning": "",
    "wiki_url": "",
    "category": "Render",
}

import bpy
import math
from os.path import join

# Monsters have 8 directions
# Characters have 16 directions
# Missiles have 32 directions
d2_directions = [
    (0.0, 0.0, 45.0),
    (0.0, 0.0, 135.0),
    (0.0, 0.0, 225.0),
    (0.0, 0.0, 315.0),
    (0.0, 0.0, 0.0),
    (0.0, 0.0, 90.0),
    (0.0, 0.0, 180.0),
    (0.0, 0.0, 270.0),
    (0.0, 0.0, 22.5),
    (0.0, 0.0, 67.5),
    (0.0, 0.0, 112.5),
    (0.0, 0.0, 157.5),
    (0.0, 0.0, 202.5),
    (0.0, 0.0, 247.5),
    (0.0, 0.0, 292.5),
    (0.0, 0.0, 337.5),
    (0.0, 0.0, 11.25),
    (0.0, 0.0, 33.75),
    (0.0, 0.0, 56.25),
    (0.0, 0.0, 78.75),
    (0.0, 0.0, 101.25),
    (0.0, 0.0, 123.75),
    (0.0, 0.0, 146.25),
    (0.0, 0.0, 168.75),
    (0.0, 0.0, 191.25),
    (0.0, 0.0, 213.75),
    (0.0, 0.0, 236.25),
    (0.0, 0.0, 258.75),
    (0.0, 0.0, 281.25),
    (0.0, 0.0, 303.75),
    (0.0, 0.0, 326.25),
    (0.0, 0.0, 348.75),
]

# Ambient lighting for transparent renders
d2_ambient = (0.0212, 0.0212, 0.0212, 1)
# Background for opaque renders
d2_background = (0, 0, 0, 1)

# Inventory tile size in pixels
d2_inv_tilesize = 28


##########
##  UI  ##
##########

class VIEW3D_PT_D2ToolsPanel(bpy.types.Panel):
    bl_label = "Diablo 2 Tools"
    bl_idname = "D2TOOLS.VIEW3D_PT_D2ToolsPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Diablo 2'
   
    def draw(self, context):
        layout = self.layout
        
        row = layout.row()
        row.prop(context.scene, "d2tools_types", expand = True)


class VIEW3D_PT_D2ToolsGenerate(bpy.types.Panel):
    bl_label = "Generate"
    bl_idname = "D2TOOLS.VIEW3D_PT_D2ToolsGenerate"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Diablo 2'
    bl_parent_id = 'D2TOOLS.VIEW3D_PT_D2ToolsPanel'
   
    def draw(self, context):
        layout = self.layout
        
        row = layout.row()
        row.prop(context.scene, "d2tools_generateRotatebox")
        
        row = layout.row()
        row.prop(context.scene, "d2tools_generateExamples")
        
        row = layout.row()
        row.prop(context.scene, "d2tools_generateSceneSetup")
        
        row = layout.row()
        row.operator("d2tools.ops_generate")
       
       
class VIEW3D_PT_D2ToolsRenderProperties(bpy.types.Panel):
    bl_label = "Render properties"
    bl_idname = "D2TOOLS.VIEW3D_PT_D2ToolsRenderProperties"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Diablo 2'
    bl_parent_id = 'D2TOOLS.VIEW3D_PT_D2ToolsPanel'
   
    def draw(self, context):
        layout = self.layout
        
        row = layout.row()
        row.prop(context.scene, "d2tools_fileName", text = "Name", icon = 'FILE')
        
        row = layout.row()
        row.prop(context.scene, "d2tools_outputDir")
        
        if (context.scene.d2tools_types == "D2ISO"):
            row = layout.row()
            row.label(text = "Directions to render")
            row = layout.row()
            row.prop(context.scene, "d2tools_directions", expand = True)
            row = layout.row()
            row.prop(context.scene, "d2tools_skipDirections")
            row = layout.row()
            row.prop(context.scene, "frame_start", text = "Frame start")
            row = layout.row()
            row.prop(context.scene, "frame_end", text = "Frame end")
            
            
        if (context.scene.d2tools_types == "D2ITEM"):
            row = layout.row()
            row.operator("d2tools.ops_set_inv_render")
            
        
class VIEW3D_PT_D2ToolsRender(bpy.types.Panel):
    bl_label = "Render"
    bl_idname = "D2TOOLS.VIEW3D_PT_D2ToolsRender"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Diablo 2'
    bl_parent_id = 'D2TOOLS.VIEW3D_PT_D2ToolsPanel'
   
    def draw(self, context):
        layout = self.layout
        
        row = layout.row()
        row.prop(context.scene.render, "film_transparent")
        
        if (context.scene.d2tools_types == "D2ISO"):
            row = layout.row()
            row.operator("d2tools.ops_render")
            
        if (context.scene.d2tools_types == "D2ITEM"):
            row = layout.row()
            row.operator("render.render")

          
#################
##  OPERATORS  ##
#################

class D2TOOLS_OT_generate(bpy.types.Operator):
    bl_label = "Generate"
    bl_idname = "d2tools.ops_generate"
    bl_description = "Generates the selected properties to bootstrap the D2 render pipeline"
    
    def generate_objects_iso(self, context):
        
        # Generate rotatebox
        rotatebox = bpy.data.objects.new('ROTATEBOX', None)
        bpy.context.collection.objects.link(rotatebox)
        rotatebox.empty_display_size = 0.5
        rotatebox.empty_display_type = 'PLAIN_AXES'
        
        # Generate camera
        cam_data = bpy.data.cameras.new('camera')
        cam = bpy.data.objects.new('CAMERA', cam_data)
        bpy.context.collection.objects.link(cam)
        bpy.context.scene.camera = cam
        cam.location = (0, -30, 20)
        cam.rotation_euler[0] = math.radians(60)
        cam.rotation_euler[1] = math.radians(0)
        cam.rotation_euler[2] = math.radians(0)
        cam.data.type = 'ORTHO'
        cam.data.ortho_scale = 7
        
        # Generate floor tile camera
        fs_cam_data = bpy.data.cameras.new('camera')
        fs_cam = bpy.data.objects.new('FS_CAMERA', fs_cam_data)
        bpy.context.collection.objects.link(fs_cam)
        bpy.context.scene.camera = fs_cam
        fs_cam.location = (0, -34.65, 20)
        fs_cam.rotation_euler[0] = math.radians(60)
        fs_cam.rotation_euler[1] = math.radians(0)
        fs_cam.rotation_euler[2] = math.radians(0)
        fs_cam.data.type = 'ORTHO'
        fs_cam.data.ortho_scale = 2.8
        
        # Generate light source
        light_data = bpy.data.lights.new('light', type='SUN')
        light = bpy.data.objects.new('LIGHT', light_data)
        bpy.context.collection.objects.link(light)
        light.location = (8.05, -11.788, 24)
        light.rotation_euler[0] = math.radians(0)
        light.rotation_euler[1] = math.radians(30.7)
        light.rotation_euler[2] = math.radians(-55.7)
        
        # Parent camera and light to rotatebox, then rotate box to direction 0
        cam.parent = rotatebox
        fs_cam.parent = rotatebox
        light.parent = rotatebox
        rotatebox.rotation_euler[0] = math.radians(0)
        rotatebox.rotation_euler[1] = math.radians(0)
        rotatebox.rotation_euler[2] = math.radians(45)
        
        # Don't allow user to meddle with settings by default
        cam.hide_select = True
        fs_cam.hide_select = True
        light.hide_select = True
        rotatebox.hide_select = True
        
        return True
    
    def generate_objects_item(self, context):
        
        # Generate rotatebox
        rotatebox = bpy.data.objects.new('ROTATEBOX', None)
        bpy.context.collection.objects.link(rotatebox)
        rotatebox.empty_display_size = 0.5
        rotatebox.empty_display_type = 'PLAIN_AXES'
        
        # Generate camera
        cam_data = bpy.data.cameras.new('camera')
        cam = bpy.data.objects.new('CAMERA', cam_data)
        bpy.context.collection.objects.link(cam)
        bpy.context.scene.camera = cam
        cam.location = (0, -10, 0)
        cam.rotation_euler[0] = math.radians(90)
        cam.rotation_euler[1] = math.radians(0)
        cam.rotation_euler[2] = math.radians(0)
        cam.data.type = 'ORTHO'
        cam.data.ortho_scale = 2.3
        
        # Generate primary light source
        light_data = bpy.data.lights.new('light', type='POINT')
        light = bpy.data.objects.new('MAIN_LIGHT', light_data)
        bpy.context.collection.objects.link(light)
        light.location = (0.1, -0.7, -0.3)
        light.energy = 50
        light.shadow_soft_size = 0.1
        
        # sun backup
        # light.location = (2.3, -2.78, 6.8)
        # light.rotation_euler[0] = math.radians(0)
        # light.rotation_euler[1] = math.radians(60)
        # light.rotation_euler[2] = math.radians(-75)
        # light.energy = 2
        # light.angle = math.radians(10)
        
        # Parent camera and light to rotatebox
        cam.parent = rotatebox
        light.parent = rotatebox
        
        # Don't allow user to meddle with settings by default
        cam.hide_select = True
        light.hide_select = True
        rotatebox.hide_select = True
        
        return True
    
    
    def generate_examples_iso(self, context):
        
        # Create root object for approximate scale example
        scales = bpy.data.objects.new('_Approximate_Scale_', None)
        bpy.context.collection.objects.link(scales)
        scales.empty_display_size = 0.5
        scales.empty_display_type = 'ARROWS'
        scales.hide_render = True
        
        # Example cubes representing approximately the height and stature of a human
        def new_bodypart(name, scale, location):
            bpy.ops.mesh.primitive_cube_add(
                size = 1,
                enter_editmode = False,
                align = 'WORLD',
                location = location,
                scale = scale,
            )
            bodypart = bpy.context.active_object
            bodypart.name = name
            bodypart.show_wire = True
            bodypart.display_type = 'WIRE'
            bodypart.parent = scales
            bodypart.hide_render = True
        
        # Generate cubes representing approximately the height and stature of a human
        new_bodypart('Human_Head', (0.2, 0.25, 0.25), (0, 0, 1.7))
        new_bodypart('Human_Torso', (0.5, 0.25, 0.7), (0, 0, 1.15))
        new_bodypart('Human_Leg_L', (0.15, 0.15, 0.8), (0.15, 0, 0.4))
        new_bodypart('Human_Leg_R', (0.15, 0.15, 0.8), (-0.15, 0, 0.4))
        
        # Floor tile
        bpy.ops.mesh.primitive_plane_add(
            size = 2,
            enter_editmode = False,
            align = 'WORLD',
        )
        tileExample = bpy.context.active_object
        tileExample.name = 'FS_Tile'
        tileExample.show_wire = True
        tileExample.display_type = 'WIRE'
        tileExample.parent = scales
        
        return True
    
    def generate_examples_item(self, context):
        
        # Inv tile size in Blender units using ortho cam of scale 2.3
        tileSize = 0.2875
        
        # Create root object for approximate scale example
        scales = bpy.data.objects.new('_Inventory_Tiles_', None)
        bpy.context.collection.objects.link(scales)
        scales.empty_display_size = 0.5
        scales.empty_display_type = 'ARROWS'
        scales.hide_render = True
        
        # Generate cubes representing approximately the height and stature of a human
        def new_inv_tile(name, location):
            bpy.ops.mesh.primitive_cube_add(
                size = 1,
                enter_editmode = False,
                align = 'WORLD',
                location = location,
                scale = (tileSize * 2, tileSize * 2, tileSize * 2),
            )
            newTile = bpy.context.active_object
            newTile.name = name
            newTile.show_wire = True
            newTile.display_type = 'WIRE'
            newTile.parent = scales
            newTile.hide_render = True
        
        new_inv_tile("Tile1", (-tileSize, 0, tileSize * 3))
        new_inv_tile("Tile2", (tileSize, 0, tileSize * 3))
        new_inv_tile("Tile3", (-tileSize, 0, tileSize * 1))
        new_inv_tile("Tile4", (tileSize, 0, tileSize * 1))
        new_inv_tile("Tile5", (-tileSize, 0, tileSize * -1))
        new_inv_tile("Tile6", (tileSize, 0, tileSize * -1))
        new_inv_tile("Tile7", (-tileSize, 0, tileSize * -3))
        new_inv_tile("Tile8", (tileSize, 0, tileSize * -3))
        
        
        return True
    
    def scene_setup_common(self, context):
        
        # Set up output settings
        bpy.context.scene.render.engine = 'CYCLES'
        bpy.context.scene.render.fps = 25
        
        # Denoise
        bpy.context.scene.cycles.use_denoising = True
        
        # Disable anti-alias
        bpy.context.scene.cycles.pixel_filter_type = 'GAUSSIAN'
        bpy.context.scene.cycles.filter_width = 0.02
        
        # Black background
        bpy.context.scene.render.film_transparent = True
        bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value = d2_ambient
        
        return True
    
    def scene_setup_iso(self, context):
        
        self.scene_setup_common(context)
        
        # Output settings
        bpy.context.scene.render.resolution_x = 256
        bpy.context.scene.render.resolution_y = 256
        bpy.context.scene.frame_end = 8
        
        return True
    
    def scene_setup_item(self, context):
        
        self.scene_setup_common(context)
        
        # Set up output settings
        bpy.context.scene.render.resolution_x = d2_inv_tilesize * 2
        bpy.context.scene.render.resolution_y = d2_inv_tilesize * 4
        bpy.context.scene.frame_start = 1
        bpy.context.scene.frame_end = 1
        
        return True
    
    
    def execute(self, context):
        
        if (context.scene.d2tools_generateRotatebox):
            if (context.scene.d2tools_types == "D2ISO"):
                self.generate_objects_iso(context)
            elif (context.scene.d2tools_types == "D2ITEM"):
                self.generate_objects_item(context)
            
        if (context.scene.d2tools_generateExamples):
            if (context.scene.d2tools_types == "D2ISO"):
                self.generate_examples_iso(context)
            elif (context.scene.d2tools_types == "D2ITEM"):
                self.generate_examples_item(context)
        
        if (context.scene.d2tools_generateSceneSetup):
            if (context.scene.d2tools_types == "D2ISO"):
                self.scene_setup_iso(context)
            elif (context.scene.d2tools_types == "D2ITEM"):
                self.scene_setup_item(context)
        
        # Deselect anything
        bpy.context.active_object.select_set(False)
        
        return {'FINISHED'}


class D2TOOLS_OT_render(bpy.types.Operator):
    bl_label = "Render directions"
    bl_idname = "d2tools.ops_render"
    bl_description = "Renders out the selected directions using Blender's render settings"
    
    def execute(self, context):
        outputDir = context.scene.d2tools_outputDir
        fileName = context.scene.d2tools_fileName
        numDirections = int(context.scene.d2tools_directions, base=10)
        skipDirections = context.scene.d2tools_skipDirections
        
        if (skipDirections >= numDirections):
            skipDirections = numDirections - 1

        # This object should contain your camera and your point light
        rotatebox = bpy.data.objects["ROTATEBOX"]
        startFrame = bpy.context.scene.frame_start
        endFrame = bpy.context.scene.frame_end
        
        # If transparent, set ambient light. Otherwise set opaque background
        if (bpy.context.scene.render.film_transparent):
            bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value = d2_ambient
        else:
            bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value = d2_background
        
        # Render the frames for each direction
        for i in range(skipDirections, numDirections):
            # Rotate the ROTATEBOX
            rotatebox.rotation_euler[0] = math.radians( d2_directions[i][0] )
            rotatebox.rotation_euler[1] = math.radians( d2_directions[i][1] )
            rotatebox.rotation_euler[2] = math.radians( d2_directions[i][2] )

            # Render animation
            for f in range(startFrame, endFrame + 1):
                bpy.context.scene.frame_set( f ) # Set frame
                
                # Output definitions
                dirNum = str( f ).zfill(2) # Zero-padds direction number (5 -> 05)
                frameNum = str( f ).zfill(4) # Zero-padds frame number (5 -> 0005)
                frameName = "{prefix}_{dir}_{f}{ext}".format(
                    prefix = fileName,
                    dir = dirNum,
                    f = frameNum,
                    ext = bpy.context.scene.render.file_extension,
                )
                bpy.context.scene.render.filepath = join( outputDir, frameName )

                # Render frame
                bpy.ops.render.render(write_still = True)
                
        
        # After rendering, reset ROTATEBOX to 0th direction
        rotatebox.rotation_euler[0] = math.radians( d2_directions[0][0] )
        rotatebox.rotation_euler[1] = math.radians( d2_directions[0][1] )
        rotatebox.rotation_euler[2] = math.radians( d2_directions[0][2] )
            
        print('Finished rendering')
        
        return {'FINISHED'}


class D2TOOLS_OT_set_inv_render(bpy.types.Operator):
    bl_label = "Set inventory space"
    bl_idname = "d2tools.ops_set_inv_render"
    bl_description = "Sets the render output to be one of the inventory space arangements"
    bl_options = {'REGISTER', 'UNDO'}
    
    horizontal_tiles: bpy.props.IntProperty(
        name = 'Horizontal tiles',
        description = 'Number of horizontal inventory spaces',
        default = 2,
        min = 1,
        max = 2,
    )
    vertical_tiles: bpy.props.IntProperty(
        name = 'Vertical tiles',
        description = 'Number of vertical inventory spaces',
        default = 4,
        min = 1,
        max = 4,
    )
    
    def execute(self, context):
        
        bpy.context.scene.render.resolution_x = d2_inv_tilesize * self.horizontal_tiles
        bpy.context.scene.render.resolution_y = d2_inv_tilesize * self.vertical_tiles
        
        return {'FINISHED'}
    
    
################
##  REGISTER  ##
################


d2tools_types = bpy.props.EnumProperty(
    name = 'Graphic type',
    description = 'The type of content to render',
    items = [
        ('D2ISO', 'World', 'Anything in the game world; characters, missiles, objects, environments'),
        ('D2ITEM', 'Item', 'Items are rendered straight on'),
    ],
    default = 'D2ISO',
)

d2tools_generateRotatebox = bpy.props.BoolProperty(
    name = "Rotatebox",
    description = "Generates a ROTATEBOX which is used in the D2Tools render process to render out all directions. After generation, don't touch this unless you know what you're doing",
    default = True,
)

d2tools_generateExamples = bpy.props.BoolProperty(
    name = "Scale example",
    description = "Generates an example mesh that approximates the height of ingame characters to give a sense of scale",
    default = True,
)

d2tools_generateSceneSetup = bpy.props.BoolProperty(
    name = "Scene setup",
    description = "Sets up the world, scene and render settings",
    default = True,
)

d2tools_outputDir = bpy.props.StringProperty(
    name = "Output directory",
    description = "'//' at the start is a relative path.",
    default = "//renders/",
    subtype = "DIR_PATH",
)

d2tools_fileName = bpy.props.StringProperty(
    name = "File name",
    description = "Output will be <file_name>_<direction>_<frame_number>.\n\nRecommendation is the name the animation will have, using D2 naming structure: <token><bodypart><armor><animation><hitclass>. As an example, Corrupt Rogue uses CRTRLITNUHTH",
)

d2tools_directions = bpy.props.EnumProperty(
    name = 'Directions',
    description = 'Number of directions to render',
    items = [
        ('1', '1', 'Renders only facing bottom left corner.'),
        ('4', '4', 'Renders facing all 4 corners.'),
        ('8', '8', '(Monsters) Renders facing all 4 corners and straights.'),
        ('16', '16', '(Player Characters) Renders all including in-between steps.'),
        ('32', '32', '(Missiles) Renders all possible directions D2 can handle.'),
    ],
    default = '8',
)

d2tools_skipDirections = bpy.props.IntProperty(
    name = 'Skip Directions',
    description = 'Number of directions to skip. Only useful if Blender crashes while rendering.',
    default = 0,
    min = 0,
    max = 32,
)

registerClasses = [
    VIEW3D_PT_D2ToolsPanel,
    VIEW3D_PT_D2ToolsGenerate,
    VIEW3D_PT_D2ToolsRenderProperties,
    VIEW3D_PT_D2ToolsRender,
    D2TOOLS_OT_generate,
    D2TOOLS_OT_render,
    D2TOOLS_OT_set_inv_render,
]

def register():
    bpy.types.Scene.d2tools_types = d2tools_types
    bpy.types.Scene.d2tools_generateRotatebox = d2tools_generateRotatebox
    bpy.types.Scene.d2tools_generateExamples = d2tools_generateExamples
    bpy.types.Scene.d2tools_generateSceneSetup = d2tools_generateSceneSetup
    bpy.types.Scene.d2tools_outputDir = d2tools_outputDir
    bpy.types.Scene.d2tools_fileName = d2tools_fileName
    bpy.types.Scene.d2tools_directions = d2tools_directions
    bpy.types.Scene.d2tools_skipDirections = d2tools_skipDirections
    
    for c in registerClasses:
        bpy.utils.register_class(c)
   
def unregister():
    del bpy.types.Scene.d2tools_types
    del bpy.types.Scene.d2tools_generateRotatebox
    del bpy.types.Scene.d2tools_generateExamples
    del bpy.types.Scene.d2tools_generateSceneSetup
    del bpy.types.Scene.d2tools_outputDir
    del bpy.types.Scene.d2tools_fileName
    del bpy.types.Scene.d2tools_directions
    del bpy.types.Scene.d2tools_skipDirections
    
    for c in registerClasses:
        bpy.utils.unregister_class(c)
   
if __name__ == "__main__":
    register()
    