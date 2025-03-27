import eel 
import os
import numpy as np
import DRR_own_method as drr
import random
from random import randint
import base64
import matplotlib as plt
from tkinter.filedialog import askopenfilename
import tkinter as tk
from PIL import Image
import nibabel as nib
import cv2
from io import BytesIO
from ctypes import *
import DRR

dirname = os.path.dirname(__file__)

#eel.init(dirname+'/web')
eel.init("web")

@eel.expose
def random_number():
    print("Random function")
    return randint(1,100)


@eel.expose
def show_view(dra_path: str, mask_path: str, axis: str) -> str:
    """Will parse the compressed images
    
    output: dra image 
    """
    
    dra, mask =  drr.load_nifti(dra_path, mask_path)
    aneurysm_neck_mask = drr.extract_aneurysm_neck(mask)



    if axis.lower() == 'x':
        image,count_1_img, count_2_img, count_neck = drr.generate_drr(dra, mask, aneurysm_neck_mask,0 , 'x')
        return

    if axis.lower() == 'y':
        image,count_1_img, count_2_img, count_neck = drr.generate_drr(dra, mask, aneurysm_neck_mask, 0 , 'y')
        return

    if axis.lower() ==  'z':
        image,count_1_img, count_2_img, count_neck = drr.generate_drr(dra, mask, aneurysm_neck_mask, 0 , 'z')

    image = ((image- image.min()) * (1/(image.max() - image.min()) * 255)).astype('uint8')
    image = Image.fromarray(image)
    image = image.convert('RGB')
    base = os.getcwd()
    image.save(base + "/buffer.png")
    image_base64 = image_to_data_url(base+"/buffer.png")

    return image_base64

@eel.expose
def show_image(dra_path, axis="x", index=0):
    image = nib.load(dra_path)
    image = image.get_fdata()
    index = int(index)
    if (axis=="x"):
        shape = image.shape[0]
        image = image[index,:,:]
        return {"image": array_to_data_url(image), "shape": shape}
    if (axis=="y"):
        shape = image.shape[1]
        image = image[:,index,:]
        return {"image": array_to_data_url(image), "shape": shape}
    else:
        shape = image.shape[2]
        image = image[:,:,index]
        return {"image": array_to_data_url(image), "shape": shape}
    



@eel.expose 
def file_selector(parameters:bool=False):
    window = tk.Tk()
    window.wm_attributes('-topmost', 1)
    window.withdraw()
    if parameters:
        filetype = [("Parameter file", "*.pth")]
    else:
        filetype= [("Niftii", "*.nii.gz")]
    filename = askopenfilename(parent=window, filetypes=filetype)
    return filename

@eel.expose
def image_to_data_url(filename):
    ext = filename.split('.')[-1]
    prefix = f'data:image/{ext};base64,'
    with open(filename, 'rb') as f:
        img = f.read()
    return prefix + base64.b64encode(img).decode('utf-8')

@eel.expose
def array_to_data_url(image):
    image = ((image- image.min()) * (1/(image.max() - image.min()) * 255)).astype('uint8')
    image = Image.fromarray(image)
    image = image.convert('RGB')
    store = BytesIO()
    image.save(store, format="jpeg")
    ext = "jpeg"
    prefix = f'data:image/{ext};base64,'
    bytesimage = store.getvalue()
    image.close()
    return prefix + base64.b64encode(bytesimage).decode('utf-8')


@eel.expose
def start_process():
    #Starting with sanity checks
    if (eel.getinnerHTML("dra_path") == "" or eel.getinnerHTML("model_parameters") == ""):
        eel.append_log("Could not find paths", "red", True)
        return
    angle_increment = int(eel.getangle()())
    print(angle_increment)
    dra_path = eel.getinnerHTML("dra_path")()
    parameter_path = eel.getinnerHTML("model_parameters")()

    eel.append_log("Compressing 3DRA images to 2D images", "black", True)
    DRR.create_compressed_images(angle_increment=angle_increment, dra_path=dra_path)
    eel.append_log("Starting ML model", "black", True)


eel.start('index.html', mode='edge', size=(1920,1080))

