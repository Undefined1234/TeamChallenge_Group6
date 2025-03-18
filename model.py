import pandas as pd
import torch 
import numpy as np
import torch.nn as nn
from torchsummary import summary
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from datetime import datetime
import neptune

from torchvision.io import read_image
from torchvision.transforms.functional import to_tensor

DATA_PATH = "dataset/" #Do not change folder structure that was created by Kasper
# dataset/
#   DRR_images/
#       [n].png
#   excel/
#       *.xlsx 


class Block(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 4, 3, 1, 1)  # In: (1, 256, 256), Out: (32, 256, 256)
        self.pool1 = nn.MaxPool2d(2,2)         # In: (32, 256, 256), Out: (32, 64, 64)
        self.conv2 = nn.Conv2d(4, 16, 3, 1, 1) # In: (32, 64, 64), Out: (64, 62, 62)
        self.pool2 = nn.MaxPool2d(2,2)         # In: (64, 62, 62), Out: (64, 15, 15)
        self.flatten = nn.Flatten()
        self.ln1 = nn.Linear(16*64*64, 64)  # Aangepast naar de juiste grootte van de tensor
        self.relu = nn.ReLU()
        self.ln2 = nn.Linear(64,5)
        self.bn1 = nn.BatchNorm2d(4)
        self.bn2 = nn.BatchNorm2d(16)


    def forward(self, x):
        x = self.conv1(x)  # Convolution layer 1
        x = self.bn1(x)
        x = self.pool1(x)  # Pooling layer 1
        x = self.conv2(x)  # Convolution layer 2
        x = self.bn2(x)
        x = self.pool2(x)  # Pooling layer 2
        x = self.flatten(x)  # Flatten the tensor
        x = self.ln1(x)  # Fully connected layer
        x = self.relu(x)
        x = self.ln2(x)
        return x
    
    
class CustomImageDataset(torch.utils.data.Dataset):
    def __init__(self, data):
        self.img_labels = data
        self.img_labels['fullpath'] = DATA_PATH+"DRR_images/"+self.img_labels['DRR filename']+".png"
        self.img_dir = DATA_PATH+"DRR_images"
        self.transform = None
        self.target_transform = None

    def __len__(self):
        return len(self.img_labels)

    def __getitem__(self, idx):
        image = read_image(self.img_labels.iloc[idx]["fullpath"])
        image = image.type(torch.FloatTensor)
        label = self.img_labels.iloc[idx]["score_classified"]
        return image, label