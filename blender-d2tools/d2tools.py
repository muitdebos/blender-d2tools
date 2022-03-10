bl_info = {
    "name": "Diablo 2 Tools",
    "author": "Aerlynn",
    "version": (0, 9),
    "blender": (2, 93, 1),
    "location": "View3D > Toolbar > Diablo 2",
    "description": "Generate Diablo 2 ready scenes and automate the rendering process.",
    "warning": "",
    "doc_url": "https://github.com/iuitdebos/blender-d2tools/tree/main/blender-d2tools",
    "category": "Render",
}

import bpy
import math
from os.path import join

# Monsters have 8 directions
# Characters have 16 directions
# Missiles have 32 directions
d2tools_directions = [
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
d2tools_ambient = (0.0212, 0.0212, 0.0212, 1)
# Background for opaque renders
d2tools_background = (0, 0, 0, 1)

# Entity vars
d2tools_ent_orthoscale = 7

# Environment vars
d2tools_env_tile_x = 160
d2tools_env_tile_y = 80
d2tools_env_orthoscale = 2.83
d2tools_env_cam_root = (15, -15, 12.24)

# Inventory tile size in pixels
d2tools_inv_tilesize = 28


#############
## HELPERS ##
#############

def get_env_camera_vars(scene):
    scale_x = 1
    scale_y = scene.d2tools_wall_height
    ratio_ortho = max(abs(scale_y / scale_x), 1) - 1
    ratio_res = max(abs(scale_y / scale_x), 0)
    
    target_res_x = round(d2tools_env_tile_x)
    target_res_y = round(d2tools_env_tile_y * (ratio_res + 1))
    target_ortho = d2tools_env_orthoscale + (ratio_ortho * d2tools_env_orthoscale / 2)
    target_x_tile_offset = -1 * ratio_res
    target_y_tile_offset = ratio_res
    
    return (
        target_res_x,
        target_res_y,
        target_ortho,
        target_x_tile_offset,
        target_y_tile_offset,
    )

def on_update_wall_height(self, context):
    active_cam = self.camera
    if (active_cam):
        cam_vars = get_env_camera_vars(self)
        
        self.render.resolution_x = cam_vars[0]
        self.render.resolution_y = cam_vars[1]
        active_cam.data.ortho_scale = cam_vars[2]
        
        x = d2tools_env_cam_root[0] + cam_vars[3]
        y = d2tools_env_cam_root[1] + cam_vars[4]
        z = d2tools_env_cam_root[2]
        active_cam.location = (x, y, z)

def on_update_env_render_types(self, context):
    new_state = self.d2tools_env_render_types
    if (new_state == "D2ENV_FLOOR"):
        self.d2tools_wall_height = 0
    elif (new_state == "D2ENV_WALL"):
        self.d2tools_wall_height = 1

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
        row.prop(context.scene, "d2tools_generate_rotatebox")
        
        row = layout.row()
        row.prop(context.scene, "d2tools_generate_examples")
        
        row = layout.row()
        row.prop(context.scene, "d2tools_generate_scene_setup")
        
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
        row.prop(context.scene, "d2tools_output_filename", text = "Name", icon = 'FILE')
        
        row = layout.row()
        row.prop(context.scene, "d2tools_output_dir")
        
        if (context.scene.d2tools_types == "D2ENT"):
            row = layout.row()
            row.label(text = "Directions to render")
            row = layout.row()
            row.prop(context.scene, "d2tools_start_direction")
            row = layout.row()
            row.prop(context.scene, "d2tools_end_direction")
            row = layout.row()
            row.prop(context.scene, "frame_start", text = "Frame start")
            row = layout.row()
            row.prop(context.scene, "frame_end", text = "Frame end")
            row = layout.row()
            row.prop(context.scene, "d2tools_frame_skip")
        
        
        if (context.scene.d2tools_types == "D2ENV"):
            row = layout.row()
            row.prop(context.scene, "d2tools_env_render_types", expand = True)
            
            if (context.scene.d2tools_env_render_types == "D2ENV_WALL"):
                row = layout.row()
                row.prop(context.scene, "d2tools_wall_height")
            
            row = layout.row()
            row.label(text = "Tiles to render")
            row = layout.row()
            row.prop(context.scene, "d2tools_env_min_x")
            row.prop(context.scene, "d2tools_env_min_y")
            row = layout.row()
            row.prop(context.scene, "d2tools_env_max_X")
            row.prop(context.scene, "d2tools_env_max_y")
            
            
        if (context.scene.d2tools_types == "D2INV"):
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
        
        if (context.scene.d2tools_types == "D2ENT"):
            row = layout.row()
            row.operator("d2tools.ops_render")
            
        if (context.scene.d2tools_types == "D2ENV"):
            row = layout.row()
            row.operator("d2tools.ops_render_tiles")
            
        if (context.scene.d2tools_types == "D2INV"):
            row = layout.row()
            row.operator("render.render")

          
#################
##  OPERATORS  ##
#################

class D2TOOLS_OT_generate(bpy.types.Operator):
    bl_label = "Generate"
    bl_idname = "d2tools.ops_generate"
    bl_description = "Generates the selected properties to bootstrap the D2 render pipeline"
    
    def generate_objects_ent(self, context):
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
        cam.location = (0, -10, 8.5)
        cam.rotation_euler[0] = math.radians(60)
        cam.rotation_euler[1] = math.radians(0)
        cam.rotation_euler[2] = math.radians(0)
        cam.data.type = 'ORTHO'
        cam.data.ortho_scale = d2tools_ent_orthoscale
        
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
        
        # Don't allow user to meddle with settings by default
        cam.hide_select = True
        light.hide_select = True
        rotatebox.hide_select = True
        
        return True
    
    def generate_objects_env(self, context):
        # Generate rotatebox
        rotatebox = bpy.data.objects.new('ROTATEBOX', None)
        bpy.context.collection.objects.link(rotatebox)
        rotatebox.empty_display_size = 0.5
        rotatebox.empty_display_type = 'PLAIN_AXES'
        
        # Rotatebox collection
        rotatebox_coll = bpy.data.collections.new("Rotatebox")
        rotatebox_coll.hide_select = True
        bpy.context.scene.collection.children.link(rotatebox_coll)
        rotatebox_coll.objects.link(rotatebox)
        bpy.context.scene.collection.objects.unlink(rotatebox)
        original_collection = bpy.context.view_layer.active_layer_collection
        layer_collection = bpy.context.view_layer.layer_collection.children[rotatebox_coll.name]
        bpy.context.view_layer.active_layer_collection = layer_collection
        
        # Generate floor tile camera
        fs_cam_data = bpy.data.cameras.new('camera')
        fs_cam = bpy.data.objects.new('FS_CAMERA', fs_cam_data)
        bpy.context.collection.objects.link(fs_cam)
        bpy.context.scene.camera = fs_cam
        fs_cam.location = d2tools_env_cam_root
        fs_cam.rotation_euler[0] = math.radians(60)
        fs_cam.rotation_euler[1] = math.radians(0)
        fs_cam.rotation_euler[2] = math.radians(45)
        fs_cam.data.type = 'ORTHO'
        fs_cam.data.ortho_scale = d2tools_env_orthoscale
        
        # Generate light source
        light_data = bpy.data.lights.new('light', type='SUN')
        light = bpy.data.objects.new('LIGHT', light_data)
        bpy.context.collection.objects.link(light)
        light.location = (8.05, -11.788, 24)
        light.rotation_euler[0] = math.radians(0)
        light.rotation_euler[1] = math.radians(30.7)
        light.rotation_euler[2] = math.radians(-55.7)
        light.parent = rotatebox
        
        # Parent camera to rotatebox with proper rotations
        rotatebox.rotation_euler[0] = math.radians(0)
        rotatebox.rotation_euler[1] = math.radians(0)
        rotatebox.rotation_euler[2] = math.radians(45)
        bpy.context.evaluated_depsgraph_get().update()
        fs_cam.parent = rotatebox
        fs_cam.matrix_parent_inverse = rotatebox.matrix_world.inverted()
        
        # Generate holdouts (prevents rendering outside the tile)
        holdout_coll = bpy.data.collections.new("Holdout")
        holdout_coll.hide_select = True
        rotatebox_coll.children.link(holdout_coll)
        layer_collection = bpy.context.view_layer.active_layer_collection.children[holdout_coll.name]
        bpy.context.view_layer.active_layer_collection = layer_collection
        layer_collection.holdout = True
        
        def new_holdout_tile(name, location):
            # Holdout frame tile
            bpy.ops.mesh.primitive_plane_add(
                size = 2,
                enter_editmode = False,
                align = 'WORLD',
            )
            holdout_tile = bpy.context.active_object
            holdout_tile.location = location
            holdout_tile.name = name
            holdout_tile.hide_select = True
            holdout_tile.hide_set(True)
            holdout_tile.parent = fs_cam
            holdout_tile.matrix_parent_inverse = rotatebox.matrix_world.inverted()
            
        new_holdout_tile("Holdout_TL", (10.247, -12.247, 10))
        new_holdout_tile("Holdout_TR", (12.247, -10.247, 10))
        new_holdout_tile("Holdout_BL", (12.247, -14.247, 10))
        new_holdout_tile("Holdout_BR", (14.247, -12.247, 10))
        
        # Don't allow user to meddle with settings by default
        fs_cam.hide_select = True
        light.hide_select = True
        rotatebox.hide_select = True
        
        bpy.context.view_layer.active_layer_collection = original_collection
        
        return True
    
    
    def generate_objects_inv(self, context):
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
        light.data.energy = 50
        light.data.shadow_soft_size = 0.1
        
        # Parent camera and light to rotatebox
        cam.parent = rotatebox
        light.parent = rotatebox
        
        # Don't allow user to meddle with settings by default
        cam.hide_select = True
        light.hide_select = True
        rotatebox.hide_select = True
        
        return True
    
    
    def generate_examples_ent(self, context):
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
        
        return True
    
    def generate_examples_env(self, context):
        # Create root object for approximate scale example
        scales = bpy.data.objects.new('_Approximate_Scale_', None)
        bpy.context.collection.objects.link(scales)
        scales.empty_display_size = 0.5
        scales.empty_display_type = 'ARROWS'
        scales.hide_render = True
        
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
    
    def generate_examples_inv(self, context):
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
        bpy.context.scene.cycles.pixel_filter_type = 'BOX'
        bpy.context.scene.cycles.filter_width = 0.01
        
        # Black background
        bpy.context.scene.render.film_transparent = True
        bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value = d2tools_ambient
        
        return True
    
    def scene_setup_ent(self, context):
        self.scene_setup_common(context)
        
        # Output settings
        bpy.context.scene.render.resolution_x = 256
        bpy.context.scene.render.resolution_y = 256
        bpy.context.scene.frame_end = 8
        
        return True
    
    
    def scene_setup_env(self, context):
        self.scene_setup_common(context)
        
        # Output settings
        bpy.context.scene.render.resolution_x = 160
        bpy.context.scene.render.resolution_y = 80
        bpy.context.scene.frame_end = 1
        
        return True
    
    def scene_setup_inv(self, context):
        self.scene_setup_common(context)
        
        # Set up output settings
        bpy.context.scene.render.resolution_x = d2tools_inv_tilesize * 2
        bpy.context.scene.render.resolution_y = d2tools_inv_tilesize * 4
        bpy.context.scene.frame_start = 1
        bpy.context.scene.frame_end = 1
        
        return True
    
    
    def execute(self, context):
        if (context.scene.d2tools_types == "D2ENT"):
            if (context.scene.d2tools_generate_rotatebox):
                self.generate_objects_ent(context)

            if (context.scene.d2tools_generate_examples):
                self.generate_examples_ent(context)

            if (context.scene.d2tools_generate_scene_setup):
                self.scene_setup_ent(context)
        
        if (context.scene.d2tools_types == "D2ENV"):
            if (context.scene.d2tools_generate_rotatebox):
                self.generate_objects_env(context)

            if (context.scene.d2tools_generate_examples):
                self.generate_examples_env(context)

            if (context.scene.d2tools_generate_scene_setup):
                self.scene_setup_env(context)

        if (context.scene.d2tools_types == "D2INV"):
            if (context.scene.d2tools_generate_rotatebox):
                self.generate_objects_inv(context)

            if (context.scene.d2tools_generate_examples):
                self.generate_examples_inv(context)

            if (context.scene.d2tools_generate_scene_setup):
                self.scene_setup_inv(context)
        
        # Deselect anything
        if (bpy.context.active_object):
            bpy.context.active_object.select_set(False)
        
        return {'FINISHED'}


class D2TOOLS_OT_render_ent(bpy.types.Operator):
    bl_label = "Render directions"
    bl_idname = "d2tools.ops_render"
    bl_description = "Renders out the selected directions using Blender's render settings"
    
    def execute(self, context):
        output_dir = context.scene.d2tools_output_dir
        filename = context.scene.d2tools_output_filename
        start_direction = context.scene.d2tools_start_direction
        end_direction = context.scene.d2tools_end_direction

        if (end_direction < start_direction):
            context.scene.d2tools_end_direction = start_direction
            end_direction = start_direction

        # This object should contain your camera and your directional light
        rotatebox = bpy.data.objects["ROTATEBOX"]
        start_frame = bpy.context.scene.frame_start
        end_frame = bpy.context.scene.frame_end
        frame_skip = context.scene.d2tools_frame_skip + 1
        
        # If transparent, set ambient light. Otherwise set opaque background
        if (bpy.context.scene.render.film_transparent):
            bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value = d2tools_ambient
        else:
            bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value = d2tools_background
        
        # Render the frames for each direction
        for d in range(start_direction, end_direction + 1):
            # Rotate the ROTATEBOX
            rotatebox.rotation_euler[0] = math.radians( d2tools_directions[d][0] )
            rotatebox.rotation_euler[1] = math.radians( d2tools_directions[d][1] )
            rotatebox.rotation_euler[2] = math.radians( d2tools_directions[d][2] )

            # Render animation
            endWithSkips = math.floor((end_frame - start_frame) / frame_skip) + start_frame + 1
            for f in range(start_frame, endWithSkips):
                target_frame = f + (f - start_frame) * (frame_skip - 1)
                bpy.context.scene.frame_set( target_frame ) # Set frame
                
                # Output definitions
                dir_num = str( d ).zfill(2) # Zero-padds direction number (5 -> 05)
                frame_num = str( target_frame ).zfill(4) # Zero-padds frame number (5 -> 0005)
                frame_name = f"{filename}_{dir_num}_{frame_num}{bpy.context.scene.render.file_extension}"
                bpy.context.scene.render.filepath = join( output_dir, frame_name )

                # Render frame
                bpy.ops.render.render(write_still = True)
                
        
        # After rendering, reset ROTATEBOX to 0th direction
        rotatebox.rotation_euler[0] = math.radians( d2tools_directions[0][0] )
        rotatebox.rotation_euler[1] = math.radians( d2tools_directions[0][1] )
        rotatebox.rotation_euler[2] = math.radians( d2tools_directions[0][2] )
            
        print('Finished rendering')
        
        return {'FINISHED'}


class D2TOOLS_OT_render_ent_env(bpy.types.Operator):
    bl_label = "Render tiles"
    bl_idname = "d2tools.ops_render_tiles"
    bl_description = "Renders out the selected tile using Blender's render settings"
    
    def execute(self, context):
        output_dir = context.scene.d2tools_output_dir
        filename = context.scene.d2tools_output_filename
        min_x = context.scene.d2tools_env_min_x
        min_y = context.scene.d2tools_env_min_y
        max_x = context.scene.d2tools_env_max_X
        max_y = context.scene.d2tools_env_max_y

        if (max_x < min_x):
            context.scene.d2tools_env_max_X = min_x
            max_x = min_x
        if (max_y < min_y):
            context.scene.d2tools_env_max_y = min_y
            max_y = min_y

        # This object should contain your camera and your directional light
        rotatebox = bpy.data.objects["ROTATEBOX"]
        
        # If transparent, set ambient light. Otherwise set opaque background
        if (bpy.context.scene.render.film_transparent):
            bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value = d2tools_ambient
        else:
            bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value = d2tools_background
        
        # Render the frames for each direction
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                # Move rotatebox to target tile
                rotatebox.location = (-2*x, 2*y, 0)
                
                # Output definitions
                x_num = str( x ).zfill(2) # Zero-padds x number (5 -> 05)
                y_num = str( y ).zfill(2) # Zero-padds y number (5 -> 05)
                frame_name = f"{filename}_{x_num}_{y_num}{bpy.context.scene.render.file_extension}"
                bpy.context.scene.render.filepath = join( output_dir, frame_name )

                # Render frame
                bpy.ops.render.render(write_still = True)
        
        # Reset rotatebox to root
        rotatebox.location = (0, 0, 0)
        
        print('Finished rendering')
        
        return {'FINISHED'}


class D2TOOLS_OT_set_inv_render(bpy.types.Operator):
    bl_label = "Set inventory space"
    bl_idname = "d2tools.ops_set_inv_render"
    bl_description = "Sets the render output to be one of the inventory space arrangements"
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
        
        bpy.context.scene.render.resolution_x = d2tools_inv_tilesize * self.horizontal_tiles
        bpy.context.scene.render.resolution_y = d2tools_inv_tilesize * self.vertical_tiles
        
        return {'FINISHED'}
    

################
##  REGISTER  ##
################

d2tools_types = bpy.props.EnumProperty(
    name = 'Graphic type',
    description = 'The type of content to render',
    items = [
        ('D2ENT', 'Entity', 'Anything 3D in the game world; characters, missiles, objects'),
        ('D2ENV', 'Environment', 'Environment pieces, floor tiles, walls etc.'),
        ('D2INV', 'Inventory', 'Inventory graphics are rendered straight on. Official graphics have often been touched up in 2D after rendering.'),
    ],
    default = 'D2ENT',
)

d2tools_generate_rotatebox = bpy.props.BoolProperty(
    name = "Rotatebox",
    description = "Generates a ROTATEBOX which is used in the D2Tools render process to render out all directions. After generation, don't touch this unless you know what you're doing",
    default = True,
)

d2tools_generate_examples = bpy.props.BoolProperty(
    name = "Scale example",
    description = "Generates an example mesh that approximates the height of ingame characters to give a sense of scale",
    default = True,
)

d2tools_generate_scene_setup = bpy.props.BoolProperty(
    name = "Scene setup",
    description = "Sets up the world, scene and render settings",
    default = True,
)

d2tools_output_dir = bpy.props.StringProperty(
    name = "Output directory",
    description = "'//' at the start is a relative path.",
    default = "//renders/",
    subtype = "DIR_PATH",
)

d2tools_output_filename = bpy.props.StringProperty(
    name = "File name",
    description = "Output will be <file_name>_<direction>_<frame_number>.\n\nRecommendation is the name the animation will have, using D2 naming structure: <token><bodypart><armor><animation><hitclass>. As an example, Corrupt Rogue uses CRTRLITNUHTH",
)

d2tools_frame_skip = bpy.props.IntProperty(
    name = 'Frame skip',
    description = 'Skip every X frames. Frame skip of 1 renders frames 0, 2, 4, 6 etc.',
    default = 0,
    min = 0,
    max = 50,
)

d2tools_start_direction = bpy.props.IntProperty(
    name = 'Start direction',
    description = 'Number of starting direction. 0 is facing bottom-left.',
    default = 0,
    min = 0,
    max = 31,
)

d2tools_end_direction = bpy.props.IntProperty(
    name = 'End direction',
    description = 'Number of end direction. Only useful if Blender crashes while rendering.',
    default = 0,
    min = 0,
    max = 31,
)

d2tools_env_render_types = bpy.props.EnumProperty(
    name = 'Render type',
    description = 'The type of content to render',
    items = [
        ('D2ENV_FLOOR', 'Floor', 'Flat floor or roof tiles. Always 160x80 pixels.'),
        ('D2ENV_WALL', 'Wall', 'Wall tiles. Always 160 pixels wide, variable height.'),
    ],
    default = 'D2ENV_FLOOR',
    update = on_update_env_render_types
)

d2tools_wall_height = bpy.props.IntProperty(
    name = 'Wall height',
    description = 'Height of walls in tiles (0 is 160x80, 1 is 160x160 etc.)',
    default = 0,
    min = 0,
    update = on_update_wall_height
)

d2tools_env_min_x = bpy.props.IntProperty(
    name = 'Min X',
    description = 'Start rendering from this tile X.',
    default = 0,
    min = 0,
)

d2tools_env_min_y = bpy.props.IntProperty(
    name = 'Min Y',
    description = 'Start rendering from this tile Y.',
    default = 0,
    min = 0,
)

d2tools_env_max_X = bpy.props.IntProperty(
    name = 'Max X',
    description = 'Render tiles until this tile X.',
    default = 0,
    min = 0,
)

d2tools_env_max_y = bpy.props.IntProperty(
    name = 'Max Y',
    description = 'Render tiles until this tile Y.',
    default = 0,
    min = 0,
)

registerClasses = [
    VIEW3D_PT_D2ToolsPanel,
    VIEW3D_PT_D2ToolsGenerate,
    VIEW3D_PT_D2ToolsRenderProperties,
    VIEW3D_PT_D2ToolsRender,
    D2TOOLS_OT_generate,
    D2TOOLS_OT_render_ent,
    D2TOOLS_OT_render_ent_env,
    D2TOOLS_OT_set_inv_render,
]

def register():
    bpy.types.Scene.d2tools_types = d2tools_types
    bpy.types.Scene.d2tools_generate_rotatebox = d2tools_generate_rotatebox
    bpy.types.Scene.d2tools_generate_examples = d2tools_generate_examples
    bpy.types.Scene.d2tools_generate_scene_setup = d2tools_generate_scene_setup
    bpy.types.Scene.d2tools_output_dir = d2tools_output_dir
    bpy.types.Scene.d2tools_output_filename = d2tools_output_filename
    bpy.types.Scene.d2tools_frame_skip = d2tools_frame_skip
    bpy.types.Scene.d2tools_start_direction = d2tools_start_direction
    bpy.types.Scene.d2tools_end_direction = d2tools_end_direction
    bpy.types.Scene.d2tools_env_render_types = d2tools_env_render_types
    bpy.types.Scene.d2tools_wall_height = d2tools_wall_height
    bpy.types.Scene.d2tools_env_min_x = d2tools_env_min_x
    bpy.types.Scene.d2tools_env_min_y = d2tools_env_min_y
    bpy.types.Scene.d2tools_env_max_X = d2tools_env_max_X
    bpy.types.Scene.d2tools_env_max_y = d2tools_env_max_y
    
    for c in registerClasses:
        bpy.utils.register_class(c)
   
def unregister():
    del bpy.types.Scene.d2tools_types
    del bpy.types.Scene.d2tools_generate_rotatebox
    del bpy.types.Scene.d2tools_generate_examples
    del bpy.types.Scene.d2tools_generate_scene_setup
    del bpy.types.Scene.d2tools_output_dir
    del bpy.types.Scene.d2tools_output_filename
    del bpy.types.Scene.d2tools_frame_skip
    del bpy.types.Scene.d2tools_start_direction
    del bpy.types.Scene.d2tools_end_direction
    del bpy.types.Scene.d2tools_env_render_types
    del bpy.types.Scene.d2tools_wall_height
    del bpy.types.Scene.d2tools_env_min_x
    del bpy.types.Scene.d2tools_env_min_y
    del bpy.types.Scene.d2tools_env_max_X
    del bpy.types.Scene.d2tools_env_max_y
    
    for c in registerClasses:
        bpy.utils.unregister_class(c)
   
if __name__ == "__main__":
    register()
    
