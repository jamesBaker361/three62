import bpy
from mathutils import Vector
from helpers import get_camera_and_scene
import os
#this blender script will get the 6 possible positions and save them for each object

#rescale object

camera,scene=get_camera_and_scene()

def rescale_to_unit_box(obj,target_height=1.0):
    # Make sure the object is selected and active
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    
    # Calculate the bounding box dimensions
    bbox_corners = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
    min_corner = Vector((min(v[0] for v in bbox_corners),
                        min(v[1] for v in bbox_corners),
                        min(v[2] for v in bbox_corners)))
    max_corner = Vector((max(v[0] for v in bbox_corners),
                        max(v[1] for v in bbox_corners),
                        max(v[2] for v in bbox_corners)))
    
    x_dist=max(v[0] for v in bbox_corners)-min(v[0] for v in bbox_corners)
    y_dist=max(v[1] for v in bbox_corners)-min(v[1] for v in bbox_corners)
    
    max_dimension = max(v[2] for v in bbox_corners)-min(v[2] for v in bbox_corners)
    print("bbox corners:", bbox_corners)
    print("obj location",obj.location)
    print(f"max x {x_dist} y {y_dist} z {max_dimension}")
    # Calculate scale factor to fit in a 1x1x1 box
    #max_dimension = max(bbox_size)  # Find the largest dimension
    scale_factor = obj.scale[2]* target_height / max_dimension
    
    # Apply scale factor
    obj.scale = (scale_factor, scale_factor, scale_factor)

    print(f"scale factor is {scale_factor}")


#standardized camera positions and angles
position_angle_list=[]

#character/object collection

def get_collection(collection_name:str):
    if collection_name in bpy.data.collections:
        # Set new_collection to the existing collection
        new_collection = bpy.data.collections[collection_name]
        print(f"Collection '{collection_name}' already exists.")
    else:
        # Create a new collection
        new_collection = bpy.data.collections.new(collection_name)
        bpy.context.scene.collection.children.link(new_collection)
        print(f"Collection '{collection_name}' created.")

    return new_collection

collection_name="characters"

collection=get_collection(collection_name)

script_directory="\\Users\\jlbak\\three62"

character_list=[]
character_images_folder=os.path.join(script_directory,"character_images")
os.makedirs(character_images_folder,exist_ok=True)
for character in character_list:
    if character not in bpy.data.objects:
        obj_filepath=os.path.join(script_directory, "characters",character, f"{character}.obj")
        if os.path.exists(obj_filepath):
            bpy.ops.wm.obj_import(filepath=obj_filepath)
    character_obj=bpy.data.objects[character]
    rescale_to_unit_box(character_obj)
    for i,(position,angle) in enumerate(position_angle_list):
        camera.position=position
        camera.rotation_euler=angle
        file_name=f"{character}_{i}.png"
        bpy.context.scene.render.filepath = os.path.join(character_images_folder, file_name)
        
        bpy.context.scene.render.image_settings.file_format = 'PNG'
        

        # Render and save the screenshot from the camera's perspective
        bpy.ops.render.render(write_still=True)
        
        