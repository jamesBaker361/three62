import bpy
from mathutils import Vector
import os
import sys
script_directory="\\Users\\jlbak\\three62"
sys.path.append(script_directory)
from helpers import get_camera_and_scene
from math import radians
from sixway import hide_collection_from_render,show_collection_from_render,character_dict
import math
import random



def random_point_at_distance(origin, distance):
    """
    Generate a random 3D point that is a fixed distance away from a given origin.
    
    :param origin: Tuple (x, y, z) representing the origin point.
    :param distance: Fixed distance from the origin.
    :return: Tuple (x, y, z) of the random point.
    """
    # Randomly select spherical coordinates
    theta = random.uniform(0, 2 * math.pi)  # Azimuthal angle [0, 2π]
    phi = random.uniform(0, math.pi)       # Polar angle [0, π]

    # Convert spherical coordinates to Cartesian
    x = distance * math.sin(phi) * math.cos(theta)
    y = distance * math.sin(phi) * math.sin(theta)
    z = distance * math.cos(phi)

    # Translate to the origin
    x += origin[0]
    y += origin[1]
    z += origin[2]

    return (x, y, z)

def point_scene_camera_at(target_point):
    # Get the active camera from the scene
    camera = bpy.context.scene.camera
    if not camera:
        print("No active camera found in the scene!")
        return
    
    # Ensure the target point is a Vector
    if not isinstance(target_point, Vector):
        target_point = Vector(target_point)
    
    # Calculate the direction vector
    direction = target_point - camera.location
    direction.normalize()
    
    # Set the camera's rotation to align with the direction vector
    camera.rotation_mode = 'XYZ'
    camera.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
    
    print(f"Scene's active camera is now pointed at {target_point}.")


if __name__=="__main__":
    with open("\\Users\\jlbak\\three62\\metadata.txt","+w") as dest:
        character_images_folder="\\Users\\jlbak\\three62\\character_training"
        os.makedirs(character_images_folder,exist_ok=True)
        n_images_per_character=2
        camera=bpy.context.scene.camera
        render = bpy.context.scene.render
        render.resolution_x = 1024  # Width
        render.resolution_y = 1024  # Height
        render.resolution_percentage = 100  # Scale (100% means full resolution)
        for character in character_dict.keys():
            hide_collection_from_render(character)

        for character,radius in character_dict.items():
            show_collection_from_render(character)
            for n in range(n_images_per_character):
                location=random_point_at_distance((0,0,0),random.uniform(radius,radius*1.5))
                camera.location=location
                point_scene_camera_at((0,0,0))
                file_name=f"{character}_{n}.png"
                bpy.context.scene.render.filepath = os.path.join(character_images_folder, file_name)
                
                bpy.context.scene.render.image_settings.file_format = 'PNG'
                

                # Render and save the screenshot from the camera's perspective
                bpy.ops.render.render(write_still=True)
                dest.write(f"{file_name},{round(camera.location[0],8)},{round(camera.location[1],8)},{round(camera.location[2],8)},{round(camera.rotation_euler.x,8)},{round(camera.rotation_euler.y,8)},{round(camera.rotation_euler.z,8)}\n")
            hide_collection_from_render(character)