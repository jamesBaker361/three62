import bpy
from mathutils import Vector
import os
import sys
script_directory="\\Users\\jlbak\\three62"
sys.path.append(script_directory)
from helpers import get_camera_and_scene
from math import radians
#this blender script will get the 6 possible positions and save them for each object

#rescale object

camera=bpy.context.scene.camera

render = bpy.context.scene.render
render.resolution_x = 1024  # Width
render.resolution_y = 1024  # Height
render.resolution_percentage = 100  # Scale (100% means full resolution)

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


def hide_collection_from_render(collection_name):
    # Get the collection
    collection = bpy.data.collections.get(collection_name)
    if not collection:
        print(f"Collection '{collection_name}' not found!")
        return
    
    # Disable rendering for the entire collection
    collection.hide_render = True
    print(f"Collection '{collection_name}' is now hidden from renders.")

def show_collection_from_render(collection_name):
    # Get the collection
    collection = bpy.data.collections.get(collection_name)
    if not collection:
        print(f"Collection '{collection_name}' not found!")
        return
    
    # Disable rendering for the entire collection
    collection.hide_render = False
    print(f"Collection '{collection_name}' is now hidden from renders.")

#standardized camera positions and angles
position_angle_list=[
    [(0,-1,0),(90,0,0)], 
    [(0,1,0),(90,0,180)],
    [(1,0,0),(90,0,90)],
    [(-1,0,0),(90,0,-90)],
    [(0,0,1),(0,0,0)],
    [(0,0,-1),(-180,0,0)]
]




character_dict={"FuneralCarriage":6.5,
                "AngoraCat":0.75,
                "Brick":0.75}

for character in character_dict.keys():
    hide_collection_from_render(character)


character_images_folder=os.path.join(script_directory,"character_images")
os.makedirs(character_images_folder,exist_ok=True)
for character,radius in character_dict.items():
    show_collection_from_render(character)
    for i,(position,angle) in enumerate(position_angle_list):
        location=[radius *p for p in position]
        camera.location=location
        camera.rotation_euler=[radians(a) for a in angle]
        file_name=f"{character}_{i}.png"
        bpy.context.scene.render.filepath = os.path.join(character_images_folder, file_name)
        
        bpy.context.scene.render.image_settings.file_format = 'PNG'
        

        # Render and save the screenshot from the camera's perspective
        bpy.ops.render.render(write_still=True)
    hide_collection_from_render(character)   