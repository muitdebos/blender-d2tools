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
        row.label(text = "WIP")
        
        row = layout.row()
        row.label(text = "World Ambient")
        
        row = layout.row()
        row.label(text = "Value: 0.021219")
        
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
        
        row = layout.row()
        row.operator("d2tools.ops_render")

          
#################
##  OPERATORS  ##
#################

class D2TOOLS_OT_generate(bpy.types.Operator):
    bl_label = "Generate scene"
    bl_idname = "d2tools.ops_generate"
    bl_description = "Generates the rotatebox, camera and light settings required for D2 rendering"
    
    def generate_objects(self, context):
        
        # Generate rotatebox
        rotatebox = bpy.data.objects.new('ROTATEBOX', None)
        bpy.context.collection.objects.link(rotatebox)
        rotatebox.empty_display_size = 0.5
        rotatebox.empty_display_type = 'PLAIN_AXES'
        
        # Generate camera
        cam_data = bpy.data.cameras.new('camera')
        cam = bpy.data.objects.new('CAMERA', cam_data)
        bpy.context.collection.objects.link(cam)
        bpy.context.scene.camera=cam
        cam.location = (0, -30, 20)
        cam.rotation_euler[0] = math.radians(60)
        cam.rotation_euler[1] = math.radians(0)
        cam.rotation_euler[2] = math.radians(0)
        cam.data.type = 'ORTHO'
        cam.data.ortho_scale = 7
        
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
        light.parent = rotatebox
        rotatebox.rotation_euler[0] = math.radians(0)
        rotatebox.rotation_euler[1] = math.radians(0)
        rotatebox.rotation_euler[2] = math.radians(45)
        
        return True
    
    
    def generate_examples(self, context):
        
        # Create root object for approximate scale example
        scales = bpy.data.objects.new('_Approximate_Scale_', None)
        bpy.context.collection.objects.link(scales)
        scales.empty_display_size = 0.5
        scales.empty_display_type = 'ARROWS'
        scales.hide_render = True
        
        # Generate cubes representing approximately the height and stature of a human
        bpy.ops.mesh.primitive_cube_add(
            size=1,
            enter_editmode=False,
            align='WORLD',
            location=(0, 0, 1.7),
            scale=(0.2, 0.25, 0.25),
        )
        humanHead = bpy.context.active_object
        humanHead.name = 'Human_Head'
        humanHead.show_wire = True
        humanHead.display_type = 'WIRE'
        humanHead.parent = scales
        
        bpy.ops.mesh.primitive_cube_add(
            size=1,
            enter_editmode=False,
            align='WORLD',
            location=(0, 0, 1.15),
            scale=(0.5, 0.25, 0.7),
        )
        humanTorso = bpy.context.active_object
        humanTorso.name = 'Human_Torso'
        humanTorso.show_wire = True
        humanTorso.display_type = 'WIRE'
        humanTorso.parent = scales
        
        bpy.ops.mesh.primitive_cube_add(
            size=1,
            enter_editmode=False,
            align='WORLD',
            location=(0.15, 0, 0.4),
            scale=(0.15, 0.15, 0.8),
        )
        humanLegL = bpy.context.active_object
        humanLegL.name = 'Human_Leg_L'
        humanLegL.show_wire = True
        humanLegL.display_type = 'WIRE'
        humanLegL.parent = scales
        
        bpy.ops.mesh.primitive_cube_add(
            size=1,
            enter_editmode=False,
            align='WORLD',
            location=(-0.15, 0, 0.4),
            scale=(0.15, 0.15, 0.8),
        )
        humanLegR = bpy.context.active_object
        humanLegR.name = 'Human_Leg_R'
        humanLegR.show_wire = True
        humanLegR.display_type = 'WIRE'
        humanLegR.parent = scales
        
        return True
    
    
    def scene_setup(self, context):
        
        # Set up output settings
        bpy.context.scene.render.engine = 'CYCLES'
        bpy.context.scene.render.resolution_x = 256
        bpy.context.scene.render.resolution_y = 256
        bpy.context.scene.frame_end = 8
        bpy.context.scene.render.fps = 25
        
        # Disable anti-alias
        bpy.context.scene.cycles.pixel_filter_type = 'GAUSSIAN'
        bpy.context.scene.cycles.filter_width = 0.02
        
        # Black background
        bpy.context.scene.render.film_transparent = True
        bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value = d2_ambient
        
        return True
    
    
    def execute(self, context):
        
        self.generate_objects(context)
        self.generate_examples(context)
        self.scene_setup(context)
        
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
                frameNum   = str( f ).zfill(4) # Zero-padds frame number (5 -> 0005)
                frameName = "{prefix}_{dir}_{f}{ext}".format(
                    prefix = fileName,
                    dir = i,
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
    
    
################
##  REGISTER  ##
################

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
]

def register():
    bpy.types.Scene.d2tools_outputDir = d2tools_outputDir
    bpy.types.Scene.d2tools_fileName = d2tools_fileName
    bpy.types.Scene.d2tools_directions = d2tools_directions
    bpy.types.Scene.d2tools_skipDirections = d2tools_skipDirections
    
    for c in registerClasses:
        bpy.utils.register_class(c)
   
def unregister():
    del bpy.types.Scene.d2tools_outputDir
    del bpy.types.Scene.d2tools_fileName
    del bpy.types.Scene.d2tools_directions
    del bpy.types.Scene.d2tools_skipDirections
    
    for c in registerClasses:
        bpy.utils.unregister_class(c)
   
if __name__ == "__main__":
    register()
    