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

dirname = os.path.dirname(__file__)

eel.init(dirname+'/web')

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
def image_to_data_url(filename):
    ext = filename.split('.')[-1]
    prefix = f'data:image/{ext};base64,'
    with open(filename, 'rb') as f:
        img = f.read()
    return prefix + base64.b64encode(img).decode('utf-8')

@eel.expose 
def file_selector():
    window = tk.Tk()
    window.wm_attributes('-topmost', 1)
    window.withdraw()
    filename = askopenfilename(parent=window, filetypes=[("Niftii","*.nii.gz")])
    return filename

eel.start('index.html', mode='edge')

