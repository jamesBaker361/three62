import bpy


def get_camera_and_scene():
    for obj in list(bpy.data.objects):  # Use a copy of the list to avoid modification during iteration
        if obj.type == 'CAMERA':
            try:
                bpy.data.objects.remove(obj, do_unlink=True)
                print(f"Deleted camera: {obj.name}")
            except ReferenceError:
                print("already removed")

    # Create a new camera
    bpy.ops.object.camera_add(location=(0, 0, 10))  # Adjust location as needed
    camera = bpy.context.object  # The newly created camera becomes the active object

    # Rename the camera to "Camera"
    camera.name = "Camera"

    # Set the new camera as the scene's active camera
    bpy.context.scene.camera = camera

    # Modify the lens property (focal length)
    camera.data.lens = 25  # Set the focal length to 25mm

    print(f"Created new camera '{camera.name}' with lens set to {camera.data.lens}mm.")
    #light=bpy.data.objects["MainLight"]
    scene = bpy.context.scene

    return camera,scene