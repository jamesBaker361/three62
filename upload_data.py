import datasets
import os
from PIL import Image



def control_images():
    directory="character_images"
    png_files = [file for file in os.listdir(directory) if file.endswith(".png")]
    name_set=set()

    src_dict={str(i):[] for i in range(6)}
    src_dict["name"]=[]

    for file in png_files:
        name=file.split("_")[0]
        name_set.add(name)

    for name in name_set:
        src_dict["name"].append(name)
        for i in range(6):
            src_dict[str(i)].append(Image.open(os.path.join(directory, f"{name}_{i}.png")))

    datasets.Dataset.from_dict(src_dict).push_to_hub("jlbaker361/three62-control")

def training_images():
    directory="character_training"
    png_files = [file for file in os.listdir(directory) if file.endswith(".png")]
    name_set=set()

    src_dict={str(i):[] for i in range(6)}
    src_dict["name"]=[]

    for file in png_files:
        name=file.split("_")[0]
        name_set.add(name)

    src_dict={key:[] for key in ["image","name","x","y","z","rot_x","rot_y","rot_z"]}
    with open("metadata.txt") as src:
        for line in src:
            split_line=line.split(",")
            image_file=split_line[0]
            name=image_file.split("_")[0]
            src_dict["name"].append(name)
            src_dict["image"].append(Image.open(os.path.join(directory,image_file)))
            for i,key in enumerate(["x","y","z","rot_x","rot_y","rot_z"]):
                src_dict[key].append(split_line[i+1])

    datasets.Dataset.from_dict(src_dict).push_to_hub("jlbaker361/three62-training")




if __name__=="__main__":
    training_images()