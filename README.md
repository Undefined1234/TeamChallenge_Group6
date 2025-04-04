# TeamChallenge_Group6
[!Note]
(For this tool you will need [Edge Explorer](https://www.microsoft.com/nl-nl/edge/download?form=MA13FJ) on your device)

Repository containing the Aneurysma Angle Estimation (AAE) GUI. This tool runs HTML in the front-end and uses python in the backend. Javascript is being used as translation language between HTML and python. 

The AAE tool uses 3DRA images to approximate the best angle under which the C-arm should be placed to obtain a 2D image that maps the aneurysm. 

## Installation
1) Create a virtual environment 
2) Open terminal and CD into this directory 
3) Run the following code and make sure the virtual environment is selected: pip install -r requirements.txt
4) run main.py

```
pip install -r requirements.txt
```
By just running the [main.py](main.py) file a GUI should start in Edge explorer. Please note that Edge must be installed on your device in order to run the GUI. 

## GUI
This GUI consists out of a backend and frontend part. The frontend relies on javascript and html and the backend relies on python. In order to preview the 3DRA files a file can be chosen in the input section of the tool. In order to perform angle estimations both a parameter file and the 3DRA file should be included in the left-top corner of the tools. 

## [CUDA](https://developer.nvidia.com/cuda-downloads)
This GUI is also CUDA compatable. In order for CUDA to work properly please install the correct version of [torch](https://pytorch.org/get-started/locally/). Upon running the angle estimation the GUI will tell if a CUDA device was found. If nu CUDA device could be found the estimation will be performed on CPU. 

## Troubleshooting

[!Caution]
This tool is for demonstration purposes only. Please do not use this tool for actual angle estimation.
