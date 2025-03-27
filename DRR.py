import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
import scipy
from scipy.ndimage import rotate, binary_dilation
import base64
from PIL import Image
import eel
import os

def load_nifti(file_path_3DRA):
    nifti_img = nib.load(file_path_3DRA)
    data_image = nifti_img.get_fdata()
    return data_image
def generate_drr(volume,  alpha=0, theta=0):
    def get_rotation_matrix(alpha, theta, shape):
        """Generate a 3D rotation matrix for given angles."""
        alpha = np.deg2rad(alpha)
        theta = np.deg2rad(theta)

        R_y = np.array([[ np.cos(alpha), 0, np.sin(alpha)],
                        [ 0,            1, 0           ],
                        [-np.sin(alpha), 0, np.cos(alpha)]])

        R_x = np.array([[1, 0,           0          ],
                        [0, np.cos(theta), -np.sin(theta)],
                        [0, np.sin(theta),  np.cos(theta)]])

        R = R_x @ R_y  # Combine rotations (first Y, then X)
        
        # Compute the shift to keep the center stable
        center = np.array(shape) / 2
        shift = center - R @ center
        return R, shift

    # Get transformation matrix
    R, shift = get_rotation_matrix(alpha, theta, volume.shape)

    # Apply affine transform for rotation
    rotated_vol = scipy.ndimage.affine_transform(volume, R, offset=shift, order=1)
    # Generate DRR by averaging over depth
    drr_img = np.mean(rotated_vol, axis=2)


    return drr_img

def create_compressed_images(angle_increment, dra_path):
    volume = load_nifti(dra_path)
    alpha = list(range(0,360,angle_increment))
    theta = list(range(0,180,angle_increment))
    time_per_image = 1 #in seconds
    eta = time_per_image*len(alpha)*len(theta)

    eel.append_log("Clearing buffer folder", "black", True)
    
    if not os.path.exists("buffer"):
        os.makedirs("buffer")
    for image in os.listdir("buffer"):
        try:
            os.remove("buffer/"+image)
        except:
            print("Could not remove "+image)


    eel.append_log("Estimated time needed for image compression: "+str(eta/60)+" Minutes", "black", True)
    i = 1
    for alpha_ in alpha:
        for theta_ in theta:
            drr_img = generate_drr(volume, alpha_, theta_)
            image_name = "IMAGE_X"+str(alpha_)+"_Y"+str(theta_)+".png"
            # drr_img = np.nan_to_num(drr_img, nan=0, posinf=0, neginf=0)
            # drr_img = np.maximum(drr_img, 0)
            drr_img = 255*(drr_img-np.min(drr_img))/(np.max(drr_img)-np.min(drr_img))
            # drr_img = np.clip(drr_img, 0, 255)
            drr_img_uint8 = drr_img.astype(np.uint8)

            # drr_img_uint8 = np.uint8(drr_img/np.max(drr_img) * 255)
            im = Image.fromarray(drr_img_uint8)
            im.save("buffer/"+image_name)
            #eel.append_log(str(i)+"/"+str(len(alpha)*len(theta)), "black", True)
            eel.setprogress(str(i/(len(alpha)*len(theta))*100))
            i=i+1
    eel.append_log("Images compressed and stored in buffer folder", "black", True)

