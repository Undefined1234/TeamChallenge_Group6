import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import rotate, binary_dilation
import base64
from PIL import Image

 # util

def load_nifti(file_path_3DRA, file_path_mask):
    nifti_img = nib.load(file_path_3DRA)
    nifti_mask = nib.load(file_path_mask)
    data_image = nifti_img.get_fdata()
    data_mask = nifti_mask.get_fdata()
    return data_image, data_mask

def extract_aneurysm_neck(segmentation):
    aneurysm_mask = segmentation == 2
    blood_vessel_mask = segmentation == 1    
    
    dilated_vessels = binary_dilation(blood_vessel_mask, structure=np.ones((2, 2, 2)))
    aneurysm_neck = dilated_vessels & aneurysm_mask

    dilated_aneurysm = binary_dilation(aneurysm_mask, structure=np.ones((4, 4, 4)))
    aneurysm_neck_vessel = dilated_aneurysm & blood_vessel_mask

    aneurysm_neck_mask = np.zeros_like(segmentation)
    aneurysm_neck_mask[aneurysm_neck | aneurysm_neck_vessel] = 1
    return aneurysm_neck_mask

def generate_drr(volume,segmentation,aneurysm_neck_seg, angle=0, axis='z'):
    if axis == 'x':
        rotated_vol = rotate(volume, angle, axes=(1, 2), reshape=False)     # axes zijn de twee assen waarover wordt geroteerd, dus bijvoorbeeld; axes = (0,1) is een rotatie om de x en y as en daarom een rotatie in de z richting.
        rotated_seg = rotate(segmentation, angle, axes=(1, 2), reshape=False)
        rotated_neck = rotate(aneurysm_neck_seg, angle, axes=(1, 2), reshape=False)
    elif axis == 'y':
        rotated_vol = rotate(volume, angle, axes=(0, 2), reshape=False)
        rotated_seg = rotate(segmentation, angle, axes=(0, 2), reshape=False)
        rotated_neck = rotate(aneurysm_neck_seg, angle, axes=(0, 2), reshape=False)
    else:  
        rotated_vol = rotate(volume, angle, axes=(0, 1), reshape=False)
        rotated_seg = rotate(segmentation, angle, axes=(0, 1), reshape=False)
        rotated_neck = rotate(aneurysm_neck_seg, angle, axes=(0, 1), reshape=False)

    drr_img = np.mean(rotated_vol, axis=2)   # axis = 2 betekend hier dat de gemiddeldes worden bepaald over de diepte van het geroteerde volume en dus niet over de breedte of hoogte.

    rotated_seg_int = np.round(rotated_seg).astype(np.int32)
    rotated_neck_int = np.round(rotated_neck).astype(np.int32)
    count_1 = np.sum((rotated_seg_int == 1) | (rotated_seg_int == 2), axis=2)
    count_2 = np.sum(rotated_seg_int == 2, axis=2)
    count_vessel = np.sum(rotated_seg_int == 1, axis=2)
    count_neck = np.sum(rotated_neck_int == 1, axis=2)

    return drr_img, count_1, count_2, count_vessel, count_neck

def visibilty_rating(c3_img):
    binary_img = (c3_img > 0).astype(np.uint8)
    overlap_img = c3_img[:][:][0]-c3_img[:][:][2]
    rating = sum(c3_img[:][:][2])-sum(overlap_img)
    return rating


# main
folder_path = "C:\Tue\Group challenge\Aneurysm_TC_data"
patient_ID = '/C0001' # HIER PATIENT ID TOEVOEGEN
file_path_3DRA = folder_path + patient_ID + '/3DRA.nii.gz'
file_path_mask = folder_path + '/Corrected_segms/' + patient_ID + '/corrected_segmentation.nii.gz'

volume, segmentation = load_nifti(file_path_3DRA, file_path_mask)
aneurysm_neck_seg = extract_aneurysm_neck(segmentation)

angle = 30  # HIER HOEK INVULLEN
rotation_axis = 'y'  # HIER ROTATIE AS INVULLEN
drr_image, count_1_img, count_2_img, count_vessel_img, count_neck = generate_drr(volume, segmentation, aneurysm_neck_seg, angle=angle, axis=rotation_axis)

# drr_image = ((drr_image- drr_image.min()) * (1/(drr_image.max() - drr_image.min()) * 255)).astype('uint8')
# plt.imshow(drr_image)
# plt.show()
# image = Image.fromarray(drr_image)
# image = image.convert('RGB')
# image.save("buffer.png")


# visualisaties
count_1_norm = count_1_img / np.max(count_1_img) 
count_2_norm = count_2_img / np.max(count_2_img) 
count_vessel_norm = count_vessel_img / np.max(count_vessel_img) 
count_neck = count_neck / np.max(count_neck)

count_1_norm[count_neck > 0] = 0
count_2_norm[count_neck > 0] = 0

combined_img = np.zeros((*count_1_img.shape, 3))
combined_img[..., 0] = count_vessel_norm  
combined_img[..., 2] = count_2_norm  
combined_img[..., 1] = count_neck

combined_img2 = np.zeros((*count_1_img.shape, 3))
combined_img2[..., 0] = count_2_norm  
combined_img2[..., 1] = count_neck

# r = visibilty_rating(combined_img)
binary_img = (combined_img > 0).astype(np.uint8)
print(max(binary_img))

fig, ax = plt.subplots(2, 3, figsize=(10, 10))
ax[0, 0].imshow(drr_image, cmap='gray')
ax[0, 0].set_title(f"DRR of 3D angiography at {angle} degrees with respect to the {rotation_axis} direction", fontsize = 7)
ax[0, 0].axis('off')

ax[1, 1].imshow(count_vessel_img, cmap='gray')
ax[1, 1].set_title("DRR of vessel structure segmentation")
ax[1, 1].axis('off')

ax[1, 0].imshow(count_2_img, cmap='Blues', interpolation='nearest')
ax[1, 0].set_title("DRR of aneurysm segmentation")
ax[1, 0].axis('off')

ax[0, 1].imshow(combined_img)
ax[0, 1].set_title("DRR of segmentation mask")
ax[0, 1].axis('off')

ax[0, 2].imshow(combined_img2)
ax[0, 2].set_title("DRR of aneurysm and neck")
ax[0, 2].axis('off')

ax[1, 2].imshow(count_neck, cmap='Blues')
ax[1, 2].set_title("DRR of aneurysm neck only")
ax[1, 2].axis('off')

plt.tight_layout()
plt.show()


