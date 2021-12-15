# Description
This repository performs the automated segmentation of the lecture recordings. Furthermore, it 
implements a recommender system for the learning units of online teaching.
## Requirements
```
python 3.8.8
Libraries for segmentation tool: see requirements_tool.txt
Libraries for recommender system: see requirements_anaconda.txt
```
## Run the segmentation tool
```
python main.py PATH_TO_RECORDINGS WHITEBOARD_PROF_IN_FULL_SCREEN
```

The parameter PATH_TO_RECORDINGS is the path to the folder with lecture recordings. 
For each lecture analysed, a result folder is created in the same path.

The parameter WHITEBOARD_PROF_IN_FULL_SCREEN is optional.
This parameter should be set to True if the recordings contains whitebaords scenes with professor in full screen.
This type of video should be in a separate path.<br/>
This tool can also be run with an IDE like PyCharm

## Run the recommender system
Jupiter Notebooks are provided for the recommender system.
This should be run in an anconda3 environment. see requirements

