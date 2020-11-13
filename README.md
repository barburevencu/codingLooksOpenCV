# Project Name
codingLooksOpenCV

# Description
A program for coding preferential looking studies for infancy research from video files (think manual offline eyetracker).

# Usage
## Starting the program
The program can be launched from the terminal/command line. After changing the working directory to the location of ```openCV.py``` and of the video to be coded, run:
```
python openCV.py NAME-OF-VIDEO.mp4 NAME-OF-OUTPUT-FILE.xlsx
```

## Initializing relevant parameters
First, the program will ask you to pass it the subject ID, then the experimental order. This information will be appended to the output file, and will come handy in data analysis to match the observation to information about experimental manipulation.

## Video
The first frame of the video will then appear on your screen, with the frame number superimposed in orange.

### Navigation: Use Keyboard Arrows
<kbd>&#8594;</kbd>: Advance one frame   
<kbd>&#8592;</kbd>: Go back one frame    
<kbd>&#8593;</kbd>: Skip 100 frames  
<kbd>&#8595;</kbd>: Go back 50 frames  
 
## Coding: Key Semantics
<kbd>l</kbd> OR <kbd>a</kbd>: Left gaze  
<kbd>r</kbd> OR <kbd>d</kbd>: Right gaze  
<kbd>c</kbd> OR <kbd>s</kbd>: Center gaze  
<kbd>b</kbd>: Blink  
<kbd>w</kbd>: Look-away  
<kbd>u</kbd>: Unknown  
<kbd>n</kbd>: NA  
<kbd>E</kbd>: End of current trial phase  
<kbd>M</kbd>: Mistake  
<kbd>B</kbd>: Set current phase to "Baseline"  
<kbd>H</kbd>: Set current phase to "Highlight"  
<kbd>T</kbd>: Set current phase to "Test"    
<kbd>F</kbd>: Flush to .csv  
<kbd>Q</kbd>: Quit program (and get excel file)
